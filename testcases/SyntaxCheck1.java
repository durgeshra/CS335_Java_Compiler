package project.unittests;

public class SyntaxCheck1 {
    public static void main(String[] args) {
        int a;
        a = 5;
        a++;
        printFunc(a);

        float b = 3.14f; 
        printFunc(b);

        long val = 100L;
        printFunc(val);
    }

    static void printFunc(float val) {
        System.out.println(val);
    }

    static void printFunc(int val) {
        System.out.println(val);
    }

    static void printFunc(long val) {
        System.out.println(val);
    }
}




