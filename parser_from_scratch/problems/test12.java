import java.io.ByteArrayInputStream;

import java.io.IOException;

import java.io.InputStream;

import java.io.PrintWriter;

import java.util.Arrays;

import java.util.InputMismatchException;



class CNTIT {

	InputStream is;

	PrintWriter out;

	String INPUT = "";

	

	void solve()

	{

		for(int T = ni();T > 0;T--){

			int n = ni(), K = ni();

			int[] from = new int[n - 1];

			int[] to = new int[n - 1];

			int[] ws = new int[n-1];

			for (int i = 0; i < n - 1; i++) {

				from[i] = ni() - 1;

				to[i] = ni() - 1;

				ws[i] = ni()-1;

			}

			int[][][] g = packWU(n, from, to, ws);

			int[][] pars = parents(g, 0);

			int[] par = pars[0], ord = pars[1], dep = pars[2];

			int[] cpar = buildCentroidTree(g);

			

			gans = 0;

			for(int i = 0;i < K;i++){

				dfsTopCT(cpar, g, i);

			}

			out.println((long)n*(n-1)/2 - gans);

		}

	}

	

	static class Context

	{

		boolean[] seps; 

		long[] wt; 

		int[] dt;

		int[] vs;

		int[][] vss; 

		int[][] ctch;

		int[][][] g;

		int[] stack;

		int[] inds;





		int color = -1;

	}



	public void dfsTopCT(int[] cpar, int[][][] g, int color) {

		int n = g.length;

		int ctroot = -1;

		for(int i = 0;i < n;i++)if(cpar[i] == -1)ctroot = i;

		

		Context cx = new Context();



		cx.seps = new boolean[n];

		cx.wt = new long[n];

		cx.dt = new int[n];

		cx.vs = new int[n];

		cx.vss = new int[n][];

		cx.ctch = parentToChildren(cpar);

		cx.color = color;

		cx.g = g;

		cx.stack = new int[n];

		cx.inds = new int[n];



		dfs(ctroot, cx);

	}

	

	public static int[][] parentToChildren(int[] par)

	{

		int n = par.length;

		int[] ct = new int[n];

		for(int i = 0;i < n;i++){

			if(par[i] >= 0){

				ct[par[i]]++;

			}

		}

		int[][] g = new int[n][];

		for(int i = 0;i < n;i++){

			g[i] = new int[ct[i]];

		}

		for(int i = 0;i < n;i++){

			if(par[i] >= 0){

				g[par[i]][--ct[par[i]]] = i;

			}

		}

		

		return g;

	}



	

	private void dfs(int sep, Context cx)

	{

		cx.seps[sep] = true;

		int neckp = 0;

		for(int[] neck : cx.g[sep]){

			if(cx.seps[neck[0]])continue;

			

			int sp = 0;

			cx.inds[sp] = 0;



			cx.dt[neck[0]] = neck[1] == cx.color ? 1 : -1;

			int vsp = 0;

			cx.stack[sp++] = neck[0];

			while(sp > 0){

				int cur = cx.stack[sp-1];

				if(cx.inds[sp-1] == 0){

					cx.vs[vsp++] = cur;



				}

				if(cx.inds[sp-1] == cx.g[cur].length){

					sp--; 

					continue; 

				}

				int[] e = cx.g[cur][cx.inds[sp-1]++];

				if(!cx.seps[e[0]] && !(sp-2 >= 0 && e[0] == cx.stack[sp-2])){



					cx.dt[e[0]] = cx.dt[cur] + (e[1] == cx.color ? 1 : -1);

					cx.stack[sp] = e[0];

					cx.inds[sp] = 0;

					sp++;

				}

			}

			cx.vss[neckp] = Arrays.copyOf(cx.vs, vsp);

			neckp++;

		}

		

		process(sep, cx, Arrays.copyOf(cx.vss, neckp));

		

		for(int e : cx.ctch[sep])dfs(e, cx);

	}

	

	private void process(int sep, Context cx, int[][] vss)

