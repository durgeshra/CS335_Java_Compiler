import java.io.ByteArrayInputStream;

import java.io.IOException;

import java.io.InputStream;

import java.io.PrintWriter;

import java.util.Arrays;

import java.util.HashMap;

import java.util.InputMismatchException;

import java.util.Map;



class CFINASUM {

	InputStream is;

	PrintWriter out;

	String INPUT = "";



	void solve()

	{

		for(int T = ni();T > 0;T--){

			int n = ni();

			int[] a = na(n);

			long[] cum = new long[n+1];

			for(int i = 0;i < n;i++)cum[i+1] = cum[i] + a[i];



			Map<Long, Integer> suf = new HashMap<>();

			for(int i = 1;i < n;i++){

				if(!suf.containsKey(cum[i])){

					suf.put(cum[i], 1);

				}else{

					suf.put(cum[i], suf.get(cum[i]) + 1);

				}

			}

			Map<Long, Integer> pre = new HashMap<>();

			long ans = 0;

			for(int i = 0;i < n;i++){

				long tar = cum[n] - a[i];

				if(tar % 2 == 0){

					tar /= 2;

					ans += pre.getOrDefault(tar, 0);

					ans += suf.getOrDefault(tar+a[i], 0);

				}



				if(i < n-1){

					if(!pre.containsKey(cum[i+1])){

						pre.put(cum[i+1], 1);

					}else{

						pre.put(cum[i+1], pre.get(cum[i+1]) + 1);

					}

					suf.put(cum[i+1], suf.get(cum[i+1])-1);

				}

			}

			out.println(ans);

		}

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



	public static void main(String[] args) throws Exception { new CFINASUM().run(); }



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

















