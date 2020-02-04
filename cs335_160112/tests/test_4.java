// Taken from https://www.codechef.com/viewsolution/26295657
/* package codechef; // don't place package name! */

import java.util.*;
import java.lang.*;
import java.io.*;

/* Name of the class has to be "Main" only if the class is public. */
class Codechef
{
	public static void main (String[] args) throws java.lang.Exception
	{
	   Scanner sc = new Scanner(System.in);
	   int t = sc.nextInt();
	   for(int i=0;i<t;i++)
	   {
	       int n = sc.nextInt();
	       Rent[] a = new Rent[n];
	       for(int j=0; j<n; j++)
	       {
	           a[j] = new Rent();
	           a[j].vx = sc.nextInt();
	           a[j].vy = sc.nextInt();
	           a[j].dx = sc.nextInt();
	           a[j].dy = sc.nextInt();
	           a[j].dir = sc.nextInt();
	       }
	       for(int k=0;k<n;k++)
	       {
	       
	       String s1 = sc.next();
	       char c = s1.charAt(1);
	       Writer writer = new PrintWriter(System.out);
	       if(c == 'E'){
	        a[k].dir = (a[k].dir + 2) % 4;
	        System.out.println((k+1) +" "+ (k+1));
	        

	       }
	       else {
	        a[k].dir = (a[k].dir + 1) % 4;
	        System.out.println((k+1)+" "+(a[k].dir)+" "+(k+1));
	        

	       }
	       writer.flush();
	       }
	       
	   }
	}
}

class Rent{
    int vx, vy, dx, dy, dir;
    
} 

