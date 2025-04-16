#!/usr/bin/python3
import os
import runpy

from setuptools import setup, find_packages
from setuptools.command.install import install

REQUIRES_PYTHON = '>=3.7'

REQUIRED = [
    'pyqt5', 'attrs', 'pyqtgraph >= 0.11', 'psutil', 'pyshortcuts', 'numpy', 'python-dateutil'
]

def abspath(*path):
    """A method to determine absolute path for a given relative path to the
    directory where this setup.py script is located"""
    setup_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(setup_dir, *path)

def get_release_info():
    namespace = runpy.run_path(abspath("beamline_console/release.py"), run_name="beamline_console.release")
    return namespace["Release"]

Release = get_release_info()

class PostInstall(install):
    def run(self):
        pass

# Where the magic happens:
setup(
    name=Release.name,
    version=Release.version_long,
    description=Release.description,
    long_description=Release.long_description,
    long_description_content_type='text/markdown',
    author=Release.authors[0][0],
    author_email=Release.authors[0][1],
    download_url=Release.download_url,
    platforms=Release.platform,
    python_requires=REQUIRES_PYTHON,
    packages=find_packages(),
    package_dir={'beamline_console': 'beamline_console',},
    package_data={'beamline_console': ['LICENSE.txt',
                                      'beamline_console/beamline_console.sh',
                                      'beamline_console/beamline_console.desktop',
                                      'beamline_console/default_config/devices.xml',
                                      'beamline_console/default_config/main.cfg'
                                      ],},
    install_requires=REQUIRED,
    include_package_data=True,
    license='GPLv3',
    entry_points={'console_scripts': ['beamline_console = beamline_console:main',],},
    scripts=['beamline_console/beamline_console.sh'],
    data_files=[('share/applications', ['beamline_console/beamline_console.desktop'])],
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Development Status :: 3 - Alpha'
    ],
)