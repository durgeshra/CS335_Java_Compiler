import java.io.*;
import java.util.*;

public class Main {
	static final StdIn in = new StdIn();
	static final PrintWriter out = new PrintWriter(System.out);
	
	public static void main(String[] args) {
		int n=in.nextInt(), q=in.nextInt();
		int[] p = in.readIntArray(n, -1);



		Node node = new Node();
		int[] rt = new int[n+1];
		rt[0]=node.init(n);
		int[] mnl = new int[n], mxl = new int[n];
		for(int i=0; i<n; ++i) {
			rt[i+1]=node.mc(rt[i]);
			node.ver[rt[i+1]]=i+1;
			mnl[i]=i-1;
			while(mnl[i]>=0&&p[mnl[i]]>p[i]) {
				node.add(rt[i+1], mnl[mnl[i]]+1, mnl[i], -(p[i]-p[mnl[i]]), 0, n-1);
				mnl[i]=mnl[mnl[i]];
			}
			mxl[i]=i-1;
			while(mxl[i]>=0&&p[mxl[i]]<p[i]) {
				node.add(rt[i+1], mxl[mxl[i]]+1, mxl[i], p[i]-p[mxl[i]], 0, n-1);
				mxl[i]=mxl[mxl[i]];
			}
			node.ans(rt[i+1], i+1);
		}
		int last=0;
		for(int i=0; i<q; ++i) {
			int l=(in.nextInt()+last-1)%n, r=(in.nextInt()+last-1)%n;
			if(l>r) {
				l^=r^(r=l);
			}
			out.println(last=node.ask(rt[r+1], l, n, 0, n-1, 0));
		}
		out.close();
	}
	
	static class Node {
		static final int sz=(int)2.5e7;
		int csz;
		int[] lc = new int[sz], rc = new int[sz];
		int[] ver = new int[sz], ans = new int[sz], mnv = new int[sz], mnp = new int[sz];
		int[] lzadd = new int[sz], lzans = new int[sz];
		void modify(int u, int x, int y) {
			mnv[u]+=x;
			lzadd[u]+=x;
			ans[u]=Math.max(ans[u], y-mnp[u]);
			lzans[u]=Math.max(lzans[u], y);
		}
		void pushdown(int u) {
			if(ver[lc[u]]!=ver[u]) {
				lc[u]=mc(lc[u]);
				ver[lc[u]]=ver[u];
			}
			int lzansl=0, lzansr=0;
			if(mnv[lc[u]]<=mnv[rc[u]]) {
				lzansl=lzans[u];
			}
			if(mnv[rc[u]]<=mnv[lc[u]]) {
				lzansr=lzans[u];
			}
			modify(lc[u], lzadd[u], lzansl);
			if(ver[rc[u]]!=ver[u]) {
				rc[u]=mc(rc[u]);
				ver[rc[u]]=ver[u];
			}
			modify(rc[u], lzadd[u], lzansr);
			lzadd[u]=0;
			lzans[u]=0;
		}
		void pushup(int u) {
			ans[u]=Math.max(ans[lc[u]], ans[rc[u]]);
			mnv[u]=Math.min(mnv[lc[u]], mnv[rc[u]]);
			if(mnv[lc[u]]==mnv[u]) {
				mnp[u]=mnp[lc[u]];
			} else {
				mnp[u]=mnp[rc[u]];
			}
		}
		int mc(int u) {
			int v=csz;
			++csz;
			ver[v]=ver[u];
			lc[v]=lc[u];
			rc[v]=rc[u];
			ans[v]=ans[u];
			mnv[v]=mnv[u];
			mnp[v]=mnp[u];
			lzadd[v]=lzadd[u];
			lzans[v]=lzans[u];
			return v;
		}
		int init(int n) {
			int root=mc(0);
			init2(root, 0, n-1);
			return root;
		}
		void init2(int u, int rangeL, int rangeR) {
			if(rangeL==rangeR) {
				mnv[u]=rangeL;
				mnp[u]=rangeL;
			} else {
				int lcR=(rangeL+rangeR)/2, rcL=lcR+1;
				lc[u]=mc(0);
				init2(lc[u], rangeL, lcR);
				rc[u]=mc(0);
				init2(rc[u], rcL, rangeR);
				pushup(u);
			}
		}
		void add(int u, int addL, int addR, int addX, int rangeL, int rangeR) {
			if(addL<=rangeL&&rangeR<=addR) {
				modify(u, addX, 0);
			} else {
				int lcR=(rangeL+rangeR)/2, rcL=lcR+1;
				pushdown(u);
				if(addL<=lcR) {
					add(lc[u], addL, addR, addX, rangeL, lcR);
				}
				if(rcL<=addR) {
					add(rc[u], addL, addR, addX, rcL, rangeR);
				}
				pushup(u);
			}
		}
		void ans(int u, int x) {
			modify(u, 0, x);
		}
		int ask(int u, int askL, int askR, int rangeL, int rangeR, int plzans) {
			if(askL<=rangeL&&rangeR<=askR) {
				return Math.max(ans[u], plzans-mnp[u]);
			} else {
				int lcR=(rangeL+rangeR)/2, rcL=lcR+1;

				plzans=Math.max(plzans, lzans[u]);
				int ans=0;
				if(askL<=lcR) {
					ans=Math.max(ans, ask(lc[u], askL, askR, rangeL, lcR, mnv[lc[u]]<=mnv[rc[u]]?plzans:0));
				}
				if(rcL<=askR) {
					ans=Math.max(ans, ask(rc[u], askL, askR, rcL, rangeR, mnv[lc[u]]>=mnv[rc[u]]?plzans:0));
				}
				return ans;
			}
		}
	}
	
