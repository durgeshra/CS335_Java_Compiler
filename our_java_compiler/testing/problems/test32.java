/**
 * <p>
 * @return the java.ext.dirs property as a list of directory
 * </p>
 */
private static File[] getExtDirs() {
    String s = java.security.AccessController.doPrivileged(
            new sun.security.action.GetPropertyAction("java.ext.dirs"));

    File[] dirs;
    if (s != null) {
        StringTokenizer st =
            new StringTokenizer(s, File.pathSeparator);
        int count = st.countTokens();
        debug("getExtDirs count " + count);
        dirs = new File[count];
        for (int i = 0; i < count; i++) {
            dirs[i] = new File(st.nextToken());
            debug("getExtDirs dirs["+i+"] "+ dirs[i]);
        }
    } else {
        dirs = new File[0];
        debug("getExtDirs dirs " + dirs);
    }
    debug("getExtDirs dirs.length " + dirs.length);
    return dirs;
}
 