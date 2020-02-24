



public static boolean commandIsAvailable(final String command) {
  try {
    final String quotedCommand = StringUtils.putIntoDoubleQuotes(command);
    final String[] parsed = new CommandLineParser().parse(quotedCommand);
    if (parsed.length != 1) return false; 
    final File commmandFile = new File(parsed[0]);
    
    if (!commmandFile.isAbsolute()) {
      final String pathVariable = getEnvVariable(isWindows() ? "Path" : "PATH");
      final StringTokenizer stPath = new StringTokenizer(pathVariable, File.pathSeparator, false);
      while (stPath.hasMoreTokens()) {
        String commandToCheck = null;
        if (isWindows() && !command.endsWith(EXE_SUFFIX)) {
          commandToCheck = command + EXE_SUFFIX;
        } else {
          commandToCheck = command;
        }
        final String path = stPath.nextToken();
        final File fullPath = new File(path, commandToCheck);
        if (fullPath.exists() && fullPath.isFile()) return true;
      }
    }
    if (!commmandFile.exists()) return false;
    return commmandFile.isFile();
  } catch (CommandLineParserException e) {
    return false;
  }
}









