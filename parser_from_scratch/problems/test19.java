import java.io.DataInputStream;
import java.io.FileInputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

class A{
	static void DFSUtil(int v, boolean[] visited, ArrayList<Integer>[] adj, ArrayList<ArrayList<Integer> > al, int k) {
        visited[v] = true;
        al.get(k).add(v);
        for (int x : adj[v]) {
            if(!visited[x]) DFSUtil(x,visited, adj, al, k);
        }

    }
    static ArrayList<ArrayList<Integer> > connectedComponents(ArrayList<Integer>[] adj) {
        boolean[] visited = new boolean[adj.length];
        ArrayList<ArrayList<Integer> > al = new ArrayList<>();
        int k = 0;
        for(int v = 1; v < adj.length; ++v) {
            if(!visited[v]) {
            	al.add(new ArrayList<Integer>());
                DFSUtil(v,visited, adj, al, k);
                k++;
            }
        }
        return al;
    }
    static void util(int v, ArrayList[] adj, boolean visited[], HashMap[] map, int prev) {
        visited[v] = true;
        if(prev>-1) {
        Iterator<Integer> i = adj[prev].listIterator();
        while (i.hasNext()) {
            int n = i.next();
           if(n!=v&&!map[Math.min(prev, n)].containsKey(Math.max(prev, n))) {
        	   if(prev<n)
        		   map[prev].put(n, 1);
        	   else
        		   map[n].put(prev, 1);
           }
        }
        }
        prev = v;
        Iterator<Integer> i = adj[v].listIterator();
        while (i.hasNext())
        {
            int n = i.next();
            if (!visited[n])
                util(v, adj, visited, map, prev);
        }
    }
    static void DFS(int v, ArrayList[] adj, HashMap[] map) {
        boolean visited[] = new boolean[adj.length];
        util(v, adj, visited, map, -1);
    }
	public static void main(String[] args) {
		try {
			BufferInput in = new BufferInput();
			StringBuilder sb = new StringBuilder();
			StringBuilder rem = new StringBuilder();

			int n = in.nextInt();
			int m = in.nextInt();
			int a = in.nextInt();
			int r = in.nextInt();
			ArrayList<Integer>[] adj = new ArrayList[n+1];

			for(int i=1;i<=n;i++) {
				adj[i] = new ArrayList<Integer>();

			}
			sb.append(m).append("\n");
			for(int i=0;i<m;i++) {
				int x = in.nextInt();
				int y = in.nextInt();
				sb.append("1 1 ");
				sb.append(x).append(" ").append(y).append("\n");




			}
			System.out.print(sb);
















		}catch(Exception e) {}

	}
static class BufferInput {

		final private int BUFFER_SIZE = 1 << 16;

		private DataInputStream din;

		private byte[] buffer;

		private int bufferPointer, bytesRead;

		public BufferInput() {
			din = new DataInputStream(System.in);
			buffer = new byte[BUFFER_SIZE];
			bufferPointer = bytesRead = 0;
		}

		public BufferInput(String file_name) throws IOException {
			din = new DataInputStream(new FileInputStream(file_name));
			buffer = new byte[BUFFER_SIZE];
			bufferPointer = bytesRead = 0;
		}

		public String readLine() throws IOException {
			byte[] buf = new byte[64];
			int cnt = 0, c;
			while ((c = read()) != -1) {
				if (c == '\n')
					break;
				buf[cnt++] = (byte) c;
			}
			return new String(buf, 0, cnt);
		}

		public String nextString() throws IOException{

			byte c = read();
			while(Character.isWhitespace(c)){
				c = read();
			}

			StringBuilder builder = new StringBuilder();
			builder.append((char)c);
			c = read();
			while(!Character.isWhitespace(c)){
				builder.append((char)c);
				c = read();
			}

			return builder.toString();
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

		public int[] nextIntArray(int n) throws IOException {
			int arr[] = new int[n];
			for(int i = 0; i < n; i++){
				arr[i] = nextInt();
			}
			return arr;
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

		public long[] nextLongArray(int n) throws IOException {
			long arr[] = new long[n];
			for(int i = 0; i < n; i++){
				arr[i] = nextLong();
			}
			return arr;
		}

		public char nextChar() throws IOException{
			byte c = read();
			while(Character.isWhitespace(c)){
				c = read();
			}
			return (char) c;
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

			if (c == '.') {
				while ((c = read()) >= '0' && c <= '9') {
					ret += (c - '0') / (div *= 10);
				}
			}

			if (neg)
				return -ret;
			return ret;
		}
		public double[] nextDoubleArray(int n) throws IOException {
			double arr[] = new double[n];
			for(int i = 0; i < n; i++){
				arr[i] = nextDouble();
			}
			return arr;
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
	}
}






