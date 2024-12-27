from typing import Optional, Any

import argparse
import os


class EnvDefault(argparse.Action):
    def __init__(self,
                 envvar: str,
                 required:bool=True,
                 default:Optional[str]=None,
                 **kwargs: Any) -> None:
        if envvar:
            if envvar in os.environ:
                default = os.environ[envvar]
        if required and default:
            required = False
        super(EnvDefault, self).__init__(default=default, required=required,
                                         **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)

