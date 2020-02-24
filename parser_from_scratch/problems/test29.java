String toClasspath(final boolean includeSystemClasspath, String[] jarFilePathnames,
    String... userClasspaths) {
  
  String classpath = getGemFireJarPath();

  userClasspaths = (userClasspaths != null ? userClasspaths : StringUtils.EMPTY_STRING_ARRAY);

  
  
  
  
  
  
  
  
  for (String userClasspath : userClasspaths) {
    if (!StringUtils.isBlank(userClasspath)) {
      classpath += (classpath.isEmpty() ? StringUtils.EMPTY_STRING : File.pathSeparator);
      classpath += userClasspath;
    }
  }

  
  if (includeSystemClasspath) {
    classpath += File.pathSeparator;
    classpath += getSystemClasspath();
  }

  jarFilePathnames =
      (jarFilePathnames != null ? jarFilePathnames : StringUtils.EMPTY_STRING_ARRAY);

  
  for (String jarFilePathname : jarFilePathnames) {
    if (!StringUtils.isBlank(jarFilePathname)) {
      classpath += (classpath.isEmpty() ? StringUtils.EMPTY_STRING : File.pathSeparator);
      classpath += jarFilePathname;
    }
  }

  return classpath;
}


