private ClassPath createClassPath(String classpath) {
    StringTokenizer tokenizer = new StringTokenizer(classpath, File.pathSeparator);
    List list = new ArrayList();
    while (tokenizer.hasMoreTokens()) {
        String item = tokenizer.nextToken();
        File f = FileUtil.normalizeFile(new File(item));
        URL url = getRootURL(f);
        if (url != null) {
            list.add(ClassPathSupport.createResource(url));
        }
    }
    return ClassPathSupport.createClassPath(list);
}
 




