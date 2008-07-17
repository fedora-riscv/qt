# Qt4 initialization script (csh)

if ( $?QT4DIR ) then
   exit
endif

setenv QT4DIR `/usr/bin/pkg-config --variable=prefix Qt` 
setenv QT4DOCDIR `/usr/bin/pkg-config --variable=docdir Qt` 
