import java.util.*;
import java.io.*;
 
/**
 *
 * @author umang
 */
 
class ANDMIN{
    
    public static int mod = (int) (1e9+7);
    
    public static long[] arr;
    
    public static class SegmentTree {
        long st[];
 
        SegmentTree(int n)  {
            st = new long[4*n];
            build(0, n - 1, 1);
        }
    
        public int getMid(int s, int e) {
            return (s+e)>>1;
        }

        public void update(int s, int e, int x, int y, long c, int si){
            if(s == x && e == y){
                st[si]-=c;
            }
            else{
                int mid = getMid(s, e);
                if(y <= mid)    
                    update(s, mid, x, y, c, 2*si);
                else if(x > mid)
                    update(mid + 1, e, x ,y ,c ,2*si + 1);
                else{
                    update(s, mid, x, mid, c, 2*si);
                    update(mid + 1, e, mid + 1, y, c, 2*si + 1);
                }
                st[si]=min(st[2*si],st[2*si+1]);
            }
        }

        public long  get(int s, int e, int x, int y, int si){

            if(s == x && e == y){
                return st[si];
            }
            int mid = getMid(s, e);
            if(y <= mid)
                return get(s, mid, x, y, 2*si);
            else if(x > mid)
                return get(mid + 1, e, x, y, 2*si + 1);
            return min(get(s, mid, x, mid, 2*si) , get(mid + 1, e, mid + 1, y, 2*si + 1));
        }

        public void build(int ss, int se, int si){
            if (ss == se) {
                st[si] = arr[ss];
                return;
            }

            int mid = getMid(ss, se);
            build(ss, mid, si * 2 );
            build(mid + 1, se, si * 2 + 1);
            st[si]=min(st[si*2],st[si*2+1]);
        }
        public void print(){
            System.out.println(Arrays.toString(st));
        }
    }
    
    public static void main(String[] args) {
 
        InputReader in = new InputReader(System.in);
        PrintWriter out = new PrintWriter(System.out);
        
        int n=in.nextInt();
        int q=in.nextInt();
        
        arr=in.nextLongArray(n);
        SegmentTree segmentTree=new SegmentTree(n);
        
        TreeSet<Integer>[] set=new TreeSet[31];
        for(int j=0;j<31;j++){
            set[j]=new TreeSet();
            for(int i=0;i<n;i++){
                if((arr[i]&(1<<j))!=0){
                    set[j].add(i);
                }
            }
        }
        
        while(q-->0){
            int t=in.nextInt();
            int l=in.nextInt()-1;
            int r=in.nextInt()-1;
            if(t==0){
                long ans=segmentTree.get(0, n-1, l, r, 1);
                out.println(ans);
            }
            else{
                long x=in.nextInt();
                for(int i=0;i<31;i++){
                    if((x&(1<<i))==0){
                        while(!set[i].isEmpty() && set[i].last()>=l){
                            int high=set[i].higher(l-1);
                            if(high<=r){
                                segmentTree.update(0, n-1, high,high, 1<<i, 1);
                                set[i].remove(high);
                            }
                            else break;
                        }
                    }
                }
            }
        }
        
        out.close();
    }
    
    static class Pair implements Comparable<Pair>{

        int x,y,i;
        
	Pair (int x,int y,int i){
		this.x=x;
		this.y=y;
		this.i=i;
	}

	Pair (int x,int y){
		this.x=x;
		this.y=y;
	}
        
	public int compareTo(Pair o) {
		if(this.x!=o.x)
                    return Integer.compare(this.x,o.x);
		else
                    return Integer.compare(this.y,o.y);
		//return 0;
	}

        public boolean equals(Object o) {
            if (o instanceof Pair) {
                Pair p = (Pair)o;
                return p.x == x && p.y == y && p.i==i;
            }
            return false;
        }
            
        public int hashCode() {
            return new Integer(x).hashCode() * 31 + new Integer(y).hashCode()+new Integer(i).hashCode()*37;
        }

        @Override
        public String toString() {
            return  x + " " + y ;
        }
    
    } 
    
    public static boolean isPal(String s){
        for(int i=0, j=s.length()-1;i<=j;i++,j--){
                if(s.charAt(i)!=s.charAt(j)) return false;
        }
        return true;
    }
    public static String rev(String s){
		StringBuilder sb=new StringBuilder(s);
		sb.reverse();
		return sb.toString();
    }
    
    public static long gcd(long x,long y){
	if(x%y==0)
		return y;
	else
		return gcd(y,x%y);
    }
    
