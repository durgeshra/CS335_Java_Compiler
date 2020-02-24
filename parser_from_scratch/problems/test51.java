/*
*
 * Run the test with a non-existent file on the application module path.
 * It should be silently ignored.
 */
public void testRunWithNonExistentEntry() throws Exception {
    String mp = "DoesNotExist" + File.pathSeparator + MODS_DIR.toString();
    String mid = TEST_MODULE + "/" + MAIN_CLASS;

    // java --module-path mods --module $TESTMODULE/$MAINCLASS
    int exitValue = exec("--module-path", mp, "--module", mid);
    assertTrue(exitValue == 0);
}
 private static void addPath(
    @NullAllowed final String path,
    @NonNull Collection<? super FileObject> collector,
    final boolean modulepath) {
    if (path != null) {
        final StringTokenizer tok = new StringTokenizer(path, File.pathSeparator);
        while (tok.hasMoreTokens()) {
            final String binrootS = tok.nextToken();
            final File f = FileUtil.normalizeFile(new File(binrootS));
            final Collection<? extends File> toAdd = modulepath ?
                    collectModules(f) :
                    Collections.singleton(f);
            toAdd.forEach((e) -> {
                final URL binroot = FileUtil.urlForArchiveOrDir(f);
                if (binroot != null) {
                    final FileObject[] someRoots = SourceForBinaryQuery.findSourceRoots(binroot).getRoots();
                    Collections.addAll(collector, someRoots);
                }
            });
        }
    }
}
 /**
 * Returns true if the specified location is in the JVM classpath. This may ignore additions to
 * the classpath that are not reflected by the value in
 * <code>System.getProperty("java.class.path")</code>.
 * 
 * @param location the directory or jar URL to test for
 * @return true if location is in the JVM classpath
 * @throws MalformedURLException
 */
public static boolean isInClassPath(URL location) throws MalformedURLException {
  String classPath = System.getProperty("java.class.path");
  StringTokenizer st = new StringTokenizer(classPath, File.pathSeparator);
  while (st.hasMoreTokens()) {
    String path = st.nextToken();
    if (location.equals(new File(path).toURI().toURL())) {
      return true;
    }
  }
  return false;
}
 