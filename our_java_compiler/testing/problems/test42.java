public static void main(String[] args)
        throws Throwable {

    String baseDir = System.getProperty("user.dir") + File.separator;
    String javac = JDKToolFinder.getTestJDKTool("javac");
    String java = JDKToolFinder.getTestJDKTool("java");

    setup(baseDir);
    String srcDir = System.getProperty("test.src");
    String cp = srcDir + File.separator + "a" + File.pathSeparator
            + srcDir + File.separator + "b.jar" + File.pathSeparator
            + ".";
    List<String[]> allCMDs = List.of(
            // Compile command
            new String[]{
                    javac, "-cp", cp, "-d", ".",
                    srcDir + File.separator + TEST_NAME + ".java"
            },
            // Run test the first time
            new String[]{
                    java, "-cp", cp, TEST_NAME, "1"
            },
            // Run test the second time
            new String[]{
                    java, "-cp", cp, TEST_NAME, "2"
            }
    );

    for (String[] cmd : allCMDs) {
        ProcessTools.executeCommand(cmd)
                    .outputTo(System.out)
                    .errorTo(System.out)
                    .shouldHaveExitValue(0);
    }
}