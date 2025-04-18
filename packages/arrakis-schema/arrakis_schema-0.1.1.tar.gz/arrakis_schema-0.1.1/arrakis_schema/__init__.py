# Copyright (c) 2025, California Institute of Technology and contributors
#
# You should have received a copy of the licensing terms for this
# software included in the file "LICENSE" located in the top-level
# directory of this package. If you did not, you can view a copy at
# https://git.ligo.org/ngdd/arrakis-python/-/raw/main/LICENSE

from __future__ import annotations

import json
import sys
from typing import Any, TypedDict

from ._version import __version__

if sys.version_info < (3, 12):
    import importlib_resources as resources
else:
    from importlib import resources


class Request(TypedDict):
    request: str
    args: dict[str, Any]


def load_schema(filename: str) -> Request:
    """Load the schema associated with the filename.

    Parameters
    ----------
    filename : str
        The schema file to load.

    Returns
    -------
    Request
        The descriptor schema.

    """
    resource = resources.files().joinpath(filename)
    with resources.as_file(resource) as path:
        return json.loads(path.read_text())
