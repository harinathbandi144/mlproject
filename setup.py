from setuptools import find_packages, setup
from typing import List

HYPEN_E_DOT = '-e .'
def get_requirements(file_path:str)->List(str):
    '''
    this functions will written the requirements
    '''

    requirements =[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements = [req.replace('\n', "") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT) # while we writing this to remove '-e .' if comes while excecuting requirements
    return requirements

# setup(
#     name="mlproject",
#     version="0.0.1",
#     author="hari",
#     author_email="harinath.bandi144@gmail.com",
#     packages=find_packages(),
#     # #install_requires=[
#     #     "pandas",
#     #     "numpy",
#     #     "seaborn"
#     # ]
#     install_requires=get_requirements("requirements.txt"))
setup(
    name="mlproject",
    version="0.0.1",
    author="hari",
    author_email="harinath.bandi144@gmail.com",
    packages=find_packages(where="src"),   # 👈 look inside src/
    package_dir={"": "src"},               # 👈 map root to src/
    install_requires=get_requirements("requirements.txt"),
)