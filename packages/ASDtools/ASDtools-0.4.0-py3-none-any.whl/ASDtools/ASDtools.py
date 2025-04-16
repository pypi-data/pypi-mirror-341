import matplotlib.patches as patches
import matplotlib.pyplot as plt
import astropy.units as u
import periodictable
import pandas as pd
import numpy as np
import itertools
import warnings
import roman
import os
import re

from sympy.utilities.iterables import multiset_permutations
from astropy.units.quantity import Quantity
from IPython.display import display, Latex
from matplotlib.patches import FancyArrow
from astroquery.nist import Nist
from fractions import Fraction
from tqdm import tqdm

flags = {
    "*": "Intensity is shared by several lines (typically, for multiply classified lines).",
    ":": "Observed value given is actually the rounded Ritz value, e.g., Ar IV, λ = 443.40 Å.",
    "-": "Somewhat lower intensity than the value given.",
    "?": "This level/line may not be real.",
    "†": "Term assignment of the level is questionable",
    "a": "Observed in absorption.",
    "bl": "Blended with another line that may affect the wavelength and intensity.",
    "b": "Band head.",
    "B": "Line or feature having large width due to autoionization broadening.",
    "c": "Complex line.",
    "d": "Diffuse line.",
    "D": "Double line.",
    "E": "Broad due to overexposure in the quoted reference",
    "f": "Forbidden line.",
    "g": "Transition involving a level of the ground term.",
    "G": "Line position roughly estimated.",
    "H": "Very hazy line.",
    "hfs": "Line has hyperfine structure.",
    "h": "Hazy line (same as 'diffuse').",
    "i": "Identification uncertain.",
    "j": "Wavelength smoothed along isoelectronic sequence.",
    "l": "Shaded to longer wavelengths; NB: This may look like a 'one' at the end of the number!",
    "m": "Masked by another line (no wavelength measurement).",
    "p": "Perturbed by a close line. Both wavelength and intensity may be affected.",
    "q": "Asymmetric line.",
    "r": "Easily reversed line.",
    "s": "Shaded to shorter wavelengths.",
    "t": "Tentatively classified line.",
    "u": "Unresolved from a close line.",
    "+x" : "The relative positions of the levels within such a system are accurate within experimental uncertainties, but no experimental connection between this system and the other levels of the spectrum has been made.",
    "+y" : "The relative positions of the levels within such a system are accurate within experimental uncertainties, but no experimental connection between this system and the other levels of the spectrum has been made.",
    "+z" : "The relative positions of the levels within such a system are accurate within experimental uncertainties, but no experimental connection between this system and the other levels of the spectrum has been made.",
    "w": "Wide line.",
    "x": "Extrapolated wavelength",
    "()" : "Theoretical value.",
    "[]" : "This level was determined by interpolation or extrapolation of known experimental values or by semiempirical calculation.",
}

acc_grades = ["AAA", "AA", "A+", "A", "B+", "B", "C+", "C", "D+", "D", "E", "-"]
acc_numbers = [r"\leq 0.3", r"\leq 1", r"\leq 2", r"\leq 3", r"\leq 7", r"\leq 10", r"\leq 18", r"\leq 25", r"\leq 40", r"\leq 50", r"> 50", "???"]

tran_types = {
    "E1": [4.935525e-19, 3],
    "M1": [3.707342e-14, 3], 
    "E2": [8.928970e-19, 5], 
    "M2": [6.707037e-14, 5], 
    "E3": [3.180240e-18, 7], 
    "M3": [2.388852e-13, 7], 
    "M1+E2": [0, 0], 
    "2P": [0, 0], 
    "HF": [0, 0], 
    "UT": [0, 0]
}

