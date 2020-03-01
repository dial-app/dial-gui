#!/usr/bin/env python3
# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Entry point for dial ui.
"""

import sys
from typing import List


def main(sys_args: List = sys.argv[1:]):
    """
    Entry point for Dial. Initialize components and stars the application.

    Args:
        sys_args: A list of arguments from the command line.
    """
    import dial_core

    # Parse arguments
    app_config = dial_core.utils.initialization.parse_args(sys_args)

    # Initialize
    from dial_gui.utils import initialization

    initialization.initialize(app_config)

    from dial_gui import app

    # Run
    sys.exit(app.run(app_config))


if __name__ == "__main__":
    main()
