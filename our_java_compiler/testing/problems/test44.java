/**
 * Run test with ---patch-module and exploded patches
 */
public void testWithExplodedPatches() throws Exception {

    // patches1/java.base:patches2/java.base
    String basePatches = PATCHES1_DIR.resolve("java.base")
            + File.pathSeparator + PATCHES2_DIR.resolve("java.base");

    String dnsPatches = PATCHES1_DIR.resolve("jdk.naming.dns")
            + File.pathSeparator + PATCHES2_DIR.resolve("jdk.naming.dns");

    String compilerPatches = PATCHES1_DIR.resolve("jdk.compiler")
            + File.pathSeparator + PATCHES2_DIR.resolve("jdk.compiler");

    runTest(basePatches, dnsPatches, compilerPatches);
}