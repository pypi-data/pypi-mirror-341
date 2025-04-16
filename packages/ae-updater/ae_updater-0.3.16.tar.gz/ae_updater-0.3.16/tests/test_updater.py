""" unit tests for ae.updater portion. """
import os
import shutil
import tempfile
from typing import cast
from unittest.mock import patch

import pytest

from ae.base import INI_EXT, defuse, in_wd, norm_path, write_file
from ae.files import read_file_text
from ae.paths import PATH_PLACEHOLDERS, normalize, user_data_path
from ae.updater import (
    COPIES_SRC_FOLDER_NAME, COPY_OVER_SRC_FOLDER_NAME, MOVES_SRC_FOLDER_NAME, MOVE_OVER_SRC_FOLDER_NAME,
    PRE_APP_MODULE_NAME, UPDATER_ARG_DST_PATH, UPDATER_ARG_OS_PLATFORM, UPDATER_ARGS_SEP, UPDATER_MODULE_NAME,
    check_copies, check_moves, check_local_updates, check_local_pre_app_runs, check_all)


FILE0 = "app" + INI_EXT
CONTENT0 = "TEST FILE0 CONTENT"
OLD_CONTENT0 = "OLD/LOCKED FILE0 CONTENT"

DIR1 = 'app_dir'
FILE1 = 'app.png'
CONTENT1 = "TEST FILE1 CONTENT"


@pytest.fixture(params=[COPIES_SRC_FOLDER_NAME,
                        COPY_OVER_SRC_FOLDER_NAME,
                        MOVES_SRC_FOLDER_NAME,
                        MOVE_OVER_SRC_FOLDER_NAME])
def files_to_upd(request, tmp_path):
    """ create test files in source directory to be updated (copied, moved and/or overwritten). """
    src_dir = tmp_path / request.param
    src_dir.mkdir()

    src_file0 = src_dir / FILE0
    src_file0.write_text(CONTENT0)

    src_sub_dir = src_dir / DIR1
    src_sub_dir.mkdir()
    src_file1 = src_sub_dir / FILE1
    src_file1.write_text(CONTENT1)

    yield str(src_file0), str(src_file1)

    # tmp_path/dst_dir1 will be removed automatically by pytest - leaving the last three temporary directories
    # .. see https://docs.pytest.org/en/latest/tmp_path.html#the-default-base-temporary-directory
    # shutil.rmtree(tmp_path)


def _create_file_at_destination(dst_folder):
    """ create file0 at destination folder to block move. """
    dst_file = cast(str, os.path.join(dst_folder, FILE0))
    write_file(dst_file, OLD_CONTENT0)
    return dst_file


