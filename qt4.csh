# Qt4 initialization script (csh)

if ( $?QMAKESPEC ) then
   exit
endif

setenv QMAKESPEC @@QMAKESPEC@@ 

