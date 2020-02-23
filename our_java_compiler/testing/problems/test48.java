/**
 * Run the test with a non-existent file on the application module path.
 * It should be silently ignored.
 */
public void testRunWithNonExistentEntry() throws Exception {
    String mp = "DoesNotExist" + File.pathSeparator + MODS_DIR.toString();
    String mid = TEST_MODULE + "/" + MAIN_CLASS;

    // java --module-path mods --module $TESTMODULE/$MAINCLASS
    int exitValue = exec("--module-path", mp, "--module", mid);
    assertTrue(exitValue == 0);
    /**
 * Get JRE extension JARs/ZIPs.
 * @param extPath a native-format path for e.g. jre/lib/ext
 * @return a native-format classpath for extension JARs and ZIPs found in it
 */
public static String getExtensions (String extPath) {
    if (extPath == null) {
        return null;
    }
    final StringBuilder sb = new StringBuilder();
    final StringTokenizer tk = new StringTokenizer (extPath, File.pathSeparator);
    while (tk.hasMoreTokens()) {
        File extFolder = FileUtil.normalizeFile(new File(tk.nextToken()));
        File[] files = extFolder.listFiles();
        if (files != null) {
            for (int i = 0; i < files.length; i++) {
                File f = files[i];
                if (!f.exists()) {
                    //May happen, eg. broken link, it is safe to ignore it
                    //since it is an extension directory, but log it.
                    LOG.log(
                            Level.WARNING,
                            NbBundle.getMessage(Util.class,"MSG_BrokenExtension"),
                            new Object[] {
                                f.getName(),
                                extFolder.getAbsolutePath()
                            });
                    continue;
                }
                if (Utilities.isMac() && "._.DS_Store".equals(f.getName())) {  //NOI18N
                    //Ignore Apple temporary ._.DS_Store files in the lib/ext folder
                    continue;
                }
                FileObject fo = FileUtil.toFileObject(f);
                if (fo == null) {
                    LOG.log(
                            Level.WARNING,
                            "Cannot create FileObject for file: {0} exists: {1}", //NOI18N
                            new Object[]{
                                f.getAbsolutePath(),
                                f.exists()
                            });
                    continue;
                }
                if (!FileUtil.isArchiveFile(fo)) {
                    // #42961: Mac OS X has e.g. libmlib_jai.jnilib.
                    continue;
                }
                sb.append(File.pathSeparator);
                sb.append(files[i].getAbsolutePath());
            }
        }
    }
    if (sb.length() == 0) {
        return null;
    }
    return sb.substring(File.pathSeparator.length());
}
 
}
 