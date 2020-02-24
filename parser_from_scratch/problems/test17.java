import java.io.*;
import java.math.BigInteger;
import java.util.*;

public class Main {
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    PrintWriter pw = new PrintWriter(System.out);
    static int MOD = 1000000007;

    public static void main(String[] args) throws IOException {
        Main m = new Main();
        m.solve();
        m.close();
    }

    void close() throws IOException {
        pw.flush();
        pw.close();
        br.close();
    }

    int readInt() throws IOException {
        return Integer.parseInt(br.readLine());
    }

    long readLong() throws IOException {
        return Long.parseLong(br.readLine());
    }

    int[] readIntLine() throws IOException {
        String[] tokens = br.readLine().split(" ");
        int[] A = new int[tokens.length];
        for (int i = 0; i < A.length; i++)
            A[i] = Integer.parseInt(tokens[i]);
        return A;
    }

    long[] readLongLine() throws IOException {
        String[] tokens = br.readLine().split(" ");
        long[] A = new long[tokens.length];
        for (int i = 0; i < A.length; i++)
            A[i] = Long.parseLong(tokens[i]);
        return A;
    }

    Set<Integer> powersOfTwo = new HashSet<>(
        Arrays.asList(1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024)
    );

    
    
    
    
    void fill(int[][] A, int r, int c, int n, int e, int f, boolean type) {
        if (n == 1) {
            A[r][c] = e;
            return;
        } else if (powersOfTwo.contains(n)) {
            if (type) {
                fill(A, r, c, n/2, e, (e+f)/2-1, true);  
                fill(A, r+n/2, c+n/2, n/2, e, (e+f)/2-1, true);  
                int m = (e+f)/2;
                fill(A, r, c+n/2, n/2, m, (m+f)/2, false);  
                fill(A, r+n/2, c, n/2, (m+f)/2+1, f, false);  
            } else {
                
                for (int i = r; i < r + n; i++) {
                    for (int j = c; j < c + n; j++) {
                        A[i][j] = e + (j - c + i - r) % n;
                    }
                }
            }
        }
    }

    
    
    
    
    void solve() throws IOException {
        int T = readInt();
        for (int t = 0; t < T; t++) {
            int N = readInt();
            if (N == 1) {
                pw.println("Hooray");
                pw.println("1");
            } else if (N % 2 == 1) {
                pw.println("Boo");
            } else {
                
                
                int[][][] buckets = new int[N - 1][N / 2][];
                for (int i = 0; i <= N - 2; i++) {
                    buckets[i][0] = new int[]{N - 1, i};
                    for (int k = 1; k <= N / 2 - 1; k++) {
                        buckets[i][k] = new int[]{(i + k) % (N - 1), (i - k + N - 1) % (N - 1)};
                    }
                }
                int[][] A = new int[N][N];
                for (int i = 0; i < N; i++) A[i][i] = 1;
                for (int i = 0; i < buckets.length; i++) {
                    for (int[] pos : buckets[i]) {
                        A[pos[0]][pos[1]] = 2 + i;
                        A[pos[1]][pos[0]] = N + 1 + i;
                    }
                }
                pw.println("Hooray");
                for (int[] row : A) {
                    for (int x : row) {
                        pw.print(x + " ");
                    }
                    pw.println();
                }
            }
        }
    }
}