class TestCheckAll:
    def test_nothing_to_do(self):
        with tempfile.TemporaryDirectory() as tmp_dir, in_wd(tmp_dir):
            check_all()

    def test_file_copies_to_user_dir_via_check_all(self, files_to_upd):
        src_dir = os.path.dirname(files_to_upd[0]) + "/"    # added slash to test removal for source folder name args
        dst_dir = user_data_path()

        copied = []
        try:
            copied += check_all(copy_src_path=src_dir)

            for src_file_path in files_to_upd:
                assert os.path.exists(src_file_path)
                assert os.path.exists(os.path.join(dst_dir, os.path.relpath(src_file_path, src_dir)))
        finally:
            for dst_file_path in copied:
                dst_path = os.path.relpath(dst_file_path, dst_dir)
                if os.path.exists(dst_file_path):
                    os.remove(dst_file_path)
                    if dst_path != os.path.basename(dst_file_path):
                        shutil.rmtree(os.path.dirname(dst_file_path))

    def test_file_copy_over_to_user_dir_via_check_all(self, files_to_upd):
        src_dir = os.path.dirname(files_to_upd[0])
        dst_dir = user_data_path()

        moved = []
        try:
            moved += check_all(copy_over_src_path=src_dir)

            for src_file_path in files_to_upd:
                assert os.path.exists(src_file_path)
                assert os.path.exists(os.path.join(dst_dir, os.path.relpath(src_file_path, src_dir)))
        finally:
            for dst_file_path in moved:
                dst_path = os.path.relpath(dst_file_path, dst_dir)
                if os.path.exists(dst_file_path):
                    os.remove(dst_file_path)
                    if dst_path != os.path.basename(dst_file_path):
                        shutil.rmtree(os.path.dirname(dst_file_path))

    def test_file_moves_to_user_dir_via_check_all(self, files_to_upd):
        src_dir = os.path.dirname(files_to_upd[0])
        dst_dir = user_data_path()

        moved = []
        try:
            moved += check_all(move_src_path=src_dir)

            for src_file_path in files_to_upd:
                assert not os.path.exists(src_file_path)
                assert os.path.exists(os.path.join(dst_dir, os.path.relpath(src_file_path, src_dir)))
        finally:
            for dst_file_path in moved:
                dst_path = os.path.relpath(dst_file_path, dst_dir)
                if os.path.exists(dst_file_path):
                    os.remove(dst_file_path)
                    if dst_path != os.path.basename(dst_file_path):
                        shutil.rmtree(os.path.dirname(dst_file_path))

    def test_file_move_over_to_user_dir_via_check_all(self, files_to_upd):
        src_dir = os.path.dirname(files_to_upd[0])
        dst_dir = user_data_path()

        moved = []
        try:
            moved += check_all(move_over_src_path=src_dir)

            for src_file_path in files_to_upd:
                assert not os.path.exists(src_file_path)
                assert os.path.exists(os.path.join(dst_dir, os.path.relpath(src_file_path, src_dir)))
        finally:
            for dst_file_path in moved:
                dst_path = os.path.relpath(dst_file_path, dst_dir)
                if os.path.exists(dst_file_path):
                    os.remove(dst_file_path)
                    if dst_path != os.path.basename(dst_file_path):
                        shutil.rmtree(os.path.dirname(dst_file_path))

    def test_folder_name_args(self, tmp_path):
        dest = str(tmp_path / 'any_destination_folder')

        src_dir0 = tmp_path / MOVES_SRC_FOLDER_NAME
        src_dir0.mkdir()
        src_fil0 = src_dir0 / "tst_updater_usr_dest_file.zyx"
        src_fil0.write_text(CONTENT0)
        usr_dst_fil0 = os.path.join(normalize('{usr}'), os.path.basename(src_fil0))

        src_dir1 = tmp_path / (MOVES_SRC_FOLDER_NAME + UPDATER_ARGS_SEP + UPDATER_ARG_DST_PATH + defuse(dest))
        src_dir1.mkdir()
        src_fil1 = src_dir1 / "with_dest_path"
        src_fil1.write_text(CONTENT0)

        platform = 'testPlatform'
        src_dir2 = str(src_dir1) + UPDATER_ARGS_SEP + UPDATER_ARG_OS_PLATFORM + platform
        os.mkdir(src_dir2)
        src_fil2 = os.path.join(src_dir2, "os_specific_file.{apk_ext}")
        write_file(src_fil2, CONTENT0)

        PATH_PLACEHOLDERS['downloads'] = dest
        src_dir3 = tmp_path / (MOVES_SRC_FOLDER_NAME + UPDATER_ARGS_SEP + UPDATER_ARG_DST_PATH + defuse('{downloads}'))
        src_dir3.mkdir()
        src_fil3 = src_dir3 / "tst_updater_downloads_dest_file.{apk_ext}"
        src_fil3.write_text(CONTENT0)

        try:
            # abs src_dir0 path (to overwrite cwd) and also used as prefix for the other 2 dirs with folder-name-args
            processed = check_all(move_src_path=str(src_dir0))

            assert len(processed) == 3
            assert any(_.endswith(os.path.basename(src_fil0)) for _ in processed)
            assert any(_.endswith(os.path.basename(src_fil1)) for _ in processed)
            assert any(_.endswith(os.path.basename(src_fil3)) for _ in processed)
            for pro in processed:
                assert os.path.isfile(pro)

            assert not os.path.isfile(src_fil0)
            assert not os.path.isfile(src_fil1)
            assert os.path.isfile(src_fil2)     # NOT moved because no platform match
            assert not os.path.isfile(src_fil3)

            assert os.path.isfile(usr_dst_fil0)
            assert os.path.isfile(os.path.join(dest, os.path.basename(src_fil1)))
            assert not os.path.isfile(os.path.join(dest, os.path.basename(src_fil2)))
            usr_dst_fil3 = os.path.join(normalize('{downloads}'), os.path.basename(src_fil3))
            assert os.path.isfile(usr_dst_fil3)
            # no need to clean up {downloads} from test-destination-fil3 because it got redirected to dest temp test dir

            with patch('ae.updater.os_platform', platform):
                processed = check_all(move_src_path=str(src_dir0))

            assert len(processed) == 1
            for pro in processed:
                assert os.path.isfile(pro)

            assert any(_.endswith(os.path.basename(src_fil2)) for _ in processed)

            assert not os.path.isfile(src_fil0)
            assert not os.path.isfile(src_fil1)
            assert not os.path.isfile(src_fil2)  # NOW moved because of platform match
            assert not os.path.isfile(src_fil3)

            assert os.path.isfile(os.path.join(dest, os.path.basename(src_fil2)))

        finally:
            if os.path.isfile(usr_dst_fil0):
                os.remove(usr_dst_fil0)     # clean up {usr} from test-destination-fil0 in ~/.config

    def test_updater_via_check_all(self, created_run_updater):
        assert os.path.exists(created_run_updater)
        check_all()
        assert not os.path.exists(created_run_updater)

    def test_pre_app_runs_via_check_all(self, created_pre_app_run):
        assert os.path.exists(created_pre_app_run)
        check_all()
        assert os.path.exists(created_pre_app_run)


