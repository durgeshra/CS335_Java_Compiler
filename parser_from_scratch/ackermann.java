class ackermann{
    int printInt ;
    int printInt(float n);

    int Ack(int m,int n, int k, int l){
    }

    int Ack(){
        int i = -1;
        int x = -1, y = -1;
        if (m==0) {
            if (m == 0) {
                i = n + 1;
            } else if (n == 0) {
                i = Ack(m - 1, 1);
            } else {
                j = Ack(m, n - 1);
                i = Ack(m - 1, j);
            }
        }
        return i;
    }
    public static void main(){
        int i = Ack(3,4);
        printInt(i);
    }
}
