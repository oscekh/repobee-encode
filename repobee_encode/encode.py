"""Plugin that encodes select files in a chosen charset. E.g. encode all files ending with .java as utf-8.

.. module:: encode
    :synopsis: Encodes files in a chosen charset

.. moduleauthor:: Oscar Ekholm
"""

import os
import pathlib
from typing import Union
import repobee_plug as plug

PLUGIN_NAME = "encode"

class EncodeHooks(plug.Plugin):
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

        out = []
        pattern = "*.java"

        try:
            path = pathlib.Path(path)

            if not path.exists():
                return plug.HookResult(
                    hook=PLUGIN_NAME,
                    status=plug.Status.ERROR,
                    msg=f"student repo {path!s} does not exist",
                )

            # error on rglob
            filepaths = [
                p
                for p in path.resolve().rglob(pattern)
                if ".git" not in str(p).split(os.sep)
            ]

            for path in filepaths:
                out.append(str(path))

                from_encoding = "iso-8859-1"
                to_encoding = "utf-8"

                # error when encoding is wrong
                with path.open(mode="r", encoding=from_encoding) as f:
                    content = f.read()

                # ValueError if path doesn't have a name
                tempfile = path.with_name(path.stem + "_tmp" + path.suffix)
                tempfile.write_text(content, encoding=to_encoding)
                #tempfile.replace(path)

            output = os.linesep.join(out)

            return plug.HookResult(
                hook=PLUGIN_NAME,
                status=plug.Status.SUCCESS,
                msg=output
            )
        except Exception as exc:
            return plug.HookResult(
                hook=PLUGIN_NAME,
                status=plug.Status.ERROR,
                msg=str(exc),
            )
