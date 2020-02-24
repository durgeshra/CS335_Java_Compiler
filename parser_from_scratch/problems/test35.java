Map<String, String> buildEnvironment(Map<String, String> original) {
    Map<String, String> ret = new HashMap<String, String>(original);
    ret.putAll(envVariables);

    
    
    String pathName = getPathName(original);

    
    String currentPath = ret.get(pathName);

    if (currentPath == null) {
        currentPath = "";
    }

    for (File path : paths) {
        currentPath = path.getAbsolutePath().replace(" ", "\\ ") 
                + File.pathSeparator + currentPath;
    }

    if (!"".equals(currentPath.trim())) {
        ret.put(pathName, currentPath);
    }
    return ret;
}
 




