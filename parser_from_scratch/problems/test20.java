import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.util.Arrays;
import java.util.HashMap;
import java.util.StringTokenizer;

public class Main {

	static long mod = 1000000007;
	static long[] f = new long[100001];

	public static void main(String[] args) throws IOException {

		PrintWriter out = new PrintWriter(System.out);
		Reader scn = new Reader();
		f[0] = 1;

		for (int i = 1; i < f.length; i++)
			f[i] = (f[i - 1] % mod * i) % mod;

		StringBuilder sb = new StringBuilder();

		int t = scn.nextInt();

		A: while (t-- > 0) {

			int n = scn.nextInt();
			long arr[] = new long[2 * n];
			long tsm = 0;

			for (int i = 0; i < 2 * n; i++) {
				arr[i] = scn.nextLong();
				tsm += arr[i];
			}
			long sum = tsm / (n + 1);
			int c = 0;
			for (int i = 0; i < arr.length; i++)
				if (arr[i] == sum)
					c++;
			if (n == 1)
				sb.append((arr[0] == arr[1] ? 1 : 0) + "\n");
			else if (tsm % (n + 1) != 0 || c < 2)
				sb.append("0\n");
			else {

				Arrays.sort(arr);
				long a[] = new long[2 * n - 2];
				int idx = 0, cnt = 0;
				for (long v : arr) {
					if (v == sum) {
						if (cnt >= 2)
							a[idx++] = v;
						else
							cnt++;
					} else
						a[idx++] = v;
				}

				int l = 0, r = a.length - 1;
				while (l < r)
					if (a[l++] + a[r--] != sum) {
						sb.append("0\n");
						continue A;
					}

				HashMap<Long, Integer> pfafrmap = new HashMap<>();
				for (int i = 0; i < n - 1; i++)
					pfafrmap.put(a[i], pfafrmap.getOrDefault(a[i], 0) + 1);

				int v = n - 1 - (sum % 2 == 0 ? pfafrmap.getOrDefault(sum / 2, 0) : 0);
				long p2v = 1;
				for (int i = 1; i <= v; i++)
					p2v = (p2v * 2) % mod;

				long denm = 1;
				for (long key : pfafrmap.keySet())
					denm = (f[pfafrmap.get(key)] * denm) % mod;

				long perm = (f[n - 1] * modInverse(denm, mod)) % mod;

				p2v = (p2v * perm) % mod;
				sb.append(p2v + "\n");
			}
		}
		out.print(sb);
		out.flush();
	}

	public static long modInverse(long A, long M) {
		return modularExponentiation(A, M - 2, M);
	}

	public static long modularExponentiation(long x, long n, long M) {
		long d = 1L;
		String bString = Long.toBinaryString(n);
		for (int i = 0; i < bString.length(); i++) {
			d = (d * d) % M;
			if (bString.charAt(i) == '1')
				d = (d * x) % M;
		}
		return d;
	}

	public static class Reader {

		final private int BUFFER_SIZE = 1 << 16;
		private DataInputStream din;
		private byte[] buffer;
		private int bufferPointer, bytesRead;

		public Reader() {
			din = new DataInputStream(System.in);
			buffer = new byte[BUFFER_SIZE];
			bufferPointer = bytesRead = 0;
		}

		public Reader(String file_name) throws IOException {
			din = new DataInputStream(new FileInputStream(file_name));
			buffer = new byte[BUFFER_SIZE];
			bufferPointer = bytesRead = 0;
		}

		public String readLine() throws IOException {
			byte[] buf = new byte[100000 + 1];
			int cnt = 0, c;
			while ((c = read()) != -1) {
				if (c == '\n')
					break;
				buf[cnt++] = (byte) c;
			}
			return new String(buf, 0, cnt);
		}

		public int nextInt() throws IOException {
			int ret = 0;
			byte c = read();
			while (c <= ' ')
				c = read();
			boolean neg = (c == '-');
			if (neg)
				c = read();
			do {
				ret = ret * 10 + c - '0';
			} while ((c = read()) >= '0' && c <= '9');
			if (neg)
				return -ret;
			return ret;
		}

		public long nextLong() throws IOException {
			long ret = 0;
			byte c = read();
			while (c <= ' ')
				c = read();
			boolean neg = (c == '-');
			if (neg)
				c = read();
			do {
				ret = ret * 10 + c - '0';
			} while ((c = read()) >= '0' && c <= '9');
			if (neg)
				return -ret;
			return ret;
		}

		public double nextDouble() throws IOException {
			double ret = 0, div = 1;
			byte c = read();
			while (c <= ' ')
				c = read();
			boolean neg = (c == '-');
			if (neg)
				c = read();

			do {
				ret = ret * 10 + c - '0';
			} while ((c = read()) >= '0' && c <= '9');

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

		private byte read() throws IOException {
			if (bufferPointer == bytesRead)
				fillBuffer();
			return buffer[bufferPointer++];
		}

		public void close() throws IOException {
			if (din == null)
				return;
			din.close();
		}

		public int[] nextIntArray(int n) throws IOException {
			int[] arr = new int[n];
			for (int i = 0; i < n; i++)
				arr[i] = nextInt();
			return arr;
		}

		public long[] nextLongArray(int n) throws IOException {
			long[] arr = new long[n];
			for (int i = 0; i < n; i++)
				arr[i] = nextLong();
			return arr;
		}

		public int[][] nextInt2DArray(int m, int n) throws IOException {
			int[][] arr = new int[m][n];
			for (int i = 0; i < m; i++)
				for (int j = 0; j < n; j++)
					arr[i][j] = nextInt();
			return arr;
		}
	}
}