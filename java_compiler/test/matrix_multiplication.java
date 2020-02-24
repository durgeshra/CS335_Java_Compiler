class matrix_multiplication{
    int printInt(int n);

    public static void main(){
        int i, j, k;
        int firstarray[][] = new int[2][2];
        int secondarray[][] = new int[2][2];
        firstarray[0][0] = 1;
        firstarray[0][1] = 2;
        firstarray[1][0] = 3;
        firstarray[1][1] = 4;
        secondarray[0][0] = 5;
        secondarray[0][1] = 6;
        secondarray[1][0] = 7;
        secondarray[1][1] = 8;
        
        int result[][] = new int[2][2];
        for (i = 0; i < 2; i++) {
            for (k = 0; k < 2; k++) {
                result[i][k] = 0;
            }
        }
        
        for (i = 0; i < 2; i++) {
            for (j = 0; j < 2; j++) {
                for (k = 0; k < 2; k++) {
                    result[i][j] =  result[i][j] + firstarray[i][k] * secondarray[k][j];
                }
            }
        }

        
        for (i = 0; i < 2; i++) {
            for (k = 0; k < 2; k++) {
                printInt(result[i][k]);
            }
        }
    }
}



