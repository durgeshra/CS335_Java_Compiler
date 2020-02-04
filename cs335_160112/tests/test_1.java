// Taken from https://www.codechef.com/viewsolution/2988299
import java.io.IOException;
import java.io.InputStream;
import java.util.Arrays;
import java.util.InputMismatchException;
 
public class Main {
 
	/**
	 * @param args
	 * @throws IOException 
	 * @throws NumberFormatException 
	 */
	public static void main(String[] args) throws NumberFormatException, IOException {
		InputReader in=new InputReader(System.in);
		//BufferedReader in=new BufferedReader(new InputStreamReader(System.in));
		int t=in.readInt();
		while(t-->0){
			
			int n=in.readInt();
			int k=in.readInt();
			int vect[][]=new int[n][k];
			int a[]=new int[k];
			int i=0;
			while(i<n){
				
				int j=0;
				while(j<k){
					vect[i][j]=in.readInt();
					j++;
				}
				i++;
			}
			int j=0;
			
			
			while(j<k){
				a[j]=in.readInt();
				j++;
			}			
			
			i=0;
			
			boolean whoisvalid[]=new boolean[n];
			/*
			int looptime=1000;
			if(n*k>1000 && n*k<5000) looptime=500;
			else if(n*k>10000) looptime=50;
			
			*/
			int looptime =0;
			int ans[]=new int[1000];
			int q=0;
			while(looptime<1000000){
				
				i=0;
				while(i<n){
					j=0;
					int temp=0;
					while(j<k){
						if(vect[i][j]>a[j] || vect[i][j]==-1) { temp=1;break;}
						j++;
					}
					if(temp==0) {
						whoisvalid[i]=true;
					}else whoisvalid[i]=false;
					i++;
				}
				i=0;
				int temp=0;	
				long sum=0;long min=0L,index=0;
				while(i<n){
					sum=0;
					if(whoisvalid[i]==true) {
						int kk=0;
						while(kk<k){
							sum+=a[kk]-vect[i][kk];
							kk++;
						}
						if(min<sum){
							min=sum;
							index=i;
						}
						temp=1;
 
					}
					i++;
				}
				if(temp==0){
					break;
				}
				else {
					//System.out.println(1);
					int kk=0;
					
					
						while(kk<k){
							a[kk]=a[kk]-vect[(int)index][kk];
							vect[(int)index][kk]=-1;
							kk++;
						}
					
					ans[q]=(int)index+1;
					q++;
				//	System.out.println(index+1); 
					whoisvalid[(int) index]=false;
					if(looptime*n*k*100>=100000000) break;
					looptime++;
				}
			}
			if(q==0){
				System.out.println(0);
			}else {
				Arrays.sort(ans,0,q);
				int kk=0;
				System.out.println(q);
				while(kk<q){
					System.out.print(ans[kk]+" ");
					kk++;
				}
				System.out.println();
			}
			
		}
	}
 
} 
 
 
class InputReader {
	 
 
	
	private InputStream stream;
    private byte[] buf = new byte[1024];
    private int curChar;
    private int numChars;
 
    public InputReader(InputStream stream) {
        this.stream = stream;
    }
 
    public int read() {
        if (numChars == -1)
            throw new InputMismatchException();
        if (curChar >= numChars) {
            curChar = 0;
            try {
                numChars = stream.read(buf);
            } catch (IOException e) {
                throw new InputMismatchException();
            }
            if (numChars <= 0)
                return -1;
        }
        return buf[curChar++];
    }
 
    public int readInt() {
        int c = read();
        while (isSpaceChar(c))
            c = read();
        int sgn = 1;
        if (c == '-') {
            sgn = -1;
            c = read();
        }
        int res = 0;
        do {
            if (c < '0' || c > '9')
                throw new InputMismatchException();
            res *= 10;
            res += c - '0';
            c = read();
        } while (!isSpaceChar(c));
        return res * sgn;
    }
 
    public String readString() {
        int c = read();
        while (isSpaceChar(c))
            c = read();
        StringBuffer res = new StringBuffer();
        do {
            res.appendCodePoint(c);
            c = read();
        } while (!isSpaceChar(c));
        return res.toString();
    }
 
    public static boolean isSpaceChar(int c) {
        return c == ' ' || c == '\n' || c == '\r' || c == '\t' || c == -1;
    }
}  
