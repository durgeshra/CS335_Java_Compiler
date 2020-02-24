import java.util.*;
import java.io.*;
import java.text.*;

public class Main{

    void pre() throws Exception{}
    int[][][] D = new int[][][]{
        {{2,-2,0}, {1,0,-2}, {2,1,0}, {1,0,1}},
        {{1,-1,0}, {1,1,0}, {0,0,-1},{0,0,2}},
        {{0,-1,0}, {0,2,0}, {2,0,-1},{2,0,1}}
    };
    void solve(int TC) throws Exception{
        int n = ni(), m = ni();
        int x = ni()-1, y = ni()-1;
        boolean[][][] vis = new boolean[3][n][m];
        boolean[][] val = new boolean[n][m];
        int[][] ans = new int[n][m];
        for(int i = 0; i< n; i++){
            String s = n();
            for(int j= 0; j< m; j++){
                val[i][j] = s.charAt(j)=='1';
                ans[i][j] = INF;
            }
        }
        PriorityQueue<State> q = new PriorityQueue<>();
        q.add(new State(0, x, y, 0));
        ans[x][y] = 0;
        vis[0][x][y] = true;
        while(!q.isEmpty()){
            State s = q.poll();
            for(int[] d:D[s.st]){
                int xx = s.x+d[1], yy = s.y+d[2];
                if(xx<0 || xx>= n || yy<0 || yy>= m || vis[d[0]][xx][yy])continue;
                if(!check(val, d[0], xx, yy,n,m))continue;
                State ss = new State(d[0], xx, yy, s.di+1);
                q.add(ss);
                vis[d[0]][xx][yy] = true;
                if(d[0]==0)ans[xx][yy] = Math.min(ans[xx][yy], ss.di);
            }
        }
        for(int i = 0; i< n; i++){
            for(int j = 0; j< m; j++)p((ans[i][j]==INF?-1:ans[i][j])+" ");pn("");
        }
    }
    boolean check(boolean[][] val, int st, int x, int y, int n, int m){
        if(st==0)return val[x][y];
        else if(st==1)return val[x][y] && y+1<m && val[x][y+1];
        else if(st==2)return val[x][y] && x+1<n && val[x+1][y];
        return false;
    }
    class State implements Comparable<State>{
        int x, y, st, di;
        public State(int ST, int X, int Y, int D){
            st=ST;x=X;y=Y;di=D;
        }
        public int compareTo(State s){
            return Integer.compare(di, s.di);
        }
        public String toString(){
            return "state = "+st+" pos "+x+" "+y +" dis "+di;
        }
    }

    void hold(boolean b)throws Exception{if(!b)throw new Exception("Hold right there, Sparky!");}
    long mod = (long)1e9+7, IINF = (long)1e18;
    final int INF = (int)1e9, MX = (int)3e5+1;
    DecimalFormat df = new DecimalFormat("0.00000000000");
    double PI = 3.1415926535897932384626433832792884197169399375105820974944, eps = 1e-8;
    static boolean multipleTC = true, memory = false;
    FastReader in;PrintWriter out;
    void run() throws Exception{
        in = new FastReader();
        out = new PrintWriter(System.out);
        int T = (snksn)?ni:1;

        pre();for(int t = 1; t<= T; t++)solve(t);
        out.flush();
        out.close();
    }
    public static void main(String[] args) throws Exception{
        if(memory)new Thread(null, new Runnable() {public void run(){try{new Main().run();}catch(Exception e){e.printStackTrace();}}}, "1", 1 << 28).start();
        else new Main().run();
    }
    long gcd(long a, long b){return (b==0)?a:gcd(b,a%b);}
    int gcd(int a, int b){return (b==0)?a:gcd(b,a%b);}
    int bit(long n){return (n==0)?0:(1+bit(n&(n-1)));}
    void p(Object o){out.print(o);}
    void pn(Object o){out.println(o);}
    void pni(Object o){out.println(o);out.flush();}
    String n()throws Exception{return in.next();}
    String nln()throws Exception{return in.nextLine();}
    int ni()throws Exception{return Integer.parseInt(in.next());}
    long nl()throws Exception{return Long.parseLong(in.next());}
    double nd()throws Exception{return Double.parseDouble(in.next());}

    class FastReader{
        BufferedReader br;
        StringTokenizer st;
        public FastReader(){
            br = new BufferedReader(new InputStreamReader(System.in));
        }

        public FastReader(String s) throws Exception{
            br = new BufferedReader(new FileReader(s));
        }

        String next() throws Exception{
            while (st == null || !st.hasMoreElements()){
                try{
                    st = new StringTokenizer(br.readLine());
                }catch (IOException  e){
                    throw new Exception(e.toString());
                }
            }
            return st.nextToken();
        }

        String nextLine() throws Exception{
            String str = "";
            try{
                str = br.readLine();
            }catch (IOException e){
                throw new Exception(e.toString());
            }
            return str;
        }
    }
}







