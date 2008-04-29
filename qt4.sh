# Qt4 initialization script (sh)

if [ -z "$QT4DIR" ] ; then
  QT4DIR=`/usr/bin/pkg-config --variable=prefix Qt`
  QT4DOCDIR=`/usr/bin/pkg-config --variable=docdir Qt`

  export QT4DIR QT4DOCDIR
fi

