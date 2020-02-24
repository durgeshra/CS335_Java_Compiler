void run() throws Exception {
    String PS = File.pathSeparator;
    writeFile("src1/p/A.java",
            "package p; public class A { }");
    compile("-d", "classes1", "src1/p/A.java");

    writeFile("src2/q/B.java",
            "package q; public class B extends p.A { }");
    compile("-d", "classes2", "-classpath", "classes1", "src2/q/B.java");

    writeFile("src/Test.java",
            " class Test extends q.B { }");

    test("src/Test.java", "-sourcepath", "src1" + PS + "src2");
    test("src/Test.java", "-classpath", "classes1" + PS + "classes2");

    File testJar = createJar();
    test("src/Test.java", "-bootclasspath",
            testJar + PS + "classes1" + PS + "classes2");

    if (errors > 0)
        throw new Exception(errors + " errors found");
}









