from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("example-package")
except PackageNotFoundError:
    __version__ = "0.0"