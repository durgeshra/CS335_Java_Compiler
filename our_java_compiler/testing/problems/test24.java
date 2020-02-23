    
    /**
     * Parse a parameter of the form "10,20,30" as an
     * RGB tuple for a color value.
     */
 1    Color getColor(String name) {
 2        String data;
 3        StringTokenizer st;
 4        int red, green, blue;
 5        
 6        data = getParameter(name);
 7        if (data == null)
 8            return null;
 9            
10        st = new StringTokenizer(data, ",");
11        try {
12            red = Integer.parseInt(st.nextToken());
13            green = Integer.parseInt(st.nextToken());
14            blue = Integer.parseInt(st.nextToken());
15        } catch (Exception e) {
16            return null; // (ERROR STATE) could not parse it
17        }
18        return new Color(red, green, blue); // (END STATE) done.
19    }