private void createImage(Path outputDir, String... modules) throws Throwable {
    Path jlink = Paths.get(JAVA_HOME, "bin", "jlink");
    String mp = JMODS.toString() + File.pathSeparator + MODS_DIR.toString();
    assertTrue(executeProcess(jlink.toString(), "--output", outputDir.toString(),
                    "--add-modules", Arrays.stream(modules).collect(Collectors.joining(",")),
                    "--module-path", mp)
                    .outputTo(System.out)
                    .errorTo(System.out)
                    .getExitValue() == 0);
}


