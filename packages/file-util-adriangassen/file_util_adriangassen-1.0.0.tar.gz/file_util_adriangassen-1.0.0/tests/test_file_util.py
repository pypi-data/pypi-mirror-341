import pytest

from file_util_adriangassen.cli import cli



class TestFileCreation:
    def test_create_empty_file(self, filepath):
        filepath = filepath()
        assert not filepath.exists()
        cli(["create", str(filepath)])
        assert filepath.exists()

    def test_create_file_with_text(self, filepath, file_contents):
        filepath = filepath()
        contents = file_contents()
        assert not filepath.exists()
        cli(["create", str(filepath), contents])
        assert filepath.exists()
        with open(filepath, "r") as f:
            assert f.read() == contents

    def test_create_empty_file_at_existing_location(self, filepath, file_contents):
        filepath = filepath()
        contents = file_contents()
        with open(filepath, "w") as f:
            f.write(contents)
        assert filepath.exists()
        with open(filepath, "r") as f:
            assert f.read() == contents
        cli(["create", "-c", str(filepath)])
        with open(filepath, "r") as f:
            assert f.read() == ""

    def test_create_file_with_text_at_existing_location(self, filepath, file_contents):
        filepath = filepath()
        original_file_contents = file_contents()
        new_file_contents = file_contents()
        with open(filepath, "w") as f:
            f.write(original_file_contents)
        assert filepath.exists()
        with open(filepath, "r") as f:
            assert f.read() == original_file_contents
        cli(["create", "-c", str(filepath), new_file_contents])
        with open(filepath, "r") as f:
            assert f.read() == new_file_contents


class TestFileCopy:
    def test_copy_file(self, filepath, file_contents):
        orig_filepath = filepath()
        dest_filepath = filepath()
        contents = file_contents()
        with open(orig_filepath, "w") as f:
            f.write(contents)
        cli(["cp", str(orig_filepath), str(dest_filepath)])
        assert dest_filepath.exists()
        with open(dest_filepath, "r") as f:
            assert f.read() == contents

    def test_copy_file_to_existing_location(self, filepath, file_contents):
        orig_filepath = filepath()
        dest_filepath = filepath()
        orig_contents = file_contents()
        existing_file_contents = file_contents()
        with open(orig_filepath, "w") as f:
            f.write(orig_contents)
        with open(dest_filepath, "w") as f:
            f.write(existing_file_contents)
        cli(["cp", "-c", str(orig_filepath), str(dest_filepath)])
        with open(dest_filepath, "r") as f:
            assert f.read() == orig_contents

    def test_exception_thrown_if_src_file_does_not_exist(self, filepath):
        non_existent_filepath = filepath()
        dest_filepath = filepath()
        with pytest.raises(RuntimeError):
            cli(["cp", str(non_existent_filepath), str(dest_filepath)])


class TestFileCombination:
    def test_combine_files(self, filepath, file_contents):
        filepath_1 = filepath()
        filepath_2 = filepath()
        dest_filepath = filepath()
        file_contents_1 = file_contents()
        file_contents_2 = file_contents()
        with open(filepath_1, "w") as f:
            f.write(file_contents_1)
        with open(filepath_2, "w") as f:
            f.write(file_contents_2)
        cli(["cmb", str(filepath_1), str(filepath_2), str(dest_filepath)])
        with open(dest_filepath, "r") as f:
            assert f.read() == file_contents_1 + file_contents_2

    def test_combine_files_to_existing_location(self, filepath, file_contents):
        filepath_1 = filepath()
        filepath_2 = filepath()
        dest_filepath = filepath()
        file_contents_1 = file_contents()
        file_contents_2 = file_contents()
        with open(filepath_1, "w") as f:
            f.write(file_contents_1)
        with open(filepath_2, "w") as f:
            f.write(file_contents_2)
        dest_filepath.touch()
        cli(["cmb", "-c", str(filepath_1), str(filepath_2), str(dest_filepath)])
        with open(dest_filepath, "r") as f:
            assert f.read() == file_contents_1 + file_contents_2

    def test_combine_files_one_does_not_exist(self, filepath):
        existing_filepath = filepath()
        non_existent_filepath = filepath()
        dest_filepath = filepath()
        existing_filepath.touch()
        with pytest.raises(RuntimeError):
            cli(["cmb", str(existing_filepath), str(non_existent_filepath), str(dest_filepath)])

    def test_combine_files_both_do_not_exist(self, filepath):
        non_existent_filepath_1 = filepath()
        non_existent_filepath_2 = filepath()
        dest_filepath = filepath()
        with pytest.raises(RuntimeError):
            cli(["cmb", str(non_existent_filepath_1), str(non_existent_filepath_2), str(dest_filepath)])


class TestFileDeletion:
    def test_delete_file(self, filepath):
        filepath = filepath()
        filepath.touch()
        assert filepath.exists()
        cli(["rm", "-c", str(filepath)])
        assert not filepath.exists()

    def test_delete_file_that_does_not_exist(self, filepath):
        non_existent_filepath = filepath()
        with pytest.raises(Exception):
            cli(["rm", "-c", str(non_existent_filepath)])

    def test_exception_when_deleting_directory(self, filepath):
        directory_path = filepath()
        directory_path.mkdir()
        with pytest.raises(Exception):
            cli(["rm", "-c", str(directory_path)])
