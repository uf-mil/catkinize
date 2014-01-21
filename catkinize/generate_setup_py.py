from catkinize import utils

def generate_setup_py(project_path):
    return '''## ! DO NOT MANUALLY INVOKE THIS setup.py, USE CATKIN INSTEAD

from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

# fetch values from package.xml
setup_args = generate_distutils_setup(
    packages=%r,
    package_dir={'': 'src'},
    requires=[], # TODO
)

setup(**setup_args)''' % (
        utils.get_python_packages(project_path),
    )
