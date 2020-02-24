import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.PrintWriter;
import java.util.Arrays;
import java.util.InputMismatchException;

class GRAPHTRE {
	InputStream is;
	PrintWriter out;
	String INPUT = "";
	
	void solve()
	{
		int mod = 1000000007;
		for(int T = ni();T > 0;T--){
			int n = ni(), m = ni();
			int[] a = na(n);
			int[] from = new int[m];
			int[] to = new int[m];
			for(int i = 0;i < m;i++){
				from[i] = ni()-1;
				to[i] = ni()-1;
			}
			int[][] g = packU(n, from, to);
			int[] nins = new int[n];
			for(int i = 0;i < n;i++){
				int nin = 0;
				for(int e : g[i]){
					if(a[e] > a[i]){
						nin++;
					}
				}
				nins[i] = nin;
			}
			
			long[] dp = new long[n+1];
			dp[0] = 1;
			for(int i = 0;i < n;i++){
				for(int j = i;j >= 0;j--){
					dp[j+1] += dp[j] * nins[i];
					dp[j+1] %= mod;
				}
			}
			
			long[] ans = new long[n+1];
			for(int i = 0;i < n;i++){
				for(int j = 0;j < n;j++){
					dp[j+1] -= dp[j] * nins[i];
					dp[j+1] %= mod;
					if(dp[j+1] < 0)dp[j+1] += mod;
				}
				
				for(int j = 0;j < n;j++){
					ans[n-j] += dp[j] * a[i];
					ans[n-j] %= mod;
				}
				
				for(int j = n-1;j >= 0;j--){
					dp[j+1] += dp[j] * nins[i];
					dp[j+1] %= mod;
				}
			}
			
			for(int i = 1;i < ans.length;i++){

				out.print(ans[i] + " ");
			}
			out.println();
		}
	}
	
	static int[][] packU(int n, int[] from, int[] to) {
		int[][] g = new int[n][];
		int[] p = new int[n];
		for (int f : from)
			p[f]++;
		for (int t : to)
			p[t]++;
		for (int i = 0; i < n; i++)
			g[i] = new int[p[i]];
		for (int i = 0; i < from.length; i++) {
			g[from[i]][--p[from[i]]] = to[i];
			g[to[i]][--p[to[i]]] = from[i];
		}
		return g;
	}
	
	void run() throws Exception
	{
		is = INPUT.isEmpty() ? System.in : new ByteArrayInputStream(INPUT.getBytes());
		out = new PrintWriter(System.out);
		
		long s = System.currentTimeMillis();
		solve();
		out.flush();
		if(!INPUT.isEmpty())tr(System.currentTimeMillis()-s+"ms");
	}
	
	public static void main(String[] args) throws Exception { new GRAPHTRE().run(); }
	
	private byte[] inbuf = new byte[1024];
	public int lenbuf = 0, ptrbuf = 0;
	
	private int readByte()
	{
		if(lenbuf == -1)throw new InputMismatchException();
		if(ptrbuf >= lenbuf){
			ptrbuf = 0;
			try { lenbuf = is.read(inbuf); } catch (IOException e) { throw new InputMismatchException(); }
			if(lenbuf <= 0)return -1;
		}
		return inbuf[ptrbuf++];
	}
	
	private boolean isSpaceChar(int c) { return !(c >= 33 && c <= 126); }
	private int skip() { int b; while((b = readByte()) != -1 && isSpaceChar(b)); return b; }
	
	private double nd() { return Double.parseDouble(ns()); }
	private char nc() { return (char)skip(); }
	
	private String ns()
	{
		int b = skip();
		StringBuilder sb = new StringBuilder();
		while(!(isSpaceChar(b))){ 
			sb.appendCodePoint(b);
			b = readByte();
		}
		return sb.toString();
	}
	
	private char[] ns(int n)
	{
		char[] buf = new char[n];
		int b = skip(), p = 0;
		while(p < n && !(isSpaceChar(b))){
			buf[p++] = (char)b;
			b = readByte();
		}
		return n == p ? buf : Arrays.copyOf(buf, p);
	}
	
	private char[][] nm(int n, int m)
	{
		char[][] map = new char[n][];
		for(int i = 0;i < n;i++)map[i] = ns(m);
		return map;
	}
	
	private int[] na(int n)
	{
		int[] a = new int[n];
		for(int i = 0;i < n;i++)a[i] = ni();
		return a;
	}
	
	private int ni()
	{
		int num = 0, b;
		boolean minus = false;
		while((b = readByte()) != -1 && !((b >= '0' && b <= '9') || b == '-'));
		if(b == '-'){
			minus = true;
			b = readByte();
		}
		
		while(true){
			if(b >= '0' && b <= '9'){
				num = num * 10 + (b - '0');
			}else{
				return minus ? -num : num;
			}
			b = readByte();
		}
	}
	
	private long nl()
	{
		long num = 0;
		int b;
		boolean minus = false;
		while((b = readByte()) != -1 && !((b >= '0' && b <= '9') || b == '-'));
		if(b == '-'){
			minus = true;
			b = readByte();
		}
		
		while(true){
			if(b >= '0' && b <= '9'){
				num = num * 10 + (b - '0');
			}else{
				return minus ? -num : num;
			}
			b = readByte();
		}
	}
	
	private void tr(Object... o) { if(INPUT.length() > 0)System.out.println(Arrays.deepToString(o)); }
}













