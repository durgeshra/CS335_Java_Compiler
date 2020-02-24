String toClasspath(final boolean includeSystemClasspath, String[] jarFilePathnames,
    String... userClasspaths) {
  // gemfire jar must absolutely be the first JAR file on the CLASSPATH!!!
  String classpath = getGemFireJarPath();

  userClasspaths = (userClasspaths != null ? userClasspaths : StringUtils.EMPTY_STRING_ARRAY);

  // Then, include user-specified classes on CLASSPATH to enable the user to override GemFire JAR
  // dependencies
  // with application-specific versions; this logic/block corresponds to classes/jar-files
  // specified with the
  // --classpath option to the 'start locator' and 'start server commands'; also this will
  // override any
  // System CLASSPATH environment variable setting, which is consistent with the Java platform
  // behavior...
  for (String userClasspath : userClasspaths) {
    if (!StringUtils.isBlank(userClasspath)) {
      classpath += (classpath.isEmpty() ? StringUtils.EMPTY_STRING : File.pathSeparator);
      classpath += userClasspath;
    }
  }

  // Now, include any System-specified CLASSPATH environment variable setting...
  if (includeSystemClasspath) {
    classpath += File.pathSeparator;
    classpath += getSystemClasspath();
  }

  jarFilePathnames =
      (jarFilePathnames != null ? jarFilePathnames : StringUtils.EMPTY_STRING_ARRAY);

  // And finally, include all GemFire dependencies on the CLASSPATH...
  for (String jarFilePathname : jarFilePathnames) {
    if (!StringUtils.isBlank(jarFilePathname)) {
      classpath += (classpath.isEmpty() ? StringUtils.EMPTY_STRING : File.pathSeparator);
      classpath += jarFilePathname;
    }
  }

  return classpath;
}