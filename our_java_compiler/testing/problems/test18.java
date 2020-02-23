// @uthor -: puneet
// TimeStamp -: 11:55 PM - 11/01/20 

import java.io.*;
import java.util.*;

class Doofish implements Runnable {

    private boolean testCases=true;
    private boolean console=false;
    
    public void solve() {
        int n=in.ni();
        int[][] mat=new int[n][n];
        for(int i=0;i<n;++i){
            mat[i][i]=2*n-1;
        }
        int lstart = 0;
        int mod=2*n-1;
        for(int i=1;i<n;++i){
            int j=0;
            lstart+=2;
            int tstart=lstart;
            while(mat[i][j]==0){
                mat[i][j]=tstart%mod;
                if(tstart>mod) mat[i][j]++;
                tstart+=2;
                j++;
            }
        }
        int nn=4;
        for(int i=1;i<n-1;++i){
            mat[n-1][i]=nn%mod;
            if(nn>=mod)mat[n-1][i]++;
            nn+=4;
        }

        int rstart = -1;
        for(int i=1;i<n;++i){
            int j=0;
            rstart+=2;
            int tstart=rstart;
            while(mat[j][i]==0){
                mat[j][i]=tstart%mod;
                if(tstart>=mod) mat[j][i]++;
                tstart+=2;
                j++;
            }
        }

        nn=3;
        for(int i=1;i<n-1;++i){
            mat[i][n-1]=nn%mod;
            if(nn>=mod)mat[i][n-1]++;
            nn+=4;
        }

        boolean isok=check(mat,n,mod);
        if(isok) {
            out.println("Hooray");
            for (int i = 0; i < n; ++i) {
                for (int j = 0; j < n; ++j) {
                    out.print(mat[i][j] + " ");
                }
                out.println();
            }
        }else {
            out.println("Boo");
        }
    }

    private boolean check(int[][] mat, int n, int mod) {

        for(int i=0;i<n;++i){
            boolean[] isvis=new boolean[mod+1];
            for(int j=0;j<n;++j){
                isvis[mat[i][j]]=true;
                isvis[mat[j][i]]=true;
            }

            for(int j=1;j<=mod;++j){
                if(!isvis[j])
                    return false;
            }
        }

        return true;
    }

    /* -------------------- Templates and Input Classes -------------------------------*/

    @Override
    public void run() {
        try {
            init();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        int t= testCases ? in.ni() : 1;
        while (t-->0) {
            solve();
            out.flush();
        }
    }

    private FastInput in;
    private PrintWriter out;
    public static void main(String[] args) throws Exception {
        new Thread(null, new Doofish(), "Main", 1 << 27).start();
    }
    private void init() throws FileNotFoundException {
        InputStream inputStream = System.in;
        OutputStream outputStream = System.out;
        try {
            if (!console && System.getProperty("user.name").equals("puneet")) {
                outputStream = new FileOutputStream("/home/puneet/Desktop/output.txt");
                inputStream = new FileInputStream("/home/puneet/Desktop/input.txt");
            }
        } catch (Exception ignored) {
        }
        out = new PrintWriter(outputStream);
        in = new FastInput(inputStream);
    }
    private void sort(int[] arr) {
        List<Integer> list = new ArrayList<>();
        for (int object : arr) list.add(object);
        Collections.sort(list);
        for (int i = 0; i < list.size(); ++i) arr[i] = list.get(i);
    }
    private void sort(long[] arr) {
        List<Long> list = new ArrayList<>();
        for (long object : arr) list.add(object);
        Collections.sort(list);
        for (int i = 0; i < list.size(); ++i) arr[i] = list.get(i);
    }
    public long ModPow(long x, long y, long MOD) {
        long res = 1L;
        x = x % MOD;
        while (y >= 1) {
            if ((y & 1) > 0) res = (res * x) % MOD;
            x = (x * x) % MOD;
            y >>= 1;
        }
        return res;
    }
    public int gcd(int a, int b) {
        if (a == 0) return b;
        return gcd(b % a, a);
    }
    public long gcd(long a, long b) {
        if (a == 0) return b;
        return gcd(b % a, a);
    }
    static class FastInput { InputStream obj;
        public FastInput(InputStream obj) {
            this.obj = obj;
        }
        byte inbuffer[] = new byte[1024];
        int lenbuffer = 0, ptrbuffer = 0;
        int readByte() { if (lenbuffer == -1) throw new InputMismatchException();
            if (ptrbuffer >= lenbuffer) { ptrbuffer = 0;
                try { lenbuffer = obj.read(inbuffer);
                } catch (IOException e) { throw new InputMismatchException(); } }
            if (lenbuffer <= 0) return -1;return inbuffer[ptrbuffer++]; }
        String ns() { int b = skip();StringBuilder sb = new StringBuilder();
            while (!(isSpaceChar(b))) // when nextLine, (isSpaceChar(b) && b!=' ')
            { sb.appendCodePoint(b);b = readByte(); }return sb.toString();}
        int ni() {
            int num = 0, b;boolean minus = false;
            while ((b = readByte()) != -1 && !((b >= '0' && b <= '9') || b == '-')) ;
            if (b == '-') { minus = true;b = readByte(); }
            while (true) { if (b >= '0' && b <= '9') { num = num * 10 + (b - '0'); } else {
                    return minus ? -num : num; }b = readByte(); }}
        long nl() { long num = 0;int b;boolean minus = false;
            while ((b = readByte()) != -1 && !((b >= '0' && b <= '9') || b == '-')) ;
            if (b == '-') { minus = true;b = readByte(); }
            while (true) { if (b >= '0' && b <= '9') { num = num * 10L + (b - '0'); } else {
                    return minus ? -num : num; }b = readByte(); } }
        boolean isSpaceChar(int c) {
            return (!(c >= 33 && c <= 126));
        }
        int skip() { int b;while ((b = readByte()) != -1 && isSpaceChar(b)) ;return b; }
        float nf() {return Float.parseFloat(ns());}
        double nd() {return Double.parseDouble(ns());}
        char nc() {return (char) skip();}
    }

}