class NIST_lines():

    def __init__(self, 
                 elements, 
                 lower_wavelength=0*u.AA, 
                 upper_wavelength=1e7*u.AA, 
                 keep_flag_columns=False, 
                 keep_original_columns=False,
                 update=True):

        def custom_formatwarning(message, category, filename, lineno, file=None, line=None):
            return f'{message}\n'
        warnings.formatwarning = custom_formatwarning
        
        ### Converts elements to list type if it's not already one
        if not isinstance(elements, list): elements = [elements]

        ### Ensures that wavelength bounds have some Astropy units
        if not isinstance(lower_wavelength, u.quantity.Quantity):
            lower_wavelength*=u.nm
            warnings.warn(f"Lower wavelength missing units, converting to nanometers {lower_wavelength}")
        if not isinstance(upper_wavelength, u.quantity.Quantity): 
            upper_wavelength*=u.nm
            warnings.warn(f"Upper wavelength missing units, converting to nanometers {upper_wavelength}")
        if lower_wavelength >= upper_wavelength:
            warnings.warn(f"The upper wavelength bound must be larger than the lower wavelength bound...")
            return

        ### Initializes class instance variables
        self.elements = [str(i) for i in elements]
        self.lower_wavelength = lower_wavelength.to(u.nm)
        self.upper_wavelength = upper_wavelength.to(u.nm)
        self.FLAG_COLUMNS = keep_flag_columns
        self.ORIGINAL_COLUMNS = keep_original_columns
        self.df = None
        self.df_raw = None
        self.keep_cols = ["Element", "Observed", "Ritz", "Type", "Rel.", "Ei (eV)", "Ek (eV)", 
                          "Aki", "gi", "gk", "S", "Acc.", "Lower level", "Upper level"]
        self.update = update
        self.fetch_lines()

    ### Retrieves lines for the specified element
    def fetch_lines(self):

        """
        Attempts to query the NIST ASD and formats
        a pd.DataFrame into a readable form
        """

        warnings.simplefilter("ignore", category=FutureWarning)
        
        ### Iterates over each element/ionization provided by the user
        for element in tqdm(self.elements, desc='Loading NIST ASD Data', disable=not self.update):

            ### Attempts to load NIST ASD data and store it in a DataFrame
            try:
                table = Nist.query(self.lower_wavelength, self.upper_wavelength, linename=element, wavelength_type='vacuum')
                df_temp = table.to_pandas()

                ### Adds data to dataframe if data was found
                if len(df_temp) != 0:
                    df_temp["Element"] = f"{element}"
                    if "Spectrum" in df_temp.columns:
                        df_temp["Element"] = df_temp["Spectrum"]
                    if self.df is None:
                        self.df = df_temp
                    else:
                        if len(df_temp) > 0:
                            self.df = pd.concat([self.df, df_temp], ignore_index=True)

            ### Prevents failure if data isn't found
            except Exception as e:
                pass

        ### Runs if any data was found
        if self.df is not None:
            
            ### Ensures each dataframe is a unique copy
            self.df = self.df.copy()
            self.df_raw = self.df.copy()

            ### Limits DataFrame to only include useful columns
            numeric_columns = ["Rel.", "Observed", "Ritz", "Ei           Ek", "Aki", "gi   gk", ]
            string_columns = ["Element", "Acc.", "Type", "Lower level", "Upper level"]
            self.df = self.df[numeric_columns+string_columns]#.dropna(subset="gi   gk").reset_index(drop=True)

            ### Handles NaN values that implied the transition is allowed
            self.df["Type"] = self.df["Type"].apply(lambda x: np.nan if x=="<NA>" else x)
            self.df["Type"] = self.df["Type"].fillna(value="E1")
            self.df["Acc."] = self.df["Acc."].fillna(value="")
            self.df["gi   gk"] = self.df["gi   gk"].fillna(value="nan - nan")
            self.df = self.df.astype("str")

            ### Creates two separate columns for energies in each transition        
            self.df["Ei (eV)"] = np.array([str(i).split(" ")[0] for i in self.df['Ei           Ek']])
            self.df["Ek (eV)"] = np.array([str(i).split(" ")[-1] for i in self.df['Ei           Ek']])
            self.df = self.df.drop(columns=['Ei           Ek'])

            ### Creates two separate columns for gi/gk in each transition
            self.df[["gi", "gk"]] = self.df["gi   gk"].apply(lambda x: str(x).replace(" ", "").split("-")).to_list()
            self.df = self.df.drop(columns=["gi   gk"])

            ### Removes flags and converts columns to floats
            for col in tqdm(["Rel.", "Observed", "Ritz", "Aki", "Ei (eV)", "Ek (eV)", "gi", "gk"], 
                            desc="Filtering out flags", 
                            disable=not self.update):
                
                self.extract_flags(colname=col)
                self.df[col] = self.df[col].astype(float)

            ### Calculates line strength "S" from DataFrame values
            self.df["S"] = self.df.apply(lambda x: x["gk"] * x["Aki"] * tran_types[x["Type"]][0] * x["Ritz"]**tran_types[x["Type"]][1], axis=1)

            ### Renames existing columns to explicit names w/ units
            self.df = self.df[self.keep_cols]
            self.df.rename(columns={"Observed": "Observed (nm)", "Ritz": "Ritz (nm)", "Type": "Transition Type"}, inplace=True)

        else:
            warnings.warn(f"No data for {self.elements} was found between {self.lower_wavelength} and {self.upper_wavelength}")

    def extract_flags(self, colname):
        """Extracts all relevant flags from line intensities"""

        #### Determines whether the parentheses contain anything
        def handle_parentheses(s):
            contained_string = s[s.find("(")+1:s.find(")")]
            if contained_string=="":
                return "()"
            return f"({contained_string})";

        ### Attempts to extract the leading number from a messy string
        def extract_leading_number(s):
            match = re.match(r'[\(\[\{]?([-+]?\d+(\.\d*)?(e[+-]?\d+)?|\.\d+(e[+-]?\d+)?)', s, re.IGNORECASE)
            return match.group(1) if match else "nan"

        ### Identifies and records all relevant flags
        def handle_flags(s):

            ### Handles weird parentheses formatting
            relevant_flags = []
            if "(" in s: 
                relevant_flags.append(handle_parentheses(s));
                s = s.replace(relevant_flags[0], "")

            ### Looks for known flags
            for flag in flags:
                if flag in s:
                    s = s.replace(flag, "")
                    relevant_flags.append(flag)

            ### Removes remaining commas
            s = s.replace(",", "")

            ### Appends remaining 'flag' to list (mainly for debugging)
            if len(s) > 0:
                relevant_flags.append(s)

            ### Returns NaN for entries with no flags
            if len(relevant_flags) == 0:
                return np.nan

            return relevant_flags

        ### Identifies, scrubs, and lists out all relevant flags into a separate column
        self.df[colname] = self.df[colname].apply(lambda x: "nan" if x=="<NA>" else x)
        self.df[f"{colname}_original"] = self.df[colname].copy()
        self.df[colname] = self.df[colname].apply(lambda x : extract_leading_number(x))
        self.df[f"{colname}_flags"] = self.df.apply(lambda x : x[f"{colname}_original"].replace(x[f"{colname}"], ""), axis=1)
        self.df[f"{colname}_flags"] = self.df[f"{colname}_flags"].apply(lambda x : handle_flags(x))

        ### Determines whether the diagnostic columns should be kept in the final DataFrame
        if (self.FLAG_COLUMNS and len(self.df[f"{colname}_flags"].dropna())>0): 
            col_index = self.keep_cols.index(colname)
            self.keep_cols.insert(col_index+1, f"{colname}_flags");
        if self.ORIGINAL_COLUMNS:
            col_index = self.keep_cols.index(colname)
            self.keep_cols.insert(col_index, f"{colname}_original");

    def explain_column_flags(self, colname):

        ### Ensures that the provided column name is a valid column
        if not "flags" in colname: colname += "_flags";
        if colname not in self.df.columns:
            warnings.warn(f"Column '{colname}' not found in DataFrame. Check that keep_flag_columns=True")
            return

        ### Initializes lists/dictionaries for flag tracking
        column_flags = np.array(self.df[colname].dropna())
        flag_counts = {flag:0 for flag in flags}
        weird_flags = {}

        ### Records the counts of each flag
        for i in column_flags:
            for flag in i:
                if flag in flag_counts.keys():
                    flag_counts[flag] += 1
                elif flag in weird_flags.keys():
                    weird_flags[flag] += 1
                else:
                    weird_flags[flag] = 1

        ### Displays each flag w/ counts w/ known definitions
        for key, value in flag_counts.items():
            if value > 0:
                print(f"   Flag: {key}")
                print(f" Counts: {value}")
                print(f"Meaning: {flags[key]}")
                print()

        ### Displays all the flags w/o known definitions
        for key, value in weird_flags.items():
            if value > 0:
                print(f"   Flag: {key}")
                print(f" Counts: {value}")
                print(f"Meaning: ???")
                print()

    def filter_accuracy(self, min_acc="B"):
        """Filters lines out below a given accuracy"""
        reject_acc = acc_grades[-(len(acc_grades) - acc_grades.index(min_acc)-1):]
        self.df = self.df[~self.df['Acc.'].isin(reject_acc)]