	static class StdIn {
		final private int BUFFER_SIZE = 1 << 16;
		private DataInputStream din;
		private byte[] buffer;
		private int bufferPointer, bytesRead;
		public StdIn() {
			din = new DataInputStream(System.in);
			buffer = new byte[BUFFER_SIZE];
			bufferPointer = bytesRead = 0;
		}
		public StdIn(InputStream in) {
			try{
				din = new DataInputStream(in);
			} catch(Exception e) {
				throw new RuntimeException();
			}
			buffer = new byte[BUFFER_SIZE];
			bufferPointer = bytesRead = 0;
		}
		public String next() {
			int c;
			while((c=read())!=-1&&(c==' '||c=='\n'||c=='\r'));
			StringBuilder s = new StringBuilder();
			while (c != -1)
			{
				if (c == ' ' || c == '\n'||c=='\r')
					break;
				s.append((char)c);
				c=read();
			}
			return s.toString();
		}
		public String nextLine() {
			int c;
			while((c=read())!=-1&&(c==' '||c=='\n'||c=='\r'));
			StringBuilder s = new StringBuilder();
			while (c != -1)
			{
				if (c == '\n'||c=='\r')
					break;
				s.append((char)c);
				c = read();
			}
			return s.toString();
		}
		public int nextInt() {
			int ret = 0;
			byte c = read();
			while (c <= ' ')
				c = read();
			boolean neg = (c == '-');
			if (neg)
				c = read();
			do
				ret = ret * 10 + c - '0';
			while ((c = read()) >= '0' && c <= '9');

			if (neg)
				return -ret;
			return ret;
		}
		public int[] readIntArray(int n, int os) {
			int[] ar = new int[n];
			for(int i=0; i<n; ++i)
				ar[i]=nextInt()+os;
			return ar;
		}
		public long nextLong() {
			long ret = 0;
			byte c = read();
			while (c <= ' ')
				c = read();
			boolean neg = (c == '-');
			if (neg)
				c = read();
			do
				ret = ret * 10 + c - '0';
			while ((c = read()) >= '0' && c <= '9');
			if (neg)
				return -ret;
			return ret;
		}
		public long[] readLongArray(int n, long os) {
			long[] ar = new long[n];
			for(int i=0; i<n; ++i)
				ar[i]=nextLong()+os;
			return ar;
		}
		public double nextDouble() {
			double ret = 0, div = 1;
			byte c = read();
			while (c <= ' ')
				c = read();
			boolean neg = (c == '-');
			if (neg)
				c = read();
			do
				ret = ret * 10 + c - '0';
			while ((c = read()) >= '0' && c <= '9');
			if (c == '.')
				while ((c = read()) >= '0' && c <= '9')
					ret += (c - '0') / (div *= 10);
			if (neg)
				return -ret;
			return ret;
		}
		private void fillBuffer() throws IOException {
			bytesRead = din.read(buffer, bufferPointer = 0, BUFFER_SIZE);
			if (bytesRead == -1)
				buffer[0] = -1;
		}
		private byte read() {
			try{
				if (bufferPointer == bytesRead)
					fillBuffer();
				return buffer[bufferPointer++];
			} catch(IOException e) {
				throw new RuntimeException();
			}
		}
		public void close() throws IOException {
			if (din == null)
				return;
			din.close();
		}
	}
}












