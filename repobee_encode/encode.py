"""Write your plugin in here!

This module comes with two example implementations of a hook, one wrapped in
a class and one as a standalone hook function.

.. module:: encode
    :synopsis: Encodes files in a chosen charset

.. moduleauthor:: Oscar Ekholm
"""

# these two imports are just for the sample plugin, remove if not used!
import pathlib
import os
from typing import Union

# this import you'll need
import repobee_plug as plug

PLUGIN_NAME = "encode"


class ExamplePlugin(plug.Plugin):
    """Example plugin that implements the act_on_cloned_repo hook."""

    def act_on_cloned_repo(
        self, path: Union[str, pathlib.Path], api: plug.API
    ) -> plug.HookResult:
        """List all files in a cloned repo.
        
        Args:
            path: Path to the student repo.
            api: An instance of :py:class:`repobee_plug.API`.
        Returns:
            a plug.HookResult specifying the outcome.
        """
        path = pathlib.Path(path)
        filepaths = [
            str(p)
            for p in path.resolve().rglob("*")
            if ".git" not in str(p).split(os.sep)
        ]
        output = os.linesep.join(filepaths)
        return plug.HookResult(hook=PLUGIN_NAME, status=plug.Status.SUCCESS, msg=output)


@plug.repobee_hook
def act_on_cloned_repo(
    path: Union[str, pathlib.Path], api: plug.API
) -> plug.HookResult:
    """Return an error hookresult with a garbage message.
    
    Args:
        path: Path to the student repo.
        api: An instance of :py:class:`repobee_plug.API`.
    Returns:
        a plug.HookResult specifying the outcome.
    """
    return plug.HookResult(
        hook=PLUGIN_NAME,
        status=plug.Status.ERROR,
        msg="This plugin is not implemented.",
    )