def draw_aufbau_diagram(N_max=6, 
                        save=False, 
                        save_dir="", 
                        filename=""):

    """
    Draws the Aufbau diagram corresponding to
    the last filled s subshell for a given N_max.

    Parameters:
    -----------
    N_max :: int
        Max principal quantum number that should be
        drawn on the diagram.
    save :: bool
        Indicates whether the Grotrian diagram
        should be saved.
    save_dir :: str
        Tells the function where to save the
        Grotrian diagram.
    filename :: str
        The name the image will be saved at.
        This string must end with ".png".
    """
    
    ### Defines orbitals (up to a practical limit)
    orbitals = ['s', 'p', 'd', 'f'] + [chr(ord('g')+i) for i in range(6)]
    
    ### Determines the necessary dimensions of the diagram
    xdim = int(N_max/2) + 0.5*(N_max%2) + 1.5
    ydim = N_max + 1

    ### Initializes figure with specified dimensions
    fig, ax = plt.subplots(figsize=(xdim,ydim))

    ### Draws each arrow on the diagram
    for i in range(1, N_max+1):
        arrow = FancyArrow(i/2+1, i/2, -(i/2+0.4), (i/2+0.4), width = 0.02, head_width=0.2, color = 'black', overhang=0.4)
        ax.add_patch(arrow)

    ### Adds boxes w/ text for each suborbital
    for y in range(1, N_max+1):    
        for x in range(1, min(y+1, N_max-y+2)):
            side_length = 0.5
            ax.text(x, y, f"{y}{orbitals[x-1]}", horizontalalignment="center", verticalalignment="center", fontsize=13)
            rect = patches.Rectangle((x-side_length/2, y-side_length/2), side_length, side_length, linewidth=2, edgecolor='k', facecolor='white')
            ax.add_patch(rect)

    ### Plots / labels the Aufbau diagram
    plt.xlim(0, xdim)
    plt.ylim(0, ydim)
    plt.xticks(list(range(1,int(xdim))))
    plt.yticks(list(range(1,int(ydim))))
    plt.title(f"Aufbau Diagram (up to n={N_max})")
    plt.xlabel(rf"Angular Momentum Number ($\ell$)")
    plt.ylabel(rf"Principal Quantum Number ($n$)")
    plt.tight_layout()
    
    ### Runs if diagram should be saved
    if save:

        ### Filename handling
        if filename == "":
            filename = f"aufbau_diagram_up_to_{N_max}.png"
        if ".png" not in filename:
            print("Invalid filename, please add '.png'")
            save=False

        ### If filename is valid, save diagram
        if save:
            plt.savefig(os.path.join(save_dir, filename))
    
    plt.show()

