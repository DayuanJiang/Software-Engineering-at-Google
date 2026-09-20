// This fake implements the FileSystem interface. This interface is also
// used by the real implementation.
public class FakeFileSystem implements FileSystem {
    // Stores a map of file name to file contents. The files are stored in
    // memory instead of on disk since tests shouldn’t need to do disk I/O.
    private Map < String, String > files = new HashMap< > ();
    
    @Override
    public void writeFile(String fileName, String contents) {
        // Add the file name and contents to the map.
        files.add(fileName, contents);
    }
  
    @Override
    public String readFile(String fileName) {
        String contents = files.get(fileName);
        // The real implementation will throw this exception if the
        // file isn’t found, so the fake must throw it too.
        if(contents == null) {
            throw new FileNotFoundException(fileName);
        }
        return contents;
    }
}
