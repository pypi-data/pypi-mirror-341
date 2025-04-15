
import os
import platform
import fnmatch
import sysconfig

from importlib import metadata as _ilm
from pathlib import Path as _Path
from ctypes import CDLL as _CDLL



def _locate_file(module: str, name: str) -> _Path:
    """
    Locate a file within a module and return the correct absolute path to
    where the file is installed on the filesystem.

    This function raises an importlib.metadata.PackageNotFoundError upon
    failure.

    :param module: name of the module to locate a file within
    :param name: name of the file to find
    :return: Absolute path to the file as a pathlib.Path object
    """
    dist = _ilm.distribution(module)

    files = [dist.locate_file(path).resolve() for path in dist.files if fnmatch.fnmatch(path.name, name)]

    if not files:
        raise _ilm.PackageNotFoundError(f"Could not find {name} within {module}")

    file = files[0]
    assert file.exists()

    return file

if platform.system() == "Linux":

    # This is critical, the MKL libraries have complicated interdependencies
    # https://stackoverflow.com/a/53343430/9225581
    mode = os.RTLD_GLOBAL | os.RTLD_LAZY

    try:
        _IOMP = _CDLL(str(_locate_file("intel_openmp", "libiomp5.so")), mode=mode)
        # _MKL_CORE = _CDLL(str(_locate_file("mkl", "libmkl_core.so.2")), mode=mode)
        # _MKL_INTEL_THREAD = _CDLL(str(_locate_file("mkl", "libmkl_intel_thread.so.2")), mode=mode)
        # _MKL_ILP64 = _CDLL(str(_locate_file("mkl", "libmkl_intel_ilp64.so.2")), mode=mode)

    except _ilm.PackageNotFoundError as e:
        raise ImportError("Could not find the MKL libraries") from e

elif platform.system() == "Windows":
    try:
        for mod, name in [("intel_openmp", "libiomp5md.dll")]:
            loc = _locate_file(mod, name)
            os.add_dll_directory(str(loc.parent))
            # _CDLL(str(loc))
            print(f"Loaded {mod}/{name} from {loc}")

    except _ilm.PackageNotFoundError as e:
        raise ImportError("Could not find the MKL libraries") from e






from ._recombine import *