def find_filling_order(max_level=5, joined=False):

    """
    Finds the Aufbau filling order up to the
    s subshell with a principal quantum number
    given by max_level.

    Parameters:
    -----------
    max_level :: int
        Max principal quantum number that should be
        used in the filling sequence.
    joined :: bool
        Determines whether the output is a list or
        string joined by "."

    Returns:
    orbs :: list / str
        The filling order (w/o electron counts) up
        to a specified maximum principal quantum
        number.
    """

    ### Initializes all relevant orbitals and a list for the filling table
    orbitals = ['s', 'p', 'd', 'f'] + [chr(ord('g')+i) for i in range(6)]
    table = []

    ### Generates table of orbitals for filling order
    for n in range(max_level):
        row = [f"{n+1}{o}" for o in orbitals[:n+1]]
        row += ["" for i in range(max_level-len(row))]
        table.append(row)
    table = np.array(table)

    ### Adds filling order to list
    orbs = []
    for n in range(max_level):
        x,y = (0,n)
        for i in range(n+1):
            if table[x][y] != "":
                orbs.append(table[x][y])
            x+=1
            y-=1

    ### Joins orbitals with a period (NIST format)
    if joined:
        orbs = ".".join(orbs)

    return orbs

def find_electronic_config(element, 
                           abbreviate=False,
                           sortby="fill order"):

    """
    Generates the ground-state electronic 
    configuration for a given element. The
    output can include the full, explicit
    configuraiton, or an abbreviated version which
    replaces filled orbitals with the nearest
    noble gas.

    Parameters:
    -----------
    element :: str
        Element symbol and ionization (i.e., He I)
        to generate a the ground-state electronic
        configuration for.
    abbreviate :: bool
        Determines whether electronic configurations
        should be abbreviated using a noble gas.
    sortby :: str
        Determines the order that the subshells in
        the returned electronic configuration should 
        be ordered.

    Returns:
    --------
    config :: str
        The ground-state electronic configuration for
        the specified element.
    """
    
    ### Initializes orbital names and capacity
    orbitals = ['s', 'p', 'd', 'f'] + [chr(ord('g')+i) for i in range(6)]
    elements = [str(i) for i in periodictable.elements]
    electron_capacity = [2 * (2*l + 1) for l in range(len(orbitals))]
    orb_to_e = {o: e for o, e in zip(orbitals, electron_capacity)}
    orbs = find_filling_order(max_level=10)
    
    ### Determines the number of electrons in atom
    num_protons = elements.index(element.split()[0])+1
    ionization = roman.fromRoman(element.split()[-1])-1
    num_electrons = num_protons-ionization

    ### Finds all filled orbitals + first unfilled orbital
    cumm_electrons = np.cumsum([int(orb_to_e[o[-1:]]) for o in orbs])
    diffs = [i if i>=0 else 1e4 for i in (cumm_electrons-num_electrons)]
    config_list = orbs[:np.argmin(diffs)+1]
    
    ### Adds some formatting so that the electron count in subshells is explicit
    leftover_electrons = (orb_to_e[config_list[-1][-1]] - min(diffs)).clip(0)
    config_list = [f"{conf}{orb_to_e[conf[-1]]}" for conf in config_list[:-1]] + [f"{config_list[-1]}{leftover_electrons}"]
    config = ".".join(config_list)

    ### Runs if abbreviated notation is desired
    closest_noble = ""
    if abbreviate:

        ### Iterates over each noble gas (in reverse order)
        noble_gasses = np.array(["He", "Ne", "Ar", "Kr", "Xe", "Rn"])
        for i in noble_gasses[::-1]:

            ### Runs this function again to get the electronic configuration
            noble_config = find_electronic_config(f"{i} I", abbreviate=False)

            ### If the noble gas configuration is in the element string, use it for abbreviation
            if (noble_config in config) and (noble_config != config):
                config = config.replace(f"{noble_config}.", "")
                closest_noble = f"[{i}]"
                break

    ### Handles the case where an element is "too ionized" to be real
    if config=="1s0":
        return "N/A"

    ### Sorts orbitals to follow strict n and subshell orders
    if sortby=="principle":
        config = config.split(".")
        sorted_config = sorted(config, key=lambda x:(int(x[0]),int(orbitals.index(x[1]))))
        config = ".".join(sorted_config)
    
    return closest_noble + config

