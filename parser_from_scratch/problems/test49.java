private ClassPath createClassPath(String classpath) {
    StringTokenizer tokenizer = new StringTokenizer(classpath, File.pathSeparator);
    List/*<PathResourceImplementation>*/ list = new ArrayList();
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
 Map<String, String> buildEnvironment(Map<String, String> original) {
    Map<String, String> ret = new HashMap<String, String>(original);
    ret.putAll(envVariables);

    // Find PATH environment variable - on Windows it can be some other
    // case and we should use whatever it has.
    String pathName = getPathName(original);

    // TODO use StringBuilder
    String currentPath = ret.get(pathName);

    if (currentPath == null) {
        currentPath = "";
    }

    for (File path : paths) {
        currentPath = path.getAbsolutePath().replace(" ", "\\ ") //NOI18N
                + File.pathSeparator + currentPath;
    }

    if (!"".equals(currentPath.trim())) {
        ret.put(pathName, currentPath);
    }
    return ret;
}
 