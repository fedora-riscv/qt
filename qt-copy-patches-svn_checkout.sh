#!/bin/bash

DATE=$(date +%Y%m%d)
EXPORT_DIR=qt-copy

set -x
rm -rf $EXPORT_DIR

# app
svn export --non-recursive svn://anonsvn.kde.org/home/kde/branches/qt/4.3 $EXPORT_DIR/
svn export svn://anonsvn.kde.org/home/kde/branches/qt/4.3/patches $EXPORT_DIR/patches

pushd $EXPORT_DIR
rm -f ../qt-copy-patches-${DATE}svn.tar.bz2
tar cjf ../qt-copy-patches-${DATE}svn.tar.bz2 \
  .applied_patches apply_patches README.qt-copy patches/ 
popd

# cleanup
rm -rf $EXPORT_DIR

