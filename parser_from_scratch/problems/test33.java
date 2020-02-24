private static void addPath(
    @NullAllowed final String path,
    @NonNull Collection<? super FileObject> collector,
    final boolean modulepath) {
    if (path != null) {
        final StringTokenizer tok = new StringTokenizer(path, File.pathSeparator);
        while (tok.hasMoreTokens()) {
            final String binrootS = tok.nextToken();
            final File f = FileUtil.normalizeFile(new File(binrootS));
            final Collection<? extends File> toAdd = modulepath ?
                    collectModules(f) :
                    Collections.singleton(f);
            toAdd.forEach((e) -> {
                final URL binroot = FileUtil.urlForArchiveOrDir(f);
                if (binroot != null) {
                    final FileObject[] someRoots = SourceForBinaryQuery.findSourceRoots(binroot).getRoots();
                    Collections.addAll(collector, someRoots);
                }
            });
        }
    }
}
 









