import os
import sys
from os.path import join

import keopscore
from keopscore.config.config import keops_cache_folder, default_build_path, _build_path


def set_build_folder(
    path, write_save_file, reset_all
):
    r"""
    Set the build folder for KeOps.

    :param path: (str) path to build folder
    :param write_save_file: (bool) write the new build folder path name in the `keops_cache_folder/build_folder_location.txt`
        file. To be used with `set_build_folder(path=None, read_save_file=True)`
    :param reset_all: (bool) flush keops cache (.pkl files)
    :return:
    """

    # if path is not given, we either read the save file or use the default build path
    save_file = join(keops_cache_folder, "build_folder_location.txt")

    if (path is None) and os.path.isfile(save_file):
        f = open(save_file, "r")
        path = f.read()
        f.close()
    elif (path is None):
        path = default_build_path

    path = os.path.expanduser(path)

    # create the folder if not yet done
    os.makedirs(path, exist_ok=True)

    # _build_path contains the current build folder path (or None if not yet set). We need
    # to remove this _build_path from the sys.path, replace the value of _build_path
    # and update the sys.path
    global _build_path
    if _build_path in sys.path:
        sys.path.remove(_build_path)
    _build_path = path
    sys.path.append(path)

    # saving the location of the build path in a file
    if write_save_file:
        f = open(save_file, "w")
        f.write(path)
        f.close()

    # reset all cached formulas if needed
    if reset_all:
        keopscore.get_keops_dll.get_keops_dll.reset(new_save_folder=_build_path)
        if keopscore.config.config.use_cuda:
            from keopscore.binders.nvrtc.Gpu_link_compile import (
                Gpu_link_compile,
                jit_compile_dll,
            )

        if not os.path.exists(jit_compile_dll()):
            Gpu_link_compile.compile_jit_compile_dll()


def get_build_folder():
    return _build_path
