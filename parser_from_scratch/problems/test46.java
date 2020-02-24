public static File[] decode(String text) {
    ArrayList<File> files = new ArrayList<File>();
    StringTokenizer tokenizer = new StringTokenizer(text, File.pathSeparator);
    while (tokenizer.hasMoreElements()) {
        File file = decodeFile((String) tokenizer.nextElement());
        files.add(file);
    }
    return files.toArray(new File[files.size()]);
}