def is_subshell_filled(config):

    """
    Determines if a given subshell is filled. 
    This function requires the principal quantum
    number (n), subshell (i.e., s, p, d, etc.),
    and electron count to be provided to work.

    Parameters:
    -----------
    config :: str
        Subshell to be analyzed. Requires the value
        of n, subshell letter, and electron count to
        be explicitly written out.

    Returns:
    --------
    isFilled :: bool
        True or false based on whether the subshell is
        entirely filled.
    """

    ### Initializes orbital names and capacity
    orbitals = ['s', 'p', 'd', 'f'] + [chr(ord('g')+i) for i in range(6)]
    electron_capacity = [2 * (2*l + 1) for l in range(len(orbitals))]
    orb_to_e = {o: e for o, e in zip(orbitals, electron_capacity)}
    
    ### Splits the orbital string into level, subshell, and electron count
    _,subshell,num_electrons = re.findall(r"(\d+|\D+)", config)
    
    return int(num_electrons)==orb_to_e[subshell]

def fraction_from_float(value):
    """Simple wrapper for the Fraction function"""
    return str(Fraction(float(value)).limit_denominator(100))

def microstate_matrix_from_config(config):

    """
    Calculates the matrix describing how
    many possible microconfigurations of
    electrons in a subshell exist for each
    possible ms and ml number.

    Parameters:
    -----------
    subshell :: str
        Subshell to generate a state matrix
        for. Should not include the principal
        quantum number.

    Returns:
    --------
    state_matrix :: np.ndarray
        Matrix describing the number of
        microconfigurations corresponding to
        each possible ms and ml number for a
        given subshell.
    ms_list :: np.ndarray
        All unique ms numbers.
    ml_list :: np.ndarray
        All unique ml numbers.
    parity :: bool
        Whether this configuration has odd
        parity.
    """
    
    ### Defines orbitals
    orbitals = ['s', 'p', 'd', 'f'] + [chr(ord('g')+i) for i in range(6)]

    ### Arrays to hold all subshell ms / ml vals
    ms_array = []
    ml_array = []
    parity = False

    ### Iterates over each subshell in config
    for i in config.split("."):

        ### Only looks at partially filled subshells
        if not is_subshell_filled(i):

            ### Extracts relevant information from subshell string
            _, subshell, num_electrons = re.findall(r"(\d+|\D+)", i)
    
            ### Defines necessary variables using the above extracted strings
            num_slots = 2 * orbitals.index(subshell.lower()) + 1
            num_electrons = int(num_electrons)

            ### Adjust parity if conditions are met
            if (orbitals.index(subshell.lower())%2 == 1) and (num_electrons%2 == 1):
                parity = not parity

            ### Determines all the unique arrangements of electrons
            init_config = [1 if i < num_electrons else 0 for i in range(2 * num_slots)]
            perms = list(multiset_permutations(init_config))
    
            ### Breaks up the above configuration into corresponding spin-up and spin-down e-
            spin_up = np.array([perm[:len(perm)//2] for perm in perms])
            spin_down = np.array([perm[len(perm)//2:] for perm in perms])
            
            ### Lays out m_l values for each slot in configuration
            ml_vals = [i - (num_slots - 1) // 2 for i in range(num_slots)]
    
            ### Calculates ms and ml values for each configuration
            ms_list = np.array([])
            ml_list = np.array([])
            for i in range(len(perms)):
                ms_list = np.append(ms_list, np.sum((spin_up[i]-spin_down[i])/2))
                ml_list = np.append(ml_list, np.sum((spin_up[i]+spin_down[i])*ml_vals))

            ### Adds ms / ml data to array
            ms_array.append(ms_list)
            ml_array.append(ml_list)

    ### Generates all unique combinations of all subshell ms / ml values
    ms_list = [sum(i) for i in itertools.product(*ms_array)]
    ml_list = [sum(i) for i in itertools.product(*ml_array)]
    
    ### Fills out state matrix for ms/ml pairs
    state_matrix = np.zeros((len(np.unique(ml_list)), len(np.unique(ms_list))))
    for ms,ml in zip(ms_list,ml_list):
        state_matrix[int(max(ml_list)+ml), int(max(ms_list)+ms)] += 1
    
    ### Extracts the unique ms and ml numbers
    ms_list = np.unique(ms_list)
    ml_list = np.unique(ml_list)

    return state_matrix, (ms_list, ml_list, parity)

def find_max_rect(matrix):
    """
    Calculates the largest sub-matrix of non-zero
    entries for a given matrix.

    Paramters:
    ----------
    matrix :: np.ndarray
        Matrix with some non-zero values

    Returns:
    --------
    best_rect :: np.ndarray
        Largest non-zero sub-matrix within matrix
    """

    ### Initializes calculation variables
    rows, cols = matrix.shape
    best_area = 0
    best_rect = None
    
    # Iterate over all possible top-left corners
    for r1 in range(rows):
        for c1 in range(cols):
            if matrix[r1, c1] == 0:
                continue
            
            # Expand the rectangle down and right
            for r2 in range(r1, rows):
                if np.any(matrix[r1:r2+1, c1] == 0):
                    break
                for c2 in range(c1, cols):
                    if np.any(matrix[r1:r2+1, c1:c2+1] == 0):
                        break
                    area = (r2 - r1 + 1) * (c2 - c1 + 1)
                    if area > best_area:
                        best_area = area
                        best_rect = (r1, r2, c1, c2)

    return best_rect

def decompose_matrix(matrix, matrix_info):

    """
    Finds the minimal combination of nonzero
    rectangular sub-matrices that sum to a given
    matrix. Also determines the term symbols that
    correspond to each sub-matrix.

    Parameters:
    -----------
    matrix :: np.ndarray
        State matrix to be decomposed.
    matrix_info :: tuple
        Tuple of state matrix ms values, ml values,
        and parity.

    Returns:
    --------
    layers :: np.ndarray
        Array containing each sub-array found in the
        matrix decomposition.
    df :: pd.DataFrame
        Dataframe containing the S, L, J, and parity
        of each term symbol.
    """

    ### Unpacks matrix lists and info
    ms_list, ml_list, parity = matrix_info

    ### Initializes orbital names
    orbitals = ['S', 'P', 'D', 'F'] + [chr(ord('G')+i) for i in range(9)]

    ### Intializes usefule data structures
    layers = []
    working_matrix = matrix.copy()
    terms = []

    ### Runs while nonzero entries remain
    while np.any(working_matrix > 0):

        ### Finds the largest nonzero sub-matrix
        rect = find_max_rect(working_matrix)
        if not rect:
            break

        ### Extracts sub-matrix
        r1, r2, c1, c2 = rect
        layer = np.zeros_like(matrix)
        layer[r1:r2+1, c1:c2+1] = 1
        layers.append(layer)

        ### Subtracts off the identified sub-matrix
        working_matrix[r1:r2+1, c1:c2+1] -= 1

        ### Initializes all possible values of J for this sub-matrix
        L,S = (np.max(ml_list[r1:r2+1]), np.max(ms_list[c1:c2+1]))
        J = np.abs(L-S)

        ### Finds the term symbols represented by sub-matrix
        while J < L+S+1:

            ### Adds unique term symbols to list
            L_str = orbitals[int(L)] if L < len(orbitals) else f"L={L}"
            term_str = f"{S}|{L_str.upper()}|{J}"
            if term_str not in terms:
                terms.append(term_str)

            J+=1
    
        ### Unpack terms into quantum numbers
        S_list, L_str_list, J_list = zip(*(term.split("|") for term in terms))
    
        ### Creates a dataframe containing all unique term symbls
        df = pd.DataFrame({'S': S_list, 'L': L_str_list, 'J': J_list})
        df['J'] = df['J'].apply(fraction_from_float)
        df = df.groupby(['S', 'L'], as_index=False).agg({'J': ', '.join})
        df['Parity'] = parity
    
    return layers, df

def display_term_symbols(df):

    """
    Displays all term symbols in a cohesive,
    LaTeX-driven format. The style of the
    output is largely driven by the preferred
    style of the NIST ASD.

    Parameters:
    -----------
    terms :: pd.DataFrame
        Dataframe containing all the term symbols
        to be displayed.
    """

    ### Initializes oribtal labels
    orbitals = ['S', 'P', 'D', 'F'] + [chr(ord('G')+i) for i in range(9)]

    ### Iterates over each orbital
    print("Term Symbols:\n-------------")
    for i in orbitals:

        ### Limits search to current orbital
        disp_string = f''
        temp_df = df[df['L']==i].reset_index(drop=True)

        ### Iterates over each remaining term
        for i in range(len(temp_df)):

            ### Extracts term info
            S = temp_df["S"][i]
            L = temp_df["L"][i]
            J = temp_df["J"][i]

            ### Handles parity display
            if temp_df["Parity"][i]:
                disp_string = f'$^{int(2*float(S)+1)}{L}^*_{{{J}}}$'
            else:
                disp_string = f'$^{int(2*float(S)+1)}{L}_{{{J}}}$'

            ### Displays term symbol
            display(Latex(disp_string))

def generate_term_symbols(config):

    """
    Takes an electronic configuration
    and finds all possible term symbols.

    Parameters:
    -----------
    config :: str
        Electric configuration to find
        all possible term symbols for.
        Should have subshells in the 
        form "1s2.2s1.3p1"
    """
    
    state_matrix, matrix_info = microstate_matrix_from_config(config)
    layers, df = decompose_matrix(state_matrix, matrix_info=matrix_info)
    display_term_symbols(df)

def draw_grotrian_diagram(element,
                          lower_wavelength=0*u.AA, 
                          upper_wavelength=1e7*u.AA,
                          min_energy = 0,
                          max_energy = 1e10,
                          min_multiplicity = 1,
                          max_multiplicity = 10,
                          min_letter = "S",
                          max_letter = "L",
                          save = False,
                          save_dir = "",
                          filename = "",
                          update=False):

    """
    Queries the NIST ASD for transitions
    corresponding to a given element, and
    draws a Grotrian diagram for all lines
    where it is possible to.

    Parameters:
    -----------
    element :: str
        Element symbol w/ ionization that should
        be used for querying the NIST ASD.
    lower_wavelength :: astropy.Quantity
        Lower wavelength to use when querying the
        NIST ASD.
    upper_wavelength :: astropy.Quantity
        Upper wavelength to use when querying the
        NIST ASD.
    min_energy :: float
        Minimum energy to plot on the Grotrian
        diagram. Assumes unit of eV.
    max_energy :: float
        Maximum energy to plot on the Grotrian
        diagram. Assumes unit of eV.
    min_multiplicity :: int
        Minimum multiplicity to plot on the
        Grotrian diagram.
    max_multiplicity :: int
        Maximum multiplicity to plot on the
        Grotrian diagram.
    min_letter :: str
        Minimum letter (L) to plot on the
        Grotrian diagram. If an invalid letter
        is provided, it is ignored.
    max_letter :: str
        Maximum letter (L) to plot on the
        Grotrian diagram. If an invalid letter
        is provided, it is ignored.
    save :: bool
        Indicates whether the Grotrian diagram
        should be saved.
    save_dir :: str
        Tells the function where to save the
        Grotrian diagram.
    filename :: str
        The name the image will be saved at.
        This string must end with ".png".
    """
    
    ### Queries NIST ASD for data
    lines = NIST_lines(element, lower_wavelength=lower_wavelength, upper_wavelength=upper_wavelength, update=update)

    ### Defines the drawing color and styles of various transitions
    type_styles = {"E1": ["black", "solid"], 
                   "E2": ["blue", "--"], 
                   "E3": ["green", "--"],
                   "M1": ["red", ":"], 
                   "M2": ["orange", ":"],
                   "M3": ["purple", ":"],
                   "M1+E2": ["gray", "--"], 
                   "2P": ["gray", "--"], 
                   "HF": ["gray", "--"], 
                   "UT": ["gray", "--"]
    }
    
    ### Filters out undesired term letters
    orbitals = ['S', 'P', 'D', 'F'] + [chr(ord('G')+i) for i in range(6)]
    if min_letter in orbitals:
        orbitals = orbitals[orbitals.index(min_letter):]
    if max_letter in orbitals:
        orbitals = orbitals[:orbitals.index(max_letter)+1]

    ### Applies filtering / formatting to the queried dataframe to isolate desired data
    df = lines.df.dropna(subset=["Ei (eV)", "Ek (eV)"]).copy()
    df = df[["Ei (eV)", "Ek (eV)", "Transition Type", "Lower level", "Upper level"]]
    df[["Conf_i", "Term_i", "J_i"]] = df["Lower level"].apply(lambda x: x.replace(" ", "").split("|")).to_list()
    df[["Conf_k", "Term_k", "J_k"]] = df["Upper level"].apply(lambda x: x.replace(" ", "").split("|")).to_list()
    df = df.loc[df["Term_i"]!='',:]
    df = df.loc[df["Term_k"]!='',:]
    df = df.loc[df["Ei (eV)"]>=min_energy]
    df = df.loc[df["Ek (eV)"]<=max_energy]
    df = df.dropna().reset_index(drop=True)
    
    ### Iterates over every possible term symbol
    possible_terms = []
    for i in range(min_multiplicity, max_multiplicity+1):
        for letter in orbitals:
            for parity in ["", "*"]:
                possible_term = f"{i}{letter}{parity}"
    
                ### Only keeps a term if it's found within the dataframe
                if possible_term in np.unique(list(df["Term_i"]) + list(df["Term_k"])):
                    possible_terms.append(possible_term)
    
    ### Finds changes in multiplicities
    change_idx = []
    for idx in range(1, len(possible_terms)):
        mult_a,_ = re.findall(r"(\d+|\D+)", possible_terms[idx-1])
        mult_b,_ = re.findall(r"(\d+|\D+)", possible_terms[idx])
        if mult_a != mult_b:
            change_idx.append(idx)
    
    ### Adds tag to ignore for xtick labels
    for idx in reversed(change_idx):
        possible_terms.insert(idx, "IGNORE")
    
    ### Filters out terms that are not "possible" (really anything with odd formatting)
    df["Term_i"] = df["Term_i"].apply(lambda x: int(possible_terms.index(x)) if x in possible_terms else np.NaN)
    df["Term_k"] = df["Term_k"].apply(lambda x: int(possible_terms.index(x)) if x in possible_terms else np.NaN)
    df = df.dropna().reset_index(drop=True)

    ### Will prevent plotting an empty dataframe
    if len(df)==0:
        print("Not enough valid transitions, sorry!")
        return
    
    ### Initializes plots and separates multiplicities with lines
    fig,ax = plt.subplots(figsize=(10, 5))
    for idx,x in enumerate(change_idx):
        plt.axvline(x+idx, color='gray', alpha=0.4)
    
    ### Iterates over each line in the dataframe
    used_labels = []
    for idx in range(len(df)):

        ### Extracts plotting information for line
        x1 = df["Term_i"][idx]
        x2 = df["Term_k"][idx]
        y1 = df["Ei (eV)"][idx]
        y2 = df["Ek (eV)"][idx]
        transition_type = df["Transition Type"][idx]
        color,ls = type_styles[transition_type]

        ### Handles plotting for new labels vs. repeated labels
        if not transition_type in used_labels:
            ax.plot([x1, x2], [y1, y2], color=color, ls=ls, label=transition_type)
            used_labels.append(transition_type)
        else:
            ax.plot([x1, x2], [y1, y2], color=color, ls=ls)

    ### Formatting
    ax.set_title(f"Grotrian Diagram for {element}")
    ax.set_xticks([i for i in range(len(possible_terms)) if possible_terms[i]!="IGNORE"])
    ax.set_xticklabels([i for i in possible_terms if i!="IGNORE"])
    ax.legend(title="Transition Type", shadow=True, edgecolor='k')
    ax.set_ylabel("Level Energy (eV)")
    fig.tight_layout()

    ### Runs if diagram should be saved
    if save:

        ### Filename handling
        if filename == "":
            filename = f"{element.replace(' ', '_')}_grotrian_diagram.png"
        if ".png" not in filename:
            print("Invalid filename, please add '.png'")
            save=False

        ### If filename is valid, save diagram
        if save:
            plt.savefig(os.path.join(save_dir, filename))
    
    plt.show()