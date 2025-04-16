"""
application environment updater
===============================

this portion is providing helper functions to set up, prepare and/or upgrade packages, resources,
:ref:`config-variables`, like :ref:`application status` or user preferences of your app.


updater check functions
-----------------------

automatically copy, move or update any files on the destination machine with the help of the helper functions
:func:`check_copies` and :func:`check_moves`. these functions can be restricted to copy/move only the files that
are not exist in the destination folder (while protecting already existing files from being overwritten).

if your app need to execute a Python pre-app-run-script on every startup of your application, then simply call
the function :func:`check_local_pre_app_runs`, which will check if an importable and executable module
with the name specified by the :data:`PRE_APP_MODULE_NAME` cpmstamt exists and contains a function with the
name `run_updater`.

the function :func:`check_local_updates` checks if a (newly added) update script/module with the name specified by the
:data:`UPDATER_MODULE_NAME` constant exists, and if yes, it imports this module and executes the function `run_updater`
declared in it. after the successful execution the update module will be deleted. this one-time execution feature can
be used e.g. to deploy and configure more complex updates, like e.g. to adapt an existing app installation,
respectively their resources and settings.

the function :func:`check_all` combines all the above update checks and executions.

..hint: more info on the update helper functions provided by this portion, you find in their respective doc-strings.

any of these update check helper functions has to be imported and executed before the loading and initialization
of the updatable code modules and resources, e.g. like so::

    from ae.updater import check_all
    check_all()

    from updatable_app_package import ...
    ...
    initialize_updatable_app_resources()

if your app only has to support one or some of the update/pre-app-run features then replace in the above code example
the :func:`check_all` with the needed check function(s).

.. note::
    the :mod:`ae.core` is calling :func:`check_all` automatically on start of your console or GUI app
    on initialization of the main app :class:`~ae.core.AppBase` class instance.

    additionally it extends the :data:`~ae.paths.PATH_PLACEHOLDERS` with OS-specific
    system paths (like e.g. {downloads}).

    to use OS-specific :data:`~ae.paths.PATH_PLACEHOLDERS` ids as folder argument values for apps not based on the
    :mod:`ae.core` portion, the function :func:`~ae.paths.add_common_storage_paths` has to be explicitly called.


data-driven file copy/move operations
-------------------------------------

the file copy and move operations provided by :func:`check_copies`, :func:`check_moves` and :func:`check_all`
are highly parameterizable.

you can specify source and destination paths for all of them via their function arguments. relative folder paths
will be relative to the current working directory ({cwd}).

additionally, the destination path and the OS where the copy/move operation has to be processed can be tweaked
via two optional arguments specified in the name of the source folder.

in order to specify individual destination OS and path, append the string :data:`UPDATER_ARGS_SEP` to the folder name
directly followed by the argument name and value.

the argument name string :data:`UPDATER_ARG_OS_PLATFORM` followed by the :data:`platform id <ae.base.os_platform>`
restricts the copy/move operations for a certain OS.

to overwrite the default destination folder/path of the copy/move operations for a source folder, put the string
:data:`UPDATER_ARG_DST_PATH` as argument name, followed by the :func:`defused <ae.base.defuse>` destination path
string as argument value. this argument value is either a relative/absolute path string or a
:data:`~ae.paths.PATH_PLACEHOLDERS` id.

for example, the files in a folder with the name `ae_updater_moves___OnOS__android`
will only be moved to the destination folder if the app is running on Android OS.
"""
import os
from typing import List

from ae.base import PACKAGE_INCLUDE_FILES_PREFIX, PY_EXT, dedefuse, module_attr, os_platform    # type: ignore
from ae.paths import copy_files, move_files, coll_folders, Collector                            # type: ignore


__version__ = '0.3.16'


