package divideconquer;









public final class ClosestPair {


    


    int numberPoints = 0;
    


    private Location[] array;
    


    Location point1 = null;
    


    Location point2 = null;
    


    private static double minNum = Double.MAX_VALUE;
    


    private static int secondCount = 0;

    


    ClosestPair(int points) {
        numberPoints = points;
        array = new Location[numberPoints];
    }

    



    public static class Location {

        double x = 0;
        double y = 0;

        




        Location(final double xpar, final double ypar) { 
            this.x = xpar;
            this.y = ypar;
        }

    }

    public Location[] createLocation(int numberValues) {
        return new Location[numberValues];

    }

    public Location buildLocation(double x, double y) {
        return new Location(x, y);
    }


    








    public int xPartition(
            final Location[] a, final int first, final int last) {

        Location pivot = a[last]; 
        int pIndex = last;
        int i = first - 1;
        Location temp; 
        for (int j = first; j <= last - 1; j++) {
            if (a[j].x <= pivot.x) { 
                i++;
                temp = a[i]; 
                a[i] = a[j];
                a[j] = temp;
            }
        }
        i++;
        temp = a[i]; 
        a[i] = a[pIndex];
        a[pIndex] = temp;
        return i; 
    }

    








    public int yPartition(
            final Location[] a, final int first, final int last) {

        Location pivot = a[last]; 
        int pIndex = last;
        int i = first - 1;
        Location temp; 
        for (int j = first; j <= last - 1; j++) {
            if (a[j].y <= pivot.y) { 
                i++;
                temp = a[i]; 
                a[i] = a[j];
                a[j] = temp;
            }
        }
        i++;
        temp = a[i]; 
        a[i] = a[pIndex];
        a[pIndex] = temp;
        return i; 
    }

    







    public void xQuickSort(
            final Location[] a, final int first, final int last) {

        if (first < last) {
            int q = xPartition(a, first, last); 
            xQuickSort(a, first, q - 1); 
            xQuickSort(a, q + 1, last); 
        }
    }

    







    public void yQuickSort(
            final Location[] a, final int first, final int last) {

        if (first < last) {
            int q = yPartition(a, first, last); 
            yQuickSort(a, first, q - 1); 
            yQuickSort(a, q + 1, last); 
        }
    }

    







    public double closestPair(final Location[] a, final int indexNum) {

        Location[] divideArray = new Location[indexNum];
        System.arraycopy(a, 0, divideArray, 0, indexNum); 
        int totalNum = indexNum; 
        int divideX = indexNum / 2; 
        Location[] leftArray = new Location[divideX]; 
        
        Location[] rightArray = new Location[totalNum - divideX];
        if (indexNum <= 3) { 
            return bruteForce(divideArray);
        }
        
        System.arraycopy(divideArray, 0, leftArray, 0, divideX);
        
        System.arraycopy(
                divideArray, divideX, rightArray, 0, totalNum - divideX);

        double minLeftArea = 0; 
        double minRightArea = 0; 
        double minValue = 0; 

        minLeftArea = closestPair(leftArray, divideX); 
        minRightArea = closestPair(rightArray, totalNum - divideX);
        
        minValue = Math.min(minLeftArea, minRightArea);

        
        
        for (int i = 0; i < totalNum; i++) {
            double xGap = Math.abs(divideArray[divideX].x - divideArray[i].x);
            if (xGap < minValue) {
                secondCount++; 
            } else {
                if (divideArray[i].x > divideArray[divideX].x) {
                    break;
                }
            }
        }
        
        Location[] firstWindow = new Location[secondCount];
        int k = 0;
        for (int i = 0; i < totalNum; i++) {
            double xGap = Math.abs(divideArray[divideX].x - divideArray[i].x);
            if (xGap < minValue) { 
                firstWindow[k] = divideArray[i]; 
                k++;
            } else {
                if (divideArray[i].x > divideArray[divideX].x) {
                    break;
                }
            }
        }
        yQuickSort(firstWindow, 0, secondCount - 1); 
        
        double length = 0;
        
        for (int i = 0; i < secondCount - 1; i++) {
            for (int j = (i + 1); j < secondCount; j++) {
                double xGap = Math.abs(firstWindow[i].x - firstWindow[j].x);
                double yGap = Math.abs(firstWindow[i].y - firstWindow[j].y);
                if (yGap < minValue) {
                    length = Math.sqrt(Math.pow(xGap, 2) + Math.pow(yGap, 2));
                    
                    if (length < minValue) {
                        
                        minValue = length;
                        
                        if (length < minNum) {
                            minNum = length;
                            point1 = firstWindow[i];
                            point2 = firstWindow[j];
                        }
                    }
                } else {
                    break;
                }
            }
        }
        secondCount = 0;
        return minValue;
    }

    






    public double bruteForce(final Location[] arrayParam) {

        double minValue = Double.MAX_VALUE; 
        double length = 0;
        double xGap = 0; 
        double yGap = 0; 
        double result = 0;

        if (arrayParam.length == 2) {
            
            xGap = (arrayParam[0].x - arrayParam[1].x);
            
            yGap = (arrayParam[0].y - arrayParam[1].y);
            
            length = Math.sqrt(Math.pow(xGap, 2) + Math.pow(yGap, 2));
            
            if (length < minNum) {
                minNum = length;

            }
            point1 = arrayParam[0];
            point2 = arrayParam[1];
            result = length;
        }
        if (arrayParam.length == 3) {
            for (int i = 0; i < arrayParam.length - 1; i++) {
                for (int j = (i + 1); j < arrayParam.length; j++) {
                    
                    xGap = (arrayParam[i].x - arrayParam[j].x);
                    
                    yGap = (arrayParam[i].y - arrayParam[j].y);
                    
                    length =
                            Math.sqrt(Math.pow(xGap, 2) + Math.pow(yGap, 2));
                    
                    if (length < minValue) {
                        
                        minValue = length;
                        if (length < minNum) {
                            
                            minNum = length;
                            point1 = arrayParam[i];
                            point2 = arrayParam[j];
                        }
                    }
                }
            }
            result = minValue;

        }
        return result; 
    }

    







    public static void main(final String[] args) {

        

        ClosestPair cp = new ClosestPair(12);
        cp.array[0] = cp.buildLocation(2, 3);
        cp.array[1] = cp.buildLocation(2, 16);
        cp.array[2] = cp.buildLocation(3, 9);
        cp.array[3] = cp.buildLocation(6, 3);
        cp.array[4] = cp.buildLocation(7, 7);
        cp.array[5] = cp.buildLocation(19, 4);
        cp.array[6] = cp.buildLocation(10, 11);
        cp.array[7] = cp.buildLocation(15, 2);
        cp.array[8] = cp.buildLocation(15, 19);
        cp.array[9] = cp.buildLocation(16, 11);
        cp.array[10] = cp.buildLocation(17, 13);
        cp.array[11] = cp.buildLocation(9, 12);

        System.out.println("Input data");
        System.out.println("Number of points: " + cp.array.length);
        for (int i = 0; i < cp.array.length; i++) {
            System.out.println("x: " + cp.array[i].x + ", y: " + cp.array[i].y);
        }

        cp.xQuickSort(cp.array, 0, cp.array.length - 1); 

        double result; 

        result = cp.closestPair(cp.array, cp.array.length);
        
        
        System.out.println("Output Data");
        System.out.println("(" + cp.point1.x + ", " + cp.point1.y + ")");
        System.out.println("(" + cp.point2.x + ", " + cp.point2.y + ")");
        System.out.println("Minimum Distance : " + result);

    }
}



