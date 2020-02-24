static void testSearchPaths() {
    List<String> i, x, iF, xF;
    i = x = iF = xF = new ArrayList<>();

    SourceLocation dir1 = new SourceLocation(Paths.get("dir1"), i, x);
    SourceLocation dir2 = new SourceLocation(Paths.get("dir2"), i, x);
    String dir1_PS_dir2 = "dir1" + File.pathSeparator + "dir2";

    Options options = Options.parseArgs("--source-path", dir1_PS_dir2);
    assertEquals(options.getSourceSearchPaths(), Arrays.asList(dir1, dir2));

    options = Options.parseArgs("--module-path", dir1_PS_dir2);
    assertEquals(options.getModuleSearchPaths(), Arrays.asList(dir1, dir2));

    options = Options.parseArgs("--class-path", dir1_PS_dir2);
    assertEquals(options.getClassSearchPath(), Arrays.asList(dir1, dir2));
}









