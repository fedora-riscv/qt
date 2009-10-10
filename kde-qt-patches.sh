# quick-n-dirty method to fetch patches from -patched git branch
# unfortunately, requires an already checked-out copy of the git repo

git format-patch --output-directory kde-qt-patches v4.5.3..4.5.3-patched
