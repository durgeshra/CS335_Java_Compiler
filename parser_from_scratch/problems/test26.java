// Java program to illustrate the behaviour of 
// char literals and integer literals when 
// we are performing addition 
public class Test { 
    public static void main(String[] args) 
    { 
        // ASCII value of 0 is 48 
        int first = '0'; 
  
        // ASCII value of 7 is 55 
        int second = '7'; 
        System.out.println("Geeks!" + first + 
                                '2' + second); 
        boolean b = true; 
        boolean c = false; 
        boolean d = 0; 
        boolean b = 1; 
        System.out.println(b); 
        System.out.println(c); 
        System.out.println(d); 
        System.out.println(e); 
        String s = "Hello"; 
  
        // If we assign without "" then it treats as a variable 
        // and causes compiler error 
        String s1 = Hello;  
  
        System.out.println(s); 
  
       
    } 
} 