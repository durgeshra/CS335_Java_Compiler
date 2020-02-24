private void startCluster(Configuration  conf) throws Exception {
  if (System.getProperty("hadoop.log.dir") == null) {
    System.setProperty("hadoop.log.dir", "target/test-dir");
  }
  conf.set("dfs.block.access.token.enable", "false");
  conf.set("dfs.permissions", "true");
  conf.set("hadoop.security.authentication", "simple");
  String cp = conf.get(YarnConfiguration.YARN_APPLICATION_CLASSPATH,
      StringUtils.join(",",
          YarnConfiguration.DEFAULT_YARN_CROSS_PLATFORM_APPLICATION_CLASSPATH))
      + File.pathSeparator + classpathDir;
  conf.set(YarnConfiguration.YARN_APPLICATION_CLASSPATH, cp);
  dfsCluster = new MiniDFSCluster.Builder(conf).build();
  FileSystem fileSystem = dfsCluster.getFileSystem();
  fileSystem.mkdirs(new Path("/tmp"));
  fileSystem.mkdirs(new Path("/user"));
  fileSystem.mkdirs(new Path("/hadoop/mapred/system"));
  fileSystem.setPermission(
    new Path("/tmp"), FsPermission.valueOf("-rwxrwxrwx"));
  fileSystem.setPermission(
    new Path("/user"), FsPermission.valueOf("-rwxrwxrwx"));
  fileSystem.setPermission(
    new Path("/hadoop/mapred/system"), FsPermission.valueOf("-rwx------"));
  FileSystem.setDefaultUri(conf, fileSystem.getUri());
  mrCluster = MiniMRClientClusterFactory.create(this.getClass(), 1, conf);

  
  Writer writer = new FileWriter(classpathDir + "/core-site.xml");
  mrCluster.getConfig().writeXml(writer);
  writer.close();
}