	{

		int m = 0;

		for(int[] v : vss)m += v.length;

		int[] alls = new int[m];

		int p = 0;

		F[] fs = new F[vss.length];

		for(int i = 0;i < vss.length;i++){

			int[] ds = new int[vss[i].length];

			for(int j = 0;j < vss[i].length;j++){

				ds[j] = cx.dt[vss[i][j]];

				alls[p++] = cx.dt[vss[i][j]];

			}

			fs[i] = new F(ds);

		}

		F all = new F(alls);

		

		long ans = (long)m*(m+1);

		for(int i = 0;i < vss.length;i++){

			ans -= (long)vss[i].length*(vss[i].length-1);

			

			if(fs[i].f == null)continue;

			for(int j = 0;j < fs[i].f.length;j++){

				long fix = fs[i].f[j] - (j-1 >= 0 ? fs[i].f[j-1] : 0);

				int tar = -(j+fs[i].base);

				ans -= (all.numle(tar) - fs[i].numle(tar)) * fix;



			}

		}

		ans -= all.numle(0)*2;



		gans += ans/2;

	}

	

	long gans = 0;

	

	static class F

	{

		int base;

		int[] f;

		

		F(int[] a)

		{

			int min = Integer.MAX_VALUE;

			int max = Integer.MIN_VALUE;

			for(int v : a){

				min = Math.min(min, v);

				max = Math.max(max, v);

			}

			base = min;

			if(a.length > 0){

				f = new int[max-min+1];

				for(int v : a){

					f[v-base]++;

				}

				for(int i = 1;i < f.length;i++){

					f[i] += f[i-1];

				}

			}

		}

		

		int numle(int x)

		{

			if(f == null)return 0;

			if(x < base)return 0;

			return f[Math.min(x-base, f.length-1)];

		}

	}



	

	public static int[][] parents(int[][][] g, int root) {

		int n = g.length;

		int[] par = new int[n];

		Arrays.fill(par, -1);

		int[] dw = new int[n];

		int[] pw = new int[n];

		int[] dep = new int[n];



		int[] q = new int[n];

		q[0] = root;

		for (int p = 0, r = 1; p < r; p++) {

			int cur = q[p];

			for (int[] nex : g[cur]) {

				if (par[cur] != nex[0]) {

					q[r++] = nex[0];

					par[nex[0]] = cur;

					dep[nex[0]] = dep[cur] + 1;

					dw[nex[0]] = dw[cur] + nex[1];

					pw[nex[0]] = nex[1];

				}

			}

		}

		return new int[][] { par, q, dep, dw, pw };

	}



	

	public static int[] buildCentroidTree(int[][][] g) {

		int n = g.length;

		int[] ctpar = new int[n];

		Arrays.fill(ctpar, -1);

		buildCentroidTree(g, 0, new boolean[n], new int[n], new int[n], new int[n], ctpar);

		return ctpar;

	}

	

	private static int buildCentroidTree(int[][][] g, int root, boolean[] sed, int[] par, int[] ord, int[] des, int[] ctpar)

	{

		

		ord[0] = root;

		par[root] = -1;

		int r = 1;

		for(int p = 0;p < r;p++) {

			int cur = ord[p];

			for(int[] nex : g[cur]){

				if(par[cur] != nex[0] && !sed[nex[0]]){

					ord[r++] = nex[0];

					par[nex[0]] = cur;

				}

			}

		}

		

		

		

		int sep = -1; 

		outer:

		for(int i = r-1;i >= 0;i--){

			int cur = ord[i];

			des[cur] = 1;

			for(int[] e : g[cur]){

				if(par[cur] != e[0] && !sed[e[0]])des[cur] += des[e[0]];

			}

			if(r-des[cur] <= r/2){

				for(int[] e : g[cur]){

					if(par[cur] != e[0] && !sed[e[0]] && des[e[0]] >= r/2+1)continue outer;

				}

				sep = cur;

				break;

			}

		}

		

		sed[sep] = true;

		for(int[] e : g[sep]){

			if(!sed[e[0]])ctpar[buildCentroidTree(g, e[0], sed, par, ord, des, ctpar)] = sep;

		}

		return sep;

	}



	

	public static int[][][] packWU(int n, int[] from, int[] to, int[] w) {

		int[][][] g = new int[n][][];

		int[] p = new int[n];

		for (int f : from)

			p[f]++;

		for (int t : to)

			p[t]++;

		for (int i = 0; i < n; i++)

			g[i] = new int[p[i]][2];

		for (int i = 0; i < from.length; i++) {

			--p[from[i]];

			g[from[i]][p[from[i]]][0] = to[i];

			g[from[i]][p[from[i]]][1] = w[i];

			--p[to[i]];

			g[to[i]][p[to[i]]][0] = from[i];

			g[to[i]][p[to[i]]][1] = w[i];

		}

		return g;

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

	

	public static void main(String[] args) throws Exception { new CNTIT().run(); }

	

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







