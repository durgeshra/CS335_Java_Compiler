



public void testRunWithNonExistentEntry() throws Exception {

    String upgrademodulepath
        = "DoesNotExit" + File.pathSeparator + UPGRADEDMODS_DIR.toString();
    String mid = "test/jdk.test.Main";

    int exitValue
        = executeTestJava(
            "--upgrade-module-path", upgrademodulepath,
            "--module-path", MODS_DIR.toString(),
            "-m", mid)
        .outputTo(System.out)
        .errorTo(System.out)
        .getExitValue();

    assertTrue(exitValue == 0);

}









