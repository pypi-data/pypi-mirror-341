######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.7.2+obcheckpoint(0.1.9);ob(v1)                                                    #
# Generated on 2025-04-16T21:50:24.098238                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.pypi.conda_environment

from .conda_environment import CondaEnvironment as CondaEnvironment

class PyPIEnvironment(metaflow.plugins.pypi.conda_environment.CondaEnvironment, metaclass=type):
    ...

