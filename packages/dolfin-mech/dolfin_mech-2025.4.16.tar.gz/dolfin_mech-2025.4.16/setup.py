import datetime
import os
import setuptools

# version = os.environ['CI_COMMIT_TAG']
version = datetime.date.today().strftime("%Y.%m.%d")

setuptools.setup(
    name="dolfin_mech",
    version=version,
    author="Martin Genet",
    author_email="martin.genet@polytechnique.edu",
    description=open("README.md", "r").readlines()[1][:-1],
    long_description = open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mgenet/dolfin_mech",
    packages=["dolfin_mech"],
    license="GPLv3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=["gmsh", "matplotlib", "meshio", "numpy", "pandas", "vtk", "myPythonLibrary", "myVTKPythonLibrary", "vtkpython_cbl"],
)
