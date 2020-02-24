public static void putPath(File path, String pathName, boolean prepend, Map<String, String> current) {
    String currentPath = current.get(pathName);

    if (currentPath == null) {
        currentPath = "";
    }

    if (prepend) {
        currentPath = path.getAbsolutePath().replace(" ", "\\ ") 
                + File.pathSeparator + currentPath;
    } else {
        currentPath = currentPath + File.pathSeparator
                + path.getAbsolutePath().replace(" ", "\\ "); 
    }

    if (!"".equals(currentPath.trim())) {
        current.put(pathName, currentPath);
    }
}
 


