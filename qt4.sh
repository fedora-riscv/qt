# Qt4 initialization script (sh)

if [ -z "$QMAKESPEC" ] ; then
  QMAKESPEC=@@QMAKESPEC@@ 
  export QMAKESPEC

fi

