from importlib.metadata import version, PackageNotFoundError
# no default exports, depends on which backend is imported
__all__ = [
    "VERSION",
]
try:
    # this requires the package to be installed!
    VERSION = version("slogger")
except PackageNotFoundError:
    VERSION = "dev"  # fallback version - running with python -m slogger


def get_version():
    return VERSION

def __version__():
    return get_version()
