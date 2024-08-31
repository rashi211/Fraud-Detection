'''
setup.py  - is a module used to build and distribute Python packages.
            It typically contains information about the package, such as its name, version, and dependencies, 
            as well as instructions for building and installing the package.

requirements.txt - This file lists the project's dependencies with their exact versions. 
                    It is used for creating reproducible environments and ensuring that the same dependencies
                    are installed across different machines.

setuptools -  A Python package used for distributing Python projects. 
                It provides utilities to package and distribute Python code.

find_packages - A function from setuptools that automatically discovers all the Python packages 
                and sub-packages in the project directory.

setup -  A function from setuptools that is used to configure and create the package.

List - Imported from typing to specify the return type of the get_requirements function.                    

'''

from setuptools import find_packages,setup
from typing import List

Hypen = '-e .'
#
def get_requirements(file_path:str)->List[str]:
    '''
    This gets the list of requiremnts.
    Input - 
    file_path: This is the parameter for the function, and it represents the path to a file
    str: This is a type hint indicating that the file_path parameter should be of type str (string). 
    Return Type -
    List[str]: This is another type hint that indicates the function will return a list of strings.
    '''
    requirements = []
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements = [req.replace("\n","") for req in requirements]

        if Hypen in requirements:
            requirements.remove(Hypen)
    
    return requirements

setup(
    name='FraudDetection',
    version='0.0.1',
    author='Rashi',
    author_email='rashibajpai1999@gmail.com',
    packages=find_packages(),
    install_requires = get_requirements('requirements.txt')
)