    public static int gcd(int x,int y){
	if(x%y==0)
		return y;
	else 
		return gcd(y,x%y);
    }
    
    public static long gcdExtended(long a,long b,long[] x){
        
        if(a==0){
            x[0]=0;
            x[1]=1;
            return b;
        }
        long[] y=new long[2];
        long gcd=gcdExtended(b%a, a, y);
        
        x[0]=y[1]-(b/a)*y[0];
        x[1]=y[0];
        
        return gcd;
    }
    
    public static int abs(int a,int b){
	return (int)Math.abs(a-b);
    }
 
    public static long abs(long a,long b){
	return (long)Math.abs(a-b);
    }
    
    public static int max(int a,int b){
	if(a>b)
		return a;
	else
		return b;
    }
 
    public static int min(int a,int b){
	if(a>b)
		return b;
	else 
		return a;
    }
    
    public static long max(long a,long b){
	if(a>b)
		return a;
	else
		return b;
    }
 
    public static long min(long a,long b){
	if(a>b)
		return b;
	else 
		return a;
    }
 
    public static long pow(long n,long p,long m){
	 long  result = 1;
	  if(p==0)
	    return 1;
	if (p==1)
	    return n;
	while(p!=0)
	{
	    if(p%2==1)
	        result *= n;
	    if(result>=m)
	    result%=m;
	    p >>=1;
	    n*=n;
	    if(n>=m)
	    n%=m;
	}
	return result;
    }
    
    public static long pow(long n,long p){
	long  result = 1;
	  if(p==0)
	    return 1;
	if (p==1)
	    return n;
	while(p!=0)
	{
	    if(p%2==1)
	        result *= n;	    
	    p >>=1;
	    n*=n;	    
	}
	return result;
    }
    
	static class InputReader {
 
		private final InputStream stream;
		private final byte[] buf = new byte[8192];
		private int curChar, snumChars;
		private SpaceCharFilter filter;
 
		public InputReader(InputStream stream) {
			this.stream = stream;
		}
 
		public int snext() {
			if (snumChars == -1)
				throw new InputMismatchException();
			if (curChar >= snumChars) {
				curChar = 0;
				try {
					snumChars = stream.read(buf);
				} catch (IOException e) {
					throw new InputMismatchException();
				}
				if (snumChars <= 0)
					return -1;
			}
			return buf[curChar++];
		}
 
		public int nextInt() {
			int c = snext();
			while (isSpaceChar(c)) {
				c = snext();
			}
			int sgn = 1;
			if (c == '-') {
				sgn = -1;
				c = snext();
			}
			int res = 0;
			do {
				if (c < '0' || c > '9')
					throw new InputMismatchException();
				res *= 10;
				res += c - '0';
				c = snext();
			} while (!isSpaceChar(c));
			return res * sgn;
		}
 
		public long nextLong() {
			int c = snext();
			while (isSpaceChar(c)) {
				c = snext();
			}
			int sgn = 1;
			if (c == '-') {
				sgn = -1;
				c = snext();
			}
			long res = 0;
			do {
				if (c < '0' || c > '9')
					throw new InputMismatchException();
				res *= 10;
				res += c - '0';
				c = snext();
			} while (!isSpaceChar(c));
			return res * sgn;
		}
 
		public int[] nextIntArray(int n) {
			int a[] = new int[n];
			for (int i = 0; i < n; i++) {
				a[i] = nextInt();
			}
			return a;
		}
 
		public long[] nextLongArray(int n) {
			long a[] = new long[n];
			for (int i = 0; i < n; i++) {
				a[i] = nextInt();
			}
			return a;
		}
                
		public String readString() {
			int c = snext();
			while (isSpaceChar(c)) {
				c = snext();
			}
			StringBuilder res = new StringBuilder();
			do {
				res.appendCodePoint(c);
				c = snext();
			} while (!isSpaceChar(c));
			return res.toString();
		}
 
		public String nextLine() {
			int c = snext();
			while (isSpaceChar(c))
				c = snext();
			StringBuilder res = new StringBuilder();
			do {
				res.appendCodePoint(c);
				c = snext();
			} while (!isEndOfLine(c));
			return res.toString();
		}
 
		public boolean isSpaceChar(int c) {
			if (filter != null)
				return filter.isSpaceChar(c);
			return c == ' ' || c == '\n' || c == '\r' || c == '\t' || c == -1;
		}
 
		private boolean isEndOfLine(int c) {
			return c == '\n' || c == '\r' || c == -1;
		}
 
		public interface SpaceCharFilter {
			public boolean isSpaceChar(int ch);
		}
	}
}    
