######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.7.2+obcheckpoint(0.1.9);ob(v1)                                                    #
# Generated on 2025-04-16T19:15:34.484335                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

from ......exception import MetaflowException as MetaflowException

class LoadingException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, message):
        ...
    ...

class ModelException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, message):
        ...
    ...

