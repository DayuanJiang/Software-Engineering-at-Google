# This fake implements the FileSystem interface. This interface is also
# used by the real implementation.
class FakeFileSystem(FileSystem):
    def __init__(self):
        # Stores a map of file name to file contents. The files are stored in
        # memory instead of on disk since tests shouldn't need to do disk I/O.
        self._files = {}

    def write_file(self, file_name, contents):
        # Add the file name and contents to the map.
        self._files[file_name] = contents

    def read_file(self, file_name):
        contents = self._files.get(file_name)
        # The real implementation will raise this exception if the
        # file isn't found, so the fake must raise it too.
        if contents is None:
            raise FileNotFoundError(file_name)
        return contents