COPIES_SRC_FOLDER_NAME = PACKAGE_INCLUDE_FILES_PREFIX + 'updater_copies'            #: copies if not exists dir name
COPY_OVER_SRC_FOLDER_NAME = PACKAGE_INCLUDE_FILES_PREFIX + 'updater_over_copies'    #: overwrite copies dir name
MOVES_SRC_FOLDER_NAME = PACKAGE_INCLUDE_FILES_PREFIX + 'updater_moves'              #: dir name for moves
MOVE_OVER_SRC_FOLDER_NAME = PACKAGE_INCLUDE_FILES_PREFIX + 'updater_over_moves'     #: overwrite moves dir name

UPDATER_ARGS_SEP = '___'                                                            #: folder-name-arg separator
UPDATER_ARG_DST_PATH = 'ToPath__'                                                   #: dst-path folder-name-arg
UPDATER_ARG_OS_PLATFORM = 'OnOS__'                                                  #: platform folder-name-arg

PRE_APP_MODULE_NAME = PACKAGE_INCLUDE_FILES_PREFIX + 'pre_app_run'                  #: pre-app-run module name
UPDATER_MODULE_NAME = PACKAGE_INCLUDE_FILES_PREFIX + 'updater'                      #: module name of updater


def check_all(copy_src_path: str = COPIES_SRC_FOLDER_NAME, copy_over_src_path: str = COPY_OVER_SRC_FOLDER_NAME,
              move_src_path: str = MOVES_SRC_FOLDER_NAME, move_over_src_path: str = MOVE_OVER_SRC_FOLDER_NAME,
              dst_folder: str = "{usr}") -> List[str]:
    """ check all outstanding scripts to be executed and files to be moved/overwritten.

    :param copy_src_path:       path to source folder/directory where the files get copied from. if not specified
                                or if you pass an empty string then :data:`COPIES_SRC_FOLDER_NAME` will be used.
    :param copy_over_src_path:  path to source folder/directory where the files get copied from and overwritten to.
                                if not specified then :data:`COPY_OVER_SRC_FOLDER_NAME` will be used.
    :param move_src_path:       path to source folder/directory where the files get moved from. if not specified
                                or if you pass an empty string then :data:`MOVES_SRC_FOLDER_NAME` will be used.
    :param move_over_src_path:  path to source folder/directory where the files get moved from and overwritten to.
                                if not specified then :data:`MOVE_OVER_SRC_FOLDER_NAME` will be used.
    :param dst_folder:          path to destination folder/directory where the files get moved to. if not specified
                                or if you pass an empty string then the user data/preferences path ({usr}) will be used.
                                this argument may get overwritten for source folder names specifying the
                                data-driven :data:`UPDATER_ARG_DST_PATH` argument.
    :return:                    list of processed (copied, moved or overwritten) files, with their destination path.
    """
    check_local_updates()

    check_local_pre_app_runs()

    processed = []
    processed += check_copies(src_path=copy_src_path, dst_path=dst_folder)
    processed += check_copies(src_path=copy_over_src_path, dst_path=dst_folder, overwrite=True)
    processed += check_moves(src_path=move_src_path, dst_path=dst_folder)
    processed += check_moves(src_path=move_over_src_path, dst_path=dst_folder, overwrite=True)

    return processed


def check_copies(src_path: str = COPIES_SRC_FOLDER_NAME, dst_path: str = "{usr}", overwrite: bool = False) -> List[str]:
    """ check on new or missing files to be copied from src_folder to the dst_folder.

    :param src_path:            path to source folder/directory where the files get copied from. If not specified then
                                :data:`COPIES_SRC_FOLDER_NAME` will be used.
    :param dst_path:            path to destination folder/directory where the files get copied to. If not specified
                                or if you pass an empty string then the user data/preferences path ({usr}) will be used.
                                this argument may get overwritten for source folder names specifying the
                                data-driven :data:`UPDATER_ARG_DST_PATH` argument.
    :param overwrite:           pass True to overwrite existing files in the destination folder/directory. on False the
                                files will only get copied if they not exist in the destination.
    :return:                    list of copied files, with their destination path.
    """
    processed = []
    for src_folder, dst_folder in source_destination_paths(src_path, dst_path):
        processed += copy_files(src_folder, dst_folder, overwrite=overwrite)
    return processed


