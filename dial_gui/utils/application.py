# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:


import toml

PYPROJECT = toml.load("pyproject.toml")


def version() -> str:
    """Returns the current version of the application."""
    return PYPROJECT["tool"]["poetry"]["version"]
