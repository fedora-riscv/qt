! /bin/bash
#
# In multilib environments there is a preferred architecture, 64 bit over 32 bit in x86_64,
# 32 bit over 64 bit in ppc64. When a conflict is found between two packages corresponding
# with different arches, the installed file is the one from the preferred arch. This is
# very common for executables in /usr/bin, for example. If the file /usr/bin/foo is found
# in an x86_64 package and in an i386 package, the executable from x86_64 will be installe

ARCH=$(uname -m)
QTVERSION=4

if [ -z "$QT4DIR" ] ; then
   case $ARCH in
      x86_64 | ia64 | s390 )
         QT4DIR=/usr/lib64/qt$QTVERSION ;;
      * )
         QT4DIR=/usr/lib/qt$QTVERSION ;;
   esac
   export QT4DIR
fi

if ! echo ${PATH} | /bin/grep -q $QT4DIR/bin ; then
 PATH=${QT4DIR}/bin:${PATH}
 export PATH
fi

exec $QT4DIR/bin/`basename $0` ${1+"$@"}

