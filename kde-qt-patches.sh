# quick-n-dirty method to fetch patches from -patched git branch
# unfortunately, requires an already checked-out copy of the git repo

git format-patch --output-directory kde-qt-patches v4.6.0-beta..v4.6-stable-patched
