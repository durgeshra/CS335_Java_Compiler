


public void testWithExplodedPatches() throws Exception {

    
    String basePatches = PATCHES1_DIR.resolve("java.base")
            + File.pathSeparator + PATCHES2_DIR.resolve("java.base");

    String dnsPatches = PATCHES1_DIR.resolve("jdk.naming.dns")
            + File.pathSeparator + PATCHES2_DIR.resolve("jdk.naming.dns");

    String compilerPatches = PATCHES1_DIR.resolve("jdk.compiler")
            + File.pathSeparator + PATCHES2_DIR.resolve("jdk.compiler");

    runTest(basePatches, dnsPatches, compilerPatches);
}