class TestFileUpdates:
    def test_copies_over_to_parent_dir(self, files_to_upd):
        src_dir = os.path.dirname(files_to_upd[0])
        dst_dir = os.path.join(src_dir, '..')
        for src_file_path in files_to_upd:
            assert os.path.exists(src_file_path)
            assert not os.path.exists(os.path.join(dst_dir, os.path.relpath(src_file_path, src_dir)))

        copied_to_files = check_copies(src_path=src_dir, dst_path=dst_dir, overwrite=True)

        for src_file_path in files_to_upd:
            assert norm_path(os.path.join(dst_dir, os.path.relpath(src_file_path, src_dir))) in copied_to_files
        if COPY_OVER_SRC_FOLDER_NAME in src_dir:
            for src_file_path in files_to_upd:
                assert os.path.exists(src_file_path)
                assert os.path.exists(os.path.join(dst_dir, os.path.relpath(src_file_path, src_dir)))

    def test_copies_over_to_parent_dir_unblocked(self, files_to_upd):
        src_dir = os.path.dirname(files_to_upd[0])
        dst_dir = os.path.join(src_dir, '..')
        dst_block_file = _create_file_at_destination(dst_dir)
        assert os.path.exists(dst_block_file)
        for src_file_path in files_to_upd:
            assert os.path.exists(src_file_path)
            dst_file = os.path.join(dst_dir, os.path.relpath(src_file_path, src_dir))
            assert dst_file == dst_block_file or not os.path.exists(dst_file)

        copied_to_files = check_copies(src_path=src_dir, dst_path=dst_dir, overwrite=True)

        for src_file_path in files_to_upd:
            assert norm_path(os.path.join(dst_dir, os.path.relpath(src_file_path, src_dir))) in copied_to_files
        if COPY_OVER_SRC_FOLDER_NAME in src_dir:
            assert os.path.exists(files_to_upd[0])
            dst_file = os.path.join(dst_dir, os.path.relpath(files_to_upd[0], src_dir))
            assert os.path.exists(dst_file)
            assert read_file_text(dst_file) == CONTENT0

            assert os.path.exists(files_to_upd[1])
            dst_file = os.path.join(dst_dir, os.path.relpath(files_to_upd[1], src_dir))
            assert os.path.exists(dst_file)
            assert read_file_text(dst_file) == CONTENT1

    def test_copies_to_parent_dir(self, files_to_upd):
        src_dir = os.path.dirname(files_to_upd[0])
        dst_dir = os.path.join(src_dir, '..')
        for src_file_path in files_to_upd:
            assert os.path.exists(src_file_path)
            assert not os.path.exists(os.path.join(dst_dir, os.path.relpath(src_file_path, src_dir)))

        copied_files = check_copies(src_path=src_dir, dst_path=dst_dir)

        for src_file_path in files_to_upd:
            assert norm_path(os.path.join(dst_dir, os.path.relpath(src_file_path, src_dir))) in copied_files
        if COPIES_SRC_FOLDER_NAME in src_dir:
            for src_file_path in files_to_upd:
                assert os.path.exists(src_file_path)
                assert os.path.exists(os.path.join(dst_dir, os.path.relpath(src_file_path, src_dir)))

    def test_copies_to_parent_dir_blocked(self, files_to_upd):
        src_dir = os.path.dirname(files_to_upd[0])
        dst_dir = os.path.join(src_dir, '..')
        dst_block_file = _create_file_at_destination(dst_dir)
        assert os.path.exists(dst_block_file)
        for src_file_path in files_to_upd:
            assert os.path.exists(src_file_path)
            dst_file = os.path.join(dst_dir, os.path.relpath(src_file_path, src_dir))
            assert dst_file == dst_block_file or not os.path.exists(dst_file)

        assert len(check_copies(src_path=src_dir, dst_path=dst_dir)) == 1

        if COPIES_SRC_FOLDER_NAME in src_dir:
            assert os.path.exists(files_to_upd[0])
            assert read_file_text(files_to_upd[0]) == CONTENT0
            dst_file = os.path.join(dst_dir, os.path.relpath(files_to_upd[0], src_dir))
            assert os.path.exists(dst_file)
            assert read_file_text(dst_file) == OLD_CONTENT0

            assert os.path.exists(files_to_upd[1])
            dst_file = os.path.join(dst_dir, os.path.relpath(files_to_upd[1], src_dir))
            assert os.path.exists(dst_file)
            assert read_file_text(dst_file) == CONTENT1

    def test_moves_over_to_parent_dir(self, files_to_upd):
        src_dir = os.path.dirname(files_to_upd[0])
        dst_dir = os.path.join(src_dir, '..')
        for src_file_path in files_to_upd:
            assert os.path.exists(src_file_path)
            assert not os.path.exists(os.path.join(dst_dir, os.path.relpath(src_file_path, src_dir)))

        moved_to_files = check_moves(src_path=src_dir, dst_path=dst_dir, overwrite=True)

        for src_file_path in files_to_upd:
            assert norm_path(os.path.join(dst_dir, os.path.relpath(src_file_path, src_dir))) in moved_to_files
        if MOVE_OVER_SRC_FOLDER_NAME in src_dir:
            for src_file_path in files_to_upd:
                assert not os.path.exists(src_file_path)
                assert os.path.exists(os.path.join(dst_dir, os.path.relpath(src_file_path, src_dir)))

    def test_moves_over_to_parent_dir_unblocked(self, files_to_upd):
        src_dir = os.path.dirname(files_to_upd[0])
        dst_dir = os.path.join(src_dir, '..')
        dst_block_file = _create_file_at_destination(dst_dir)
        assert os.path.exists(dst_block_file)
        for src_file_path in files_to_upd:
            assert os.path.exists(src_file_path)
            dst_file = os.path.join(dst_dir, os.path.relpath(src_file_path, src_dir))
            assert dst_file == dst_block_file or not os.path.exists(dst_file)

        moved_to_files = check_moves(src_path=src_dir, dst_path=dst_dir, overwrite=True)

        for src_file_path in files_to_upd:
            assert norm_path(os.path.join(dst_dir, os.path.relpath(src_file_path, src_dir))) in moved_to_files
        if MOVE_OVER_SRC_FOLDER_NAME in src_dir:
            assert not os.path.exists(files_to_upd[0])
            dst_file = os.path.join(dst_dir, os.path.relpath(files_to_upd[0], src_dir))
            assert os.path.exists(dst_file)
            assert read_file_text(dst_file) == CONTENT0

            assert not os.path.exists(files_to_upd[1])
            dst_file = os.path.join(dst_dir, os.path.relpath(files_to_upd[1], src_dir))
            assert os.path.exists(dst_file)
            assert read_file_text(dst_file) == CONTENT1

    def test_moves_to_parent_dir(self, files_to_upd):
        src_dir = os.path.dirname(files_to_upd[0])
        dst_dir = os.path.join(src_dir, '..')
        for src_file_path in files_to_upd:
            assert os.path.exists(src_file_path)
            assert not os.path.exists(os.path.join(dst_dir, os.path.relpath(src_file_path, src_dir)))

        moved_to_files = check_moves(src_path=src_dir, dst_path=dst_dir)

        for src_file_path in files_to_upd:
            assert norm_path(os.path.join(dst_dir, os.path.relpath(src_file_path, src_dir))) in moved_to_files
        if MOVES_SRC_FOLDER_NAME in src_dir:
            for src_file_path in files_to_upd:
                assert not os.path.exists(src_file_path)
                assert os.path.exists(os.path.join(dst_dir, os.path.relpath(src_file_path, src_dir)))

    def test_moves_to_parent_dir_blocked(self, files_to_upd):
        src_dir = os.path.dirname(files_to_upd[0])
        dst_dir = os.path.join(src_dir, '..')
        dst_block_file = _create_file_at_destination(dst_dir)
        assert os.path.exists(dst_block_file)
        for src_file_path in files_to_upd:
            assert os.path.exists(src_file_path)
            dst_file = os.path.join(dst_dir, os.path.relpath(src_file_path, src_dir))
            assert dst_file == dst_block_file or not os.path.exists(dst_file)

        assert len(check_moves(src_path=src_dir, dst_path=dst_dir)) == 1

        if MOVES_SRC_FOLDER_NAME in src_dir:
            assert os.path.exists(files_to_upd[0])
            assert read_file_text(files_to_upd[0]) == CONTENT0
            dst_file = os.path.join(dst_dir, os.path.relpath(files_to_upd[0], src_dir))
            assert os.path.exists(dst_file)
            assert read_file_text(dst_file) == OLD_CONTENT0

            assert not os.path.exists(files_to_upd[1])
            dst_file = os.path.join(dst_dir, os.path.relpath(files_to_upd[1], src_dir))
            assert os.path.exists(dst_file)
            assert read_file_text(dst_file) == CONTENT1


def _create_module(tmp_dir, module_name):
    fn = cast(str, os.path.join(tmp_dir, module_name + '.py'))
    write_file(fn, """def run_updater():\n    return True""")

    return fn


@pytest.fixture
def created_run_updater():
    """ create test module to be executed. """
    with tempfile.TemporaryDirectory() as tmp_dir, in_wd(tmp_dir):
        yield _create_module(tmp_dir, UPDATER_MODULE_NAME)


@pytest.fixture
def created_pre_app_run():
    """ create test module to be executed. """
    with tempfile.TemporaryDirectory() as tmp_dir, in_wd(tmp_dir):
        yield _create_module(tmp_dir, PRE_APP_MODULE_NAME)


class TestRunUpdater:
    def test_updater(self, created_run_updater):
        assert os.path.exists(created_run_updater)
        check_local_updates()
        assert not os.path.exists(created_run_updater)

    def test_pre_app_runs(self, created_pre_app_run):
        assert os.path.exists(created_pre_app_run)
        check_local_pre_app_runs()
        assert os.path.exists(created_pre_app_run)
