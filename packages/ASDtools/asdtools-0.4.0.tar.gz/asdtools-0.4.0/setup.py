from setuptools import setup

with open("README_no_images.md", "r") as f:
    description = f.read()

setup(
    name='ASDtools',
    version='0.4.0',
    author='Autumn Stephens',
    author_email='aust8150@colorado.edu',
    packages=['ASDtools'],
    url='https://github.com/Autumn10677/ASDtools.git',
    description='A set of tools for loading and visualizing the NIST ASD.',
    install_requires=['astropy',
                      'astroquery',
                      'Fraction',
                      'ipython!=8.17.1,<9.0.0,>=8.13.0',
                      'matplotlib',
                      'numpy<2',
                      'pandas',
                      'periodictable',
                      'roman',
                      'sympy',
                      'tqdm'],
    long_description=description,
    long_description_content_type="text/markdown"
)