

package Fall0811;
import java.util.Iterator;

public class GenericList<E> implements Iterable<E>{
 
    private static final int DEFAULT_CAP = 10;
 
    
    protected E[] container; 
    private int listSize;
    
    public Iterator<E> iterator(){
        return new GenListIterator();
    }
    
    
    private class GenListIterator implements Iterator<E>{
        private int indexOfNextElement;
        private boolean okToRemove;
        
        private GenListIterator(){
            indexOfNextElement = 0;
            okToRemove = false;
        }
    }   
}