def check_moves(src_path: str = MOVES_SRC_FOLDER_NAME, dst_path: str = "{usr}", overwrite: bool = False) -> List[str]:
    """ check on missing files to be moved from src_folder to the dst_folder.

    :param src_path:            path to source folder/directory where the files get moved from. If not specified then
                                :data:`MOVES_SRC_FOLDER_NAME` will be used. Please note that the source folder itself
                                will neither be moved nor removed (but will be empty after the operation finished).
    :param dst_path:            path to destination folder/directory where the files get moved to. If not specified
                                or if you pass an empty string then the user data/preferences path ({usr}) will be used.
                                this argument may get overwritten for source folder names specifying the
                                data-driven :data:`UPDATER_ARG_DST_PATH` argument.
    :param overwrite:           pass True to overwrite existing files in the destination folder/directory. on False the
                                files will only get moved if they not exist in the destination.
    :return:                    list of moved files, with their destination path.
    """
    processed = []
    for src_folder, dst_folder in source_destination_paths(src_path, dst_path):
        processed += move_files(src_folder, dst_folder, overwrite=overwrite)
    return processed


def check_local_updates() -> bool:
    """ check if ae_updater script exists in the current working directory to be executed and deleted.

    .. note:
        if the module :data:`UPDATER_MODULE_NAME` exists, is declaring a :func:`run_updater` function, which
        is returning a non-empty return value (evaluating as boolean True), then the module will be
        automatically deleted after the execution of the function.

    :return:                    return value of the executed `run_updater` function (if the module
                                :data:`UPDATER_MODULE_NAME` can be loaded/imported and contains this function)
                                else False.
    """
    func = module_attr(UPDATER_MODULE_NAME, attr_name='run_updater')
    ret = func() if func else False
    if ret:
        os.remove(UPDATER_MODULE_NAME + PY_EXT)
    return ret


def check_local_pre_app_runs() -> bool:
    """ check if a pre-app-run-script exists in the current working directory to be executed on/before app startup.

    :return:                    return value of the executed `run_updater` function (if the module
                                :data:`PRE_APP_MODULE_NAME` can be loaded/imported and contains this function)
                                else False.
    """
    func = module_attr(PRE_APP_MODULE_NAME, attr_name='run_updater')
    return func() if func else False


def source_destination_paths(src_folder_prefix: str, default_dst_folder: str) -> list[tuple[str, str]]:
    """ collect source folders and determine destination folders for each of them.

    :param src_folder_prefix:   source folder name without folder-name-args.
    :param default_dst_folder:  destination folder default (if not specified in folder-name-args).
    :return:                    list of source and destination folders to process.
    """
    if src_folder_prefix.endswith('/'):
        src_folder_prefix = src_folder_prefix[:-1]
    paths = []

    coll = Collector(item_collector=coll_folders)
    coll.collect('{cwd}', append=src_folder_prefix + '*', only_first_of='prefix')
    for src_path in coll.paths:
        _folder_prefix, *folder_name_args = src_path.split(UPDATER_ARGS_SEP)
        dst_path = default_dst_folder
        process_folder = True
        for arg_name_val in folder_name_args:
            if arg_name_val.startswith(UPDATER_ARG_DST_PATH):
                dst_path = dedefuse(arg_name_val[len(UPDATER_ARG_DST_PATH):])
            elif arg_name_val.startswith(UPDATER_ARG_OS_PLATFORM):
                process_folder = arg_name_val[len(UPDATER_ARG_OS_PLATFORM):] == os_platform
        if process_folder:
            paths.append((src_path, dst_path))

    return paths
