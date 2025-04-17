"""OpenCAL

OpenCAL core library for Python

Note:

    This project is in beta stage.

Viewing documentation using IPython
-----------------------------------
To see which functions are available in `opencal`, type ``opencal.<TAB>`` (where
``<TAB>`` refers to the TAB key), or use ``opencal.*get_version*?<ENTER>`` (where
``<ENTER>`` refers to the ENTER key) to narrow down the list.  To view the
docstring for a function, use ``opencal.get_version?<ENTER>`` (to view the
docstring) and ``opencal.get_version??<ENTER>`` (to view the source code).
"""

import importlib.metadata
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(name)s:%(message)s',  # See https://docs.python.org/3/library/logging.html#logrecord-attributes
    datefmt=r'%Y-%m-%dT%H:%M:%S%z'
)

import opencal.config

cfg, config_path = opencal.config.get_config()

# import opencal.core.professor.acquisition.arthur
# import opencal.core.professor.acquisition.baptiste
# import opencal.core.professor.acquisition.charles
# import opencal.core.professor.acquisition.denis
# import opencal.core.professor.acquisition.ernest
# import opencal.core.professor.acquisition.professor
# import opencal.core.professor.acquisition.ralph
# import opencal.core.professor.acquisition.randy
# import opencal.core.professor.consolidation.alice
# import opencal.core.professor.consolidation.berenice
# import opencal.core.professor.consolidation.brutus
# import opencal.core.professor.consolidation.celia
# import opencal.core.professor.consolidation.doreen
# import opencal.core.professor.consolidation.professor
import opencal.io.database
import opencal.models
# import opencal.statistics

# PEP0440 compatible formatted version, see:
# https://www.python.org/dev/peps/pep-0440/
#
# Generic release markers:
# X.Y
# X.Y.Z # For bugfix releases  
# 
# Admissible pre-release markers:
# X.YaN # Alpha release
# X.YbN # Beta release         
# X.YrcN # Release Candidate   
# X.Y # Final release
#
# Dev branch marker is: 'X.Y.dev' or 'X.Y.devN' where N is an integer.
# 'X.Y.dev0' is the canonical version of 'X.Y.dev'

__version__ = importlib.metadata.version("opencal")


def get_version():
    return __version__


__all__: list[str] = [
    # 'get_version',
]