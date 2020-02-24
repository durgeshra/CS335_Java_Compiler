



public void testRunWithNonExistentEntry() throws Exception {
    String mp = "DoesNotExist" + File.pathSeparator + MODS_DIR.toString();
    String mid = TEST_MODULE + "/" + MAIN_CLASS;

    
    int exitValue = exec("--module-path", mp, "--module", mid);
    assertTrue(exitValue == 0);
    




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
                    
                    
                    LOG.log(
                            Level.WARNING,
                            NbBundle.getMessage(Util.class,"MSG_BrokenExtension"),
                            new Object[] {
                                f.getName(),
                                extFolder.getAbsolutePath()
                            });
                    continue;
                }
                if (Utilities.isMac() && "._.DS_Store".equals(f.getName())) {  
                    
                    continue;
                }
                FileObject fo = FileUtil.toFileObject(f);
                if (fo == null) {
                    LOG.log(
                            Level.WARNING,
                            "Cannot create FileObject for file: {0} exists: {1}", 
                            new Object[]{
                                f.getAbsolutePath(),
                                f.exists()
                            });
                    continue;
                }
                if (!FileUtil.isArchiveFile(fo)) {
                    
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
 


