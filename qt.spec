%define smp 1

%define desktop_file 1
%define redhat_artwork 1
%define desktop_file_utils_version 0.2.93

%define mysql4 1

%define immodule 1

%define ver 3.3.4

%define qt_dirname qt-3.3
%define qtdir %{_libdir}/%{qt_dirname}

# build Motif extention
%define motif_extention 0

# pkg-config
%define pkg_config 1

# install manuals
%define installman 1

# buildmysql: Build MySQL plugins
%define buildmysql 1

# buildpsql: Build Postgres plugins
%define buildpsql 1

# buildodbc: Build ODBC plugins
%define buildodbc 1

# buildmt: Build libs with threading support
%define buildmt 1

# cups support
%define cups 1

%define debug 0

%define sover %{ver}

%define styleplugins 0

%if %{styleplugins}
%define plugins_style -plugin-style-cde -plugin-style-motifplus -plugin-style-platinum -plugin-style-sgi -plugin-style-windows -plugin-style-compact -qt-imgfmt-png -qt-imgfmt-jpeg -qt-imgfmt-mng
%else
%define plugins_style -qt-style-cde -qt-style-motifplus -qt-style-platinum -qt-style-sgi -qt-style-windows -qt-style-compact -qt-imgfmt-png -qt-imgfmt-jpeg -qt-imgfmt-mng
%endif

%if %{buildmysql}
%define plugin_mysql -plugin-sql-mysql
%else
%define plugin_mysql %{nil}
%endif

%if %{mysql4}
%define mysql_include_dir %{_includedir}/mysql
%define mysql_lib_dir %{_libdir}/mysql
%define mysql_buildreq mysql-devel
%else
%define mysql_include_dir %{_includedir}/mysql3/mysql
%define mysql_lib_dir %{_libdir}/mysql3/mysql
%define mysql_buildreq mysqlclient10-devel
%endif

%if %{buildpsql}
%define plugin_psql -plugin-sql-psql
%else
%define plugin_psql %{nil}
%endif

%if %{buildodbc}
%define plugin_odbc -plugin-sql-odbc
%else
%define plugin_odbc %{nil}
%endif

%define plugins %{plugin_mysql} %{plugin_psql} %{plugin_odbc} %{plugins_style}

Summary: The shared library for the Qt GUI toolkit.
Name: qt
Version: %{ver}
Release: 8
Epoch: 1
License: GPL/QPL
Group: System Environment/Libraries
Buildroot: %{_tmppath}/%{name}-root
Url: http://www.troll.no
Source: ftp://ftp.troll.no/qt/source/qt-x11-free-%{version}.tar.bz2
Source1: qtrc

Patch1: qt-3.3.4-print-CJK.patch
Patch2: qt-3.0.5-nodebug.patch
Patch3: qt-3.1.0-makefile.patch
Patch5: qt-x11-free-3.3.0-strip.patch
Patch7: qt-x11-free-3.3.2-quiet.patch
Patch8: qt-x11-free-3.3.3-qembed.patch
Patch12: qt-uic-nostdlib.patch
Patch13: qt-x11-free-3.3.4-qfontdatabase_x11.patch
Patch14: qt-x11-free-3.3.3-gl.patch
Patch16: qt-x11-free-3.3.4-fullscreen.patch
Patch17: qt-x11-free-3.3.4-gcc4.patch

# immodule patches
Patch50: qt-x11-immodule-unified-qt3.3.4-20041203.diff.bz2
Patch51: qximinputcontext_x11.cpp.patch
Patch52: qt-x11-free-3.3.3-immodule-quiet.patch
Patch53: qt-x11-free-3.3.3-immodule-qinputcontext.patch
Patch54: qt-x11-free-3.3.4-immodule-xim.patch

# qt-copy patches
Patch100: 0048-qclipboard_hack_80072.patch

Prefix: %{qtdir}

Prereq: /sbin/ldconfig
Prereq: fileutils

Requires: fontconfig >= 2.0
Requires: /etc/ld.so.conf.d

BuildRequires: gcc-c++
BuildRequires: libstdc++-devel
BuildRequires: libmng-devel
BuildRequires: glibc-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: zlib-devel
BuildRequires: libungif-devel
BuildRequires: perl
BuildRequires: sed
BuildRequires: findutils
BuildRequires: xorg-x11-devel
BuildRequires: cups-devel
BuildRequires: tar

%if %{motif_extention}
BuildRequires: openmotif-devel >= 2.2.2
%endif

%if %{desktop_file}
BuildRequires: desktop-file-utils >= %{desktop_file_utils_version}
%endif

%if %{buildmysql}
BuildRequires: %{mysql_buildreq}
%endif

%if %{buildpsql}
BuildRequires: postgresql-devel
%endif

%if %{buildodbc}
BuildRequires: unixODBC-devel
%endif

BuildRequires: fontconfig-devel >= 2.0


%package config
Summary: Grapical configuration tool for programs using Qt
Group: User Interface/Desktops
Requires: %{name} = %{epoch}:%{version}-%{release}


%package devel
Summary: Development files and documentation for the Qt GUI toolkit.
Group: Development/Libraries
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: xorg-x11-devel
Requires: libpng-devel
Requires: libjpeg-devel
Requires: libmng-devel


%package Xt
Summary: An Xt (X Toolkit) compatibility add-on for the Qt GUI toolkit.
Group: System Environment/Libraries
Requires: %{name} = %{epoch}:%{version}-%{release}


%package styles
Summary: Extra styles for the Qt GUI toolkit.
Group: User Interface/Desktops
Requires: %{name} = %{epoch}:%{version}-%{release}


%if %{buildodbc}
%package ODBC
Summary: ODBC drivers for Qt's SQL classes.
Group: System Environment/Libraries
Requires: %{name} = %{epoch}:%{version}-%{release}
%endif


%if %{buildmysql}
%package MySQL
Summary: MySQL drivers for Qt's SQL classes.
Group: System Environment/Libraries
Requires: %{name} = %{epoch}:%{version}-%{release}
%endif


%if %{buildpsql}
%package PostgreSQL
Summary: PostgreSQL drivers for Qt's SQL classes.
Group: System Environment/Libraries
Requires: %{name} = %{epoch}:%{version}-%{release}
%endif


%package static
Summary: Version of the Qt GUI toolkit for static linking
Group: Development/Libraries
Requires: %{name}-devel = %{epoch}:%{version}-%{release}


%package designer
Summary: Interface designer (IDE) for the Qt toolkit
Group: Development/Tools
Requires: %{name}-devel = %{epoch}:%{version}-%{release}


%description
Qt is a GUI software toolkit which simplifies the task of writing and
maintaining GUI (Graphical User Interface) applications
for the X Window System.

Qt is written in C++ and is fully object-oriented.

This package contains the shared library needed to run qt
applications, as well as the README files for qt.


%description config
Qt is a GUI software toolkit which simplifies the task of writing and
maintaining GUI (Graphical User Interface) applications
for the X Window System.

Qt is written in C++ and is fully object-oriented.

This package contains a grapical configuration tool for programs using Qt.


%description devel
The qt-devel package contains the files necessary to develop
applications using the Qt GUI toolkit: the header files, the Qt meta
object compiler, the man pages, the HTML documentation and example
programs.

Install qt-devel if you want to develop GUI applications using the Qt
toolkit.


%description Xt
An Xt (X Toolkit) compatibility add-on for the Qt GUI toolkit.


%description static
Version of the Qt library for static linking


%description styles
Extra styles (themes) for the Qt GUI toolkit.


%if %{buildodbc}
%description ODBC
ODBC driver for Qt's SQL classes (QSQL)
%endif


%if %{buildmysql}
%description MySQL
MySQL driver for Qt's SQL classes (QSQL)
%endif


%if %{buildpsql}
%description PostgreSQL
PostgreSQL driver for Qt's SQL classes (QSQL)
%endif


%description designer
The qt-designer package contains an User Interface designer tool
for the Qt toolkit.


%prep
%setup -q -n %{name}-x11-free-%{version}
%patch1 -p1 -b .cjk
%patch2 -p1 -b .ndebug
%patch3 -p1 -b .makefile
%patch5 -p1
%patch7 -p1 -b .quiet
%patch8 -p1 -b .qembed
%patch12 -p1 -b .nostdlib
%patch13 -p1 -b .fonts
%patch14 -p1 -b .gl
%patch16 -p1 -b .size
%patch17 -p1 -b .gcc4

%if %{immodule}
%patch50 -p1
%patch51 -p0 -b .qximinputcontext_x11
%patch52 -p1 -b .quiet
%patch53 -p1 -b .im
%patch54 -p1 -b .xim
%endif

%patch100 -p0 -b .klipper

# convert to UTF-8
iconv -f iso-8859-1 -t utf-8 < doc/man/man3/qdial.3qt > doc/man/man3/qdial.3qt_
mv doc/man/man3/qdial.3qt_ doc/man/man3/qdial.3qt

%build
export QTDIR=`/bin/pwd`
export LD_LIBRARY_PATH="$QTDIR/lib:$LD_LIBRARY_PATH"
export PATH="$QTDIR/bin:$PATH"
export QTDEST=%{qtdir}

%if %{smp}
   export SMP_MFLAGS="%{?_smp_mflags}"
%endif

%if %{immodule}
   sh ./make-symlinks.sh
%endif

# set some default FLAGS
%ifarch ia64
OPTFLAGS="-O0"
%else
OPTFLAGS="$RPM_OPT_FLAGS"
%endif

# don't use rpath
perl -pi -e "s|-Wl,-rpath,| |" mkspecs/*/qmake.conf

# set correct FLAGS
perl -pi -e "s|-O2|$INCLUDES $OPTFLAGS|g" mkspecs/*/qmake.conf

# set correct lib path
if [ "%{_lib}" == "lib64" ] ; then
   perl -pi -e "s,/lib, /%{_lib},g" config.tests/unix/{checkavail,cups.test,nis.test}
fi

# build shared, threaded (default) libraries
echo yes | ./configure \
  -prefix $QTDEST \
  -docdir %{_docdir}/qt-devel-%{version}/ \
%if %{_lib} == lib64
  -platform linux-g++-64 \
%else
  -platform linux-g++ \
%endif
%if %{debug}
  -debug \
%else
  -release \
%endif
  -shared \
  -largefile \
  -qt-gif \
  -system-zlib \
  -system-libpng \
  -system-libmng \
  -system-libjpeg \
  -no-g++-exceptions \
  -enable-styles \
  -enable-tools \
  -enable-kernel \
  -enable-widgets \
  -enable-dialogs \
  -enable-iconview \
  -enable-workspace \
  -enable-network \
  -enable-canvas \
  -enable-table \
  -enable-xml \
  -enable-opengl \
  -enable-sql \
  -qt-style-motif \
  %{plugins} \
  -stl \
%if %{buildmt}
  -thread \
%endif
%if %{cups}
  -cups \
%endif
  -sm \
%if "%{xfree_xinerame}" == "0"
  -L`pwd`/Xinerama \
%endif
  -xinerama \
  -xrender \
  -xkb \
  -ipv6 \
  -dlopen-opengl \
  -xft

make $SMP_MFLAGS src-qmake

# build psql plugin
%if %{buildpsql}
   pushd plugins/src/sqldrivers/psql
   qmake -o Makefile "INCLUDEPATH+=%{_includedir}/pgsql %{_includedir}/pgsql/server %{_includedir}/pgsql/internal" "LIBS+=-lpq" psql.pro
popd
%endif

# build mysql plugin
%if %{buildmysql}
   pushd plugins/src/sqldrivers/mysql
   qmake -o Makefile "INCLUDEPATH+=%{mysql_include_dir}" "LIBS+=-L%{mysql_lib_dir} -lmysqlclient" mysql.pro
popd
%endif

# build odbc plugin
%if %{buildodbc}
   pushd plugins/src/sqldrivers/odbc
   qmake -o Makefile "LIBS+=-lodbc" odbc.pro
   popd
%endif

make $SMP_MFLAGS src-moc
make $SMP_MFLAGS sub-src
make $SMP_MFLAGS sub-tools UIC="$QTDIR/bin/uic -nostdlib -L $QTDIR/plugins"

# build Xt/Motif Extention
%if %{motif_extention}
   make -C extensions/motif/src $SMP_MFLAGS
%endif

%install
rm -rf %{buildroot}

export QTDIR=`/bin/pwd`
export LD_LIBRARY_PATH="$QTDIR/lib:$LD_LIBRARY_PATH"
export PATH="$QTDIR/bin:$PATH"
export QTDEST=%{qtdir}

make install INSTALL_ROOT=%{buildroot}

for i in findtr qt20fix qtrename140 lrelease lupdate ; do
   install bin/$i %{buildroot}%{qtdir}/bin/
done

%if ! %{pkg_config}
   rm -rf %{buildroot}%{_libdir}/pkgconfig
%else
   mkdir -p  %{buildroot}%{_libdir}/pkgconfig
   pushd %{buildroot}%{_libdir}/pkgconfig
   ln -sf ../%{qt_dirname}/lib/pkgconfig/* .
popd
%endif

# install man pages
%if %{installman}
  mkdir -p %{buildroot}%{_mandir}
  cp -fR doc/man/* %{buildroot}%{_mandir}/
%endif

# clean up
make -C tutorial clean
make -C examples clean

# Make sure the examples can be built outside the source tree.
# Our binaries fulfill all requirements, so...
perl -pi -e "s,^DEPENDPATH.*,,g;s,^REQUIRES.*,,g" `find examples -name "*.pro"`

# don't include Makefiles of qt examples/tutorials
find examples -name "Makefile" | xargs rm -f
find examples -name "*.obj" | xargs rm -rf
find examples -name "*.moc" | xargs rm -rf
find tutorial -name "Makefile" | xargs rm -f

for a in */*/Makefile ; do
  sed 's|^SYSCONF_MOC.*|SYSCONF_MOC		= %{qtdir}/bin/moc|' < $a > ${a}.2
  mv -v ${a}.2 $a
done

mkdir -p %{buildroot}/etc/profile.d
cat > %{buildroot}/etc/profile.d/qt.sh <<EOF
# Qt initialization script (sh)
if [ -z "\$QTDIR" ] ; then
	QTDIR="%{qtdir}"
fi
export QTDIR
EOF

cat > %{buildroot}/etc/profile.d/qt.csh <<EOF
# Qt initialization script (csh)
if ( \$?QTDIR ) then
         exit
endif
setenv QTDIR %{qtdir}
EOF

chmod 755 %{buildroot}/etc/profile.d/*

mkdir -p %{buildroot}%{_bindir}
for i in bin/*; do
	ln -s ../%{_lib}/%{qt_dirname}/bin/`basename $i` %{buildroot}/%{_bindir}
done

# Add desktop file
%if %{desktop_file}
   mkdir -p %{buildroot}%{_datadir}/applications
   cat >%{buildroot}%{_datadir}/applications/qt-designer.desktop <<EOF
%else
   mkdir -p %{buildroot}%{_datadir}/applnk/Development
   cat >%{buildroot}%{_datadir}/applnk/Development/designer.desktop <<EOF
%endif
[Desktop Entry]
BinaryPattern=designer;
Name=Qt Designer
GenericName=Interface Designer
Exec=designer
Icon=designer
InitialPreference=5
MapNotify=true
MimeType=application/x-designer
Terminal=false
Encoding=UTF-8
Type=Application
Categories=Application;Development;X-Red-Hat-Extra;
X-Desktop-File-Install-Version=0.3
EOF

# move it into redhat-artwork
%if ! %{redhat_artwork}
   # Sane default settings
   mkdir -p %{buildroot}%{qtdir}/etc/settings
   cat >%{buildroot}%{qtdir}/etc/settings/qtrc <<"EOF"
[General]
libraryPath=%{_libdir}/kde3/plugins
style=Highcolor

[KDE]
contrast=7
EOF
%endif

pushd mkspecs
rm -fr default
if [ "%_lib" == "lib64" ]; then
   ln -sf linux-g++-64 default
else
   ln -sf linux-g++ default
fi
popd
cp -aR mkspecs %{buildroot}%{qtdir}

# Patch qmake to use qt-mt unconditionally
perl -pi -e "s,-lqt ,-lqt-mt ,g;s,-lqt$,-lqt-mt,g" %{buildroot}%{qtdir}/mkspecs/*/qmake.conf

rm -f %{buildroot}%{qtdir}/lib/*.la

mkdir -p %{buildroot}/etc/ld.so.conf.d
echo "%{qtdir}/lib" > %{buildroot}/etc/ld.so.conf.d/qt-%{_arch}.conf

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc FAQ LICENSE.QPL README* changes*
%dir %{qtdir}
%dir %{qtdir}/bin
%dir %{qtdir}/lib
%dir %{qtdir}/plugins
%if %{immodule}
%{qtdir}/plugins/inputmethods
%endif
/etc/ld.so.conf.d/*
%if ! %{redhat_artwork}
%{qtdir}/etc/settings/qtrc
%endif
%{qtdir}/lib/libqui.so.*
%{qtdir}/lib/libqt*.so.*


%files config
%defattr(-,root,root,-)
%{qtdir}/bin/qtconfig
%{_bindir}/qtconfig*


%files devel
%defattr(-,root,root,-)
%attr(0755,root,root) %config /etc/profile.d/*
%{qtdir}/bin/moc
%{qtdir}/bin/uic
%{qtdir}/bin/findtr
%{qtdir}/bin/qt20fix
%{qtdir}/bin/qtrename140
%{qtdir}/bin/assistant
%{qtdir}/bin/qm2ts
%{qtdir}/bin/qmake
%{qtdir}/bin/qembed
%{qtdir}/bin/linguist
%{qtdir}/bin/lupdate
%{qtdir}/bin/lrelease
%{qtdir}/include
%{qtdir}/mkspecs
%{qtdir}/lib/libqt*.so
%{qtdir}/lib/libqui.so
%{qtdir}/lib/libeditor.a
%{qtdir}/lib/libdesigner*.a
%{qtdir}/lib/libqassistantclient.a
%{qtdir}/lib/*.prl
%if %{installman}
%{_mandir}/*/*
%endif
%{qtdir}/translations
%{qtdir}/phrasebooks
%{_bindir}/assistant*
%{_bindir}/moc*
%{_bindir}/uic*
%{_bindir}/findtr*
%{_bindir}/qt20fix*
%{_bindir}/qtrename140*
%{_bindir}/qmake*
%{_bindir}/qm2ts*
%{_bindir}/qembed
%{_bindir}/linguist
%{_bindir}/lrelease
%{_bindir}/lupdate
%if %{pkg_config}
%{_libdir}/pkgconfig/*
%{qtdir}/lib/pkgconfig
%endif
%doc doc/html
%doc examples
%doc tutorial

%if %{motif_extention}
%post Xt -p /sbin/ldconfig
%postun Xt -p /sbin/ldconfig

%files Xt
%defattr(-,root,root,-)
%{qtdir}/lib/libqmotif.so*
%endif


%if %{styleplugins}
%files styles
%defattr(-,root,root,-)
%dir %{qtdir}/plugins/styles
%{qtdir}/plugins/styles/*
%endif


%if %{buildodbc}
%files ODBC
%defattr(-,root,root,-)
%{qtdir}/plugins/sqldrivers/libqsqlodbc*
%endif


%if %{buildpsql}
%files PostgreSQL
%defattr(-,root,root,-)
%{qtdir}/plugins/sqldrivers/libqsqlpsql*
%endif


%if %{buildmysql}
%files MySQL
%defattr(-,root,root,-)
%{qtdir}/plugins/sqldrivers/libqsqlmysql*
%endif


%files designer
%defattr(-,root,root,-)
%{_bindir}/designer*
%dir %{qtdir}/plugins/designer
%{qtdir}/templates
%{qtdir}/plugins/designer/*
%{qtdir}/bin/designer
%if %{desktop_file}
%{_datadir}/applications/*.desktop
%else
%{_datadir}/applnk/Development/*
%endif


%changelog
* Fri Mar 04 2005 Than Ngo <than@redhat.com> 1:3.3.4-8
- rebuilt against gcc-4.0.0-0.31

* Tue Mar 01 2005 Than Ngo <than@redhat.com> 1:3.3.4-7
- fix build problem with gcc4

* Mon Feb 28 2005 Than Ngo <than@redhat.com> 1:3.3.4-6
- rebuilt against gcc-4

* Tue Feb 22 2005 Than Ngo <than@redhat.com> 1:3.3.4-5
- fix application crash when input methode not available (bug #140658)
- remove .moc/.obj
- add qt-copy patch to fix KDE #80072

* Fri Feb 11 2005 Than Ngo <than@redhat.com> 1:3.3.4-4
- update qt-x11-immodule-unified patch

* Thu Feb 10 2005 Than Ngo <than@redhat.com> 1:3.3.4-3 
- fix rpm file conflict

* Wed Feb 02 2005 Than Ngo <than@redhat.com> 1:3.3.4-2
- remove useless doc files #143949
- fix build problem if installman is disable #146311
- add missing html/examples/tutorial symlinks

* Fri Jan 28 2005 Than Ngo <than@redhat.com> 1:3.3.4-1
- update to 3.3.4
- adapt many patches to qt-3.3.4
- drop qt-x11-free-3.3.0-freetype, qt-x11-free-3.3.3-qmake, qt-x11-free-3.3.1-lib64
  qt-x11-free-3.3.3-qimage, which are included in new upstream

* Tue Nov 30 2004 Than Ngo <than@redhat.com> 1:3.3.3-16
- add sql macro

* Mon Nov 29 2004 Than Ngo <than@redhat.com> 1:3.3.3-15
- convert qdial.3qt to UTF-8 bug #140946

* Tue Nov 23 2004 Than Ngo <than@redhat.com> 1:3.3.3-14
- add missing lupdate and lrelease #140230

* Fri Nov 19 2004 Than Ngo <than@redhat.com> 1:3.3.3-13 
- apply patch to fix qinputcontext

* Thu Nov 11 2004 Than Ngo <than@redhat.com> 1:3.3.3-12
- link against MySQL 3
- fix rpm conflict

* Wed Nov 10 2004 Than Ngo <than@redhat.com> 1:3.3.3-11
- apply patch to fix fullscreen problem
- remove html documents duplicate #135696

* Tue Nov 02 2004 Than Ngo <than@redhat.com> 1:3.3.3-10
- rebuilt

* Tue Nov 02 2004 Than Ngo <than@redhat.com> 1:3.3.3-9
- remove unused patch
- set XIMInputStyle=On The Spot
- require xorg-x11-devel instead XFree86-devel

* Thu Oct 14 2004 Than Ngo <than@redhat.com> 1:3.3.3-8
- don't compress examples/tutorial

* Thu Oct 07 2004 Than Ngo <than@redhat.com> 1:3.3.3-7
- fix build problem without qt immodule #134918

* Tue Sep 28 2004 Than Ngo <than@redhat.com> 1:3.3.3-6
- fix font problem, bz #133578

* Tue Sep 14 2004 Than Ngo <than@redhat.com> 1:3.3.3-4
- update new immodule patch
- fix multilib problem #132516

* Wed Aug 18 2004 Than Ngo <than@redhat.com> 1:3.3.3-3
- add patch to fix dlopen issue (#126422)
- add image handling fix

* Thu Aug 12 2004 Than Ngo <than@redhat.com> 1:3.3.3-2
- fix qmake broken link (#129723)

* Wed Aug 11 2004 Than Ngo <than@redhat.com> 1:3.3.3-1
- update to 3.3.3 release

* Thu Jul 01 2004 Than Ngo <than@redhat.com> 1:3.3.2-10
- add immodule for Qt

* Tue Jun 29 2004 Than Ngo <than@redhat.com> 1:3.3.2-9
- add sub package config, allow multi lib installation (#126643)

* Thu Jun 24 2004 Than Ngo <than@redhat.com> 1:3.3.2-8
- add fontconfig fix for qfontdatabase, #123868
- fix some buildrequires problem, #125289
- fix dangling symlink, #125351
- get rid of backup files

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com> 1:3.3.2-7
- rebuilt

* Tue May 25 2004 Than Ngo <than@redhat.com> 1:3.3.2-5
- add missing qembed tool #124052, #124052
- get rid of unused trigger
- add qt.conf in ld.so.conf.d -> don't change ld.so.conf #124080

* Wed May 12 2004 Than Ngo <than@redhat.com> 1:3.3.2-4
- backport some qt patches, Symbol font works again

* Mon May 10 2004 Than Ngo <than@redhat.com> 1:3.3.2-3
- fixed annoying warning

* Tue May 04 2004 Than Ngo <than@redhat.com> 1:3.3.2-2
- fix broken symlink at qt document, bug #121652

* Thu Apr 29 2004 Than Ngo <than@redhat.com> 3.3.2-1
- update to 3.3.2

* Thu Apr 22 2004 Than Ngo <than@redhat.com> 3.3.1-1
- add cvs backport
- fix lib64 issue, #121052
- fix CJK font display, bug #121017, #120542, thanks to Leon Ho
- compress tutorial/examples

* Fri Mar 26 2004 Than Ngo <than@redhat.com> 3.3.1-0.8
- fixed symlinks issue, #117572

* Thu Mar 25 2004 Than Ngo <than@redhat.com> 3.3.1-0.7
- add Trolltech patch, fix dpi setting issue

* Tue Mar 23 2004 Than Ngo <than@redhat.com> 3.3.1-0.6
- add 0034-qclipboard_recursion_fix.patch from CVS, #118368
- add better qt-x11-free-3.3.1-fontdatabase.patch

* Sun Mar 07 2004 Than Ngo <than@redhat.com> 1:3.3.1-0.5
- disable smpflags

* Fri Mar 05 2004 Than Ngo <than@redhat.com> 1:3.3.1-0.4
- fix font alias

* Thu Mar 04 2004 Than Ngo <than@redhat.com> 1:3.3.1-0.3
- add fontdatabase fix from Trolltech

* Thu Mar 04 2004 Than Ngo <than@redhat.com> 1:3.3.1-0.2
- fix wrong symlink #117451

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Mar 01 2004 Than Ngo <than@redhat.com> 3.3.1-0.1
- update to 3.3.1

* Mon Feb 23 2004 Than Ngo <than@redhat.com> 3.3.0-0.4
- add fix for building with freetype 2.1.7 or newer

* Tue Feb 17 2004 Than Ngo <than@redhat.com> 3.3.0-0.3 
- enable IPv6 support
- use dlopen, instead of linking with OpenGL libraries directly
- don't install backup files

* Thu Feb 05 2004 Than Ngo <than@redhat.com> 1:3.3.0-0.2
- fix fontdatabase
- don't use strip in install script
- fix qt default setting
 
* Wed Feb 04 2004 Than Ngo <than@redhat.com> 1:3.3.0-0.1
- 3.3.0

* Fri Jan 30 2004 Than Ngo <than@redhat.com> 1:3.2.3-0.4
- add mouse patch from CVS, bug #114647

* Tue Jan 20 2004 Than Ngo <than@redhat.com> 1:3.2.3-0.3
- rebuild

* Tue Dec  2 2003 Than Ngo <than@redhat.com> 1:3.2.3-0.2
- Added missing prl files, (report from trolltech)
- Fixed description
- include requires XFree86-devel on qt-devel
 
* Fri Nov 14 2003 Than Ngo <than@redhat.com> 1:3.2.3-0.1
- 3.2.3 release

* Thu Oct 30 2003 Than Ngo <than@redhat.com> 1:3.2.2-0.4
- fix encoding problem

* Sat Oct 18 2003 Than Ngo <than@redhat.com> 1:3.2.2-0.3
- fix encoding problem

* Fri Oct 17 2003 Than Ngo <than@redhat.com> 1:3.2.2-0.2
- add font alias patch file, thanks to Leon Ho
- clean up monospace.patch from Leon Ho
- remove some unneeded patch files

* Thu Oct 16 2003 Than Ngo <than@redhat.com> 1:3.2.2-0.1
- 3.2.2 release
- remove a patch file, which is included in 3.2.2

* Tue Oct 14 2003 Than Ngo <than@redhat.com> 1:3.2.1-1.3
- remove some unneeded patch files
- don't load XLFDs if XFT2 is used

* Mon Sep 08 2003 Than Ngo <than@redhat.com> 1:3.2.1-1.2
- fixed rpm file list

* Tue Sep 02 2003 Than Ngo <than@redhat.com> 1:3.2.1-1.1
- fix for the khtml form lineedit bug from CVS

* Wed Aug 27 2003 Than Ngo <than@redhat.com> 1:3.2.1-1
- 3.2.1 release

* Wed Jul 23 2003 Than Ngo <than@redhat.com> 1:3.2.0-1
- 3.2.0 release

* Mon Jun 23 2003 Than Ngo <than@redhat.com> 3.2.0b2-0.1
- 3.2.0b2
- add missing templates for designer

* Wed Jun 18 2003 Than Ngo <than@redhat.com> 3.2.0b1-0.2
- clean up specfile

* Wed Jun 18 2003 Than Ngo <than@redhat.com> 3.2.0b1-0.1
- 3.2.0b1

* Tue Jun 17 2003 Than Ngo <than@redhat.com> 3.1.2-12
- rebuilt

* Tue Jun 17 2003 Than Ngo <than@redhat.com> 3.1.2-10
- add missing translations

* Wed Jun 11 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon May 19 2003 Than Ngo <than@redhat.com> 3.1.2-7
- add some patches from KDE CVS qt-copy, thanks to Alexei Podtelezhnikov

* Mon May  5 2003 Than Ngo <than@redhat.com> 3.1.2-5.1
- set correct permission config scripts

* Tue Apr 29 2003 Than Ngo <than@redhat.com> 3.1.2-4
- fix typo bug in font loader

* Wed Apr  9 2003 Than Ngo <than@redhat.com> 3.1.2-2
- add xrandr extension

* Mon Mar  3 2003 Than Ngo <than@redhat.com> 3.1.2-1
- 3.1.2 release

* Mon Feb 17 2003 Elliot Lee <sopwith@redhat.com> 3.1.1-7
- ppc64 support

* Wed Jan 29 2003 Than Ngo <than@redhat.com> 3.1.1-6
- add missing Categories section in qt designer #82920

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Dec 30 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- Change qmlined.h to not include an attic header that is also not shipped
  with Red Hat Linux. This also fixes building unixODBC, that includes this
  header (apparently also without needing it).

* Thu Dec 19 2002 Than Ngo <than@redhat.com> 3.1.1-3
- add monospace patch file from Leon Ho (bug #79949)
- add small patch file from Sysoltsev Slawa (bug #79731)

* Tue Dec 17 2002 Than Ngo <than@redhat.com> 3.1.1-2
- don't require XFree86, it's not needed

* Tue Dec 17 2002 Than Ngo <than@redhat.com> 3.1.1-1
- update to 3.1.1

* Thu Nov 28 2002 Than Ngo <than@redhat.com> 3.1.0-1.3
- don't write Date into created moc files

* Mon Nov 18 2002 Than Ngo <than@redhat.com> 3.1.0-1.2
- add missing libs
- remove workaround for ppc

* Sun Nov 17 2002 Than Ngo <than@redhat.com> 3.1.0-1.1
- adjust qfontdatabase_x11 for 3.1.0
- fix lib64 issue
- add workaround to build on ppc

* Wed Nov 13 2002 Than Ngo <than@redhat.com> 3.1.0-1
- update to 3.1.0
- adjust some patch files for 3.1.0
- clean up specfile
- remove some Xft2 patch files, which are now in 3.1.0
- add qwidget_x11.cpp.diff from Trolltech
- install qt in %%{_libdir}/qt-3.1 (bug #77706)
- don't use rpath
- enable large file support
- use system Xinerama
- remove unneeded cups patch file
- fix to build against new XFree86

* Tue Nov  5 2002 Than Ngo <than@redhat.com> 3.0.5-19
- examples misconfigured (bug #76083)
- don't include pkg-config (bug #74621)
- fix build problem with new XFree86

* Tue Sep 17 2002 Than Ngo <than@redhat.com> 3.0.5-18
- Fixed binaries symlinks

* Mon Sep  9 2002 Than Ngo <than@redhat.com> 3.0.5-17hammer
- clean up spec file for 64bit machine

* Thu Aug 29 2002 Than Ngo <than@redhat.com> 3.0.5-17
- Fixed rpath issue (bug #69692, #69575)
- Removed dlopen patch
- Added monospace alias patch from Leon Ho (bug #72811)
- Added man pages

* Sun Aug 25 2002 Than Ngo <than@redhat.com> 3.0.5-16
- Added missing catagory in qt designer
- Added small gb18030 patch file from Leon Ho

* Thu Aug 22 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.5-15
- Prereq fileutils (#71500)

* Tue Aug 20 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.5-14
- Don't link to libstdc++, it isn't used
- Work around s390 compiler bug (fpic/fPIC coexistance)
- Do away with the "Feature Bluecurve already defined" warning message
- Remove qmake cache files from the package

* Wed Aug 14 2002 Than Ngo <than@redhat.com> 3.0.5-13
- Added fix to use VT100 graphic characters (bug #71364)
- Added fontdatabase fix from llch@redhat.com (bug #68353)

* Mon Aug 12 2002 Bernhard Rosenkraenzer <bero@redhat.com> [not built]
- Fix default qtrc

* Mon Aug 12 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.5-12
- Fix CJK Printing (#71123)

* Sun Aug 11 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.5-11
- Move qtconfig from qt-devel to qt, it's generally useful
- Use -fno-use-cxa-atexit
- Some tweaks to allow building Qt/Embedded with the same spec file
- Apply the GB18030 patch even if xft2 isn't set

* Fri Aug  9 2002 Than Ngo <than@redhat.com> 3.0.5-10
- Added XIM patch from llch@redhat.com (bug #70411)

* Sun Aug  4 2002 Than Ngo <than@redhat.com> 3.0.5-9
- add a missing patch file (closelock/openlock)

* Thu Aug  1 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.5-8
- Define QT_INSTALL_PREFIX in qmake

* Thu Aug  1 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.5-7
- Find correct location of qmake mkspecs even if QTDIR isn't set

* Thu Jul 25 2002 Than Ngo <than@redhat.com> 3.0.5-6
- Check file descriptor before closelock
* Thu Jul 25 2002 Than Ngo <than@redhat.com> 3.0.5-5
- Fixed a bug in openlock

* Wed Jul 24 2002 Than Ngo <than@redhat.com> 3.0.5-4
- Tiny tweaks to qt3 patch

* Tue Jul 23 2002 Owen Taylor <otaylor@redhat.com>
- Tiny fix to qt3.diff to not add '0' as a test character (#68964)

* Mon Jul 22 2002 Tim Powers <timp@redhat.com> 3.0.5-2
- rebuild using gcc-3.2-0.1

* Mon Jul 22 2002 Than Ngo <than@redhat.com> 3.0.5-1
- 3.0.5
- Fixed dependencies issue

* Thu Jul 18 2002 Than Ngo <than@redhat.com> 3.0.4-12
- Added qt-clipfix from Harald Hoyer (bug #67648)

* Tue Jul 16 2002 Than Ngo <than@redhat.com> 3.0.4-11
- get rid of qt resource, it's now in redhat-artworks
- add some define to build for 7.3

* Thu Jul 11 2002 Than Ngo <than@redhat.com> 3.0.4-10
- add missing Buildprequires desktop-file-utils
- add patches for GB18030 (llch@redhat.com) bug #68430

* Tue Jul 09 2002 Than Ngo <than@redhat.com> 3.0.4-9
- add new desktop file for qt designer

* Fri Jul  5 2002 Jakub Jelinek <jakub@redhat.com> 3.0.4-8
- compile libXinerama.a with -fpic in Qt until XFree86 is fixed
- make %%xft2 work even if old Xft headers aren't installed

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jun 18 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.4-6
- Re-enable Xft2 now that fontconfig is fixed
- Require a version of fontconfig that works
- Use -fPIC rather than -fpic on alpha

* Tue Jun 18 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.4-5
- Revert to Xft1 for now, Xft2 is too unstable
- Exclude alpha for now to work around binutils bugs

* Tue Jun 11 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.4-4
- Add (and fix up) fontconfig patch

* Mon Jun  3 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.4-3
- Remove the glweak patch, it isn't needed after dropping XFree86 3.x

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May  5 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.4-1
- 3.0.4
- Make SQL plugins optional (buildtime)
- Register with pkgconfig

* Thu May 02 2002 Than Ngo <than@redhat.com> 3.0.3-12
- qtdir /usr/lib/qt3
- build against gcc-3.1-0.26
- add qt-3.0.3-glweak.patch 

* Wed Apr 17 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.3-11
- qt3-gcc2.96 should be in qt, not qt-devel

* Mon Apr 15 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.3-10
- Tweaks to allow parallel installations of Qt 3.x (gcc 2.96) and Qt 3.x
  (gcc 3.1)
- Fix up debug spewage at Qt designer startup

* Wed Apr 10 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.3-9
- Spec file fixes

* Wed Apr 10 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.3-8
- Get rid of non-threaded version, dlopen()'ing threaded code
  (like plugins) from non-threaded code is dangerous
- Add some fixes from qt-copy, fixing the ksplash crash some people
  have noticed on a first login
- Add translation fixes from CVS
- Patch example .pro files to build outside the Qt source tree (#63023)
- Fix various bugs

* Thu Apr 04 2002 Leon Ho <llch@redhat.com> 3.0.3-7
- fixes for CJK - qpsprinter
- fixes for CJK - gb18030

* Fri Mar 29 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.3-6
- Make sure it builds with both gcc 2.96 and 3.1

* Wed Mar 28 2002 Leon Ho <llch@redhat.com> 3.0.3-5
- fixes for CJK - qpsprinter

* Wed Mar 27 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.3-4
- Add CJK patches

* Tue Mar 26 2002 Than Ngo <than@redhat.com> 3.0.3-3
- fix loading kde styles

* Tue Mar 19 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.3-1
- Update to 3.0.3 final

* Thu Mar 14 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.3-0.cvs20020314.1
- Update to 3.0.3-pre, required for KDE3
- force -fPIC usage
- Remove conflict with qt2 < 2.3.2-1, the new qt2 2.3.1 is fixed and qt 2.3.2
  is broken
- Ship the qmake config files (so qmake works for building any 3rd party stuff,
  e.g. aethera)

* Wed Mar  6 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.2-2
- Add some fixes from KDE's qt-copy CVS
- Pluginize image formats

* Mon Feb 25 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.2-1
- 3.0.2 final

* Tue Feb 19 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.2-0.cvs20020118.3
- Add GB18030 codec patch, #60034
- Force-build jpeg support, fixing #59775 and #59795

* Sat Jan 26 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.2-0.cvs20020118.2
- Build with CUPS support

* Fri Jan 18 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.2-0.cvs20020118.1
- Fix up /usr/bin/moc links, they should point to qt3

* Mon Jan 14 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.2-0.cvs20020114.1
- Build styles directly into the main library for now, there's too much broken
  code out there depending on this ATM.

* Wed Jan  9 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.2-0.cvs20020109.1
- Stop excluding alpha, gcc has been fixed

* Tue Jan  8 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.2-0.cvs20020108.1
- Add fixes from CVS; this fixes the "Alt + F1, arrow up, arrow up doesn't work
  in KDE" bug

* Mon Dec 17 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.1-2
- Fix up settings search path
- Add default qtrc allowing to use KDE 3.x Qt plugins
- Make sure QLibrary uses RTLD_GLOBAL when dlopen()ing libraries

* Thu Dec 13 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.1.0-1
- Work around gcc bug #57467

* Wed Dec 12 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 3.0.1 final

* Mon Dec 10 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.1-0.cvs20011210.1
- Update to current (needed by KDE 3.x)
- Rebuild with current libstdc++
- Temporarily disable building on alpha
- Fix build with PostgreSQL 7.2

* Mon Nov 26 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.0-5
- Fix up glweak

* Mon Nov  5 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.0-4
- Give designer, uic, moc, etc. their real names - the qt2 versions
  have been renamed in qt2-2.3.2-1.
  Conflict with qt2 < 2.3.2-1.

* Thu Oct 25 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.0-3
- Add symlink /usr/lib/qt-3.0.0 -> /usr/lib/qt3 and set QTDIR to the
  symlink, allowing to update to 3.0.1 without breaking rpath'ed binaries

* Tue Oct 16 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.0-1
- 3.0.0 final
- fix some minor specfile bugs
- Modularize some more (image format plugins)
- Build codecs

* Tue Sep 18 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.0-0.beta5.1
- beta5
- Share more code between qt-x11 and qt-embedded builds

* Wed Aug 29 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.0-0.beta4.1
- beta4
- build the Motif style directly into Qt rather than as a plugin - Qt should
  always have at least one style...
- replace the designer3 symlink with a shell script that sets QTDIR correctly
  before launching designer
- Add desktop file for designer

* Mon Aug  6 2001 Tim Powers <timp@redhat.com> 3.0.0-0.beta3.4
- explicitly include qm2ts, qmake, qtconfig in the devel package file list to avoid dangling symlinks

* Thu Aug  2 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.0-0.beta3.3
- Try yet another workaround for buildsystem breakages

* Tue Jul 31 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Add another ugly workaround for build system problems, this should finally
  get rid of the dangling symlinks

* Tue Jul 31 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.0-0.beta3.2
- Rephrase parts of the spec file, hopefully pleasing the build system

* Sun Jul 29 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.0-0.beta3.1
- beta3
- Fix dangling symlinks

* Sun Jun 24 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.0-0.beta1.2
- Fix up QSQL Postgres classes for Postgres 7.1.x
- Fix various bugs:
  - QtMultilineEdit and QtTableView should actually compile
  - Link libqsqlpsql with libpq
  - Don't link the base library with libmysqlclient, linking the MySQL
    module with it is sufficient
- Add missing const qualifier
- move the SQL drivers to separate packages to avoid dependencies
- build and install designer plugins - converting glade files to Qt is fun. ;)
- handle RPM_OPT_FLAGS

* Tue May 22 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.0-0.beta1.1
- 3.0 beta 1

* Wed May 16 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.0-0.cvs20010516.1
- Update, remove conflicts with Qt 2.x

* Mon May 14 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.0-0.cvs20010514.1
- Initial build of 3.0 branch

* Fri Apr 27 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.3.0-6
- Fix crashes on ia64, Patch from Bill Nottingham <notting@redhat.com>
- Allow building qt-nox

* Fri Apr 20 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.3.0-5
- Make sure uic and designer use the libqui from the source tree, not
  a previously installed one.
  Linking uic-x11 against libqui-embedded is definitely not a feature. ;)
- The qclipboard fix is needed for qt-x11 only, don't apply it if we're
  building qt-embedded

* Sat Apr 14 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Handle LPRng specific constructs in printcap, Bug #35937

* Sun Mar 25 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add qfont patch from Trolltech

* Tue Mar 13 2001 Harald Hoyer <harald@redhat.de>
- added patch for '@euro' language settings

* Tue Mar  6 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.3.0 final
- BuildRequires XFree86-devel >= 4.0.2 (#30486)

* Mon Feb 26 2001 Than Ngo <than@redhat.com>
- fix check_env function, so that qt does not crash if QT_XFT is not set
- fix symlinks

* Mon Feb 26 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.3.0b1
- Add a patch to qpsprinter that handles TrueType fonts even if they come from xfs

* Tue Feb 13 2001 Preston Brown <pbrown@redhat.com>
- japanese input and clipboard fixes applied.  Changes have been sent upstream by patch authors.

* Fri Feb  9 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Rebuild with new Mesa to get rid of pthreads linkage
- Add Xft fix from KDE CVS

* Wed Feb  7 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Add printing bugfix patch from Trolltech

* Sat Feb  3 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.2.4
- Qt Embedded: Add QVfb and VNC support

* Tue Jan 16 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Don't segfault when running Qt/Embedded applications as root
- Improve the Qt/Embedded sparc patch so we don't need the specfile hacks
  anymore
- Fix a bug in QPrintDialog (causing KDE Bug #18608)

* Thu Jan 11 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- bzip2 source to save space
- Qt/Embedded 2.2.3
- Fix qte build on sparc

* Wed Dec 20 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Run ldconfig in %%post and %%postun for qt-Xt

* Sun Dec 17 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Build with the Xrender extension
  (Patch from Keith Packard <keithp@keithp.com>)

* Wed Dec 13 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.2.3

* Tue Dec 12 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Rebuild to fix permissions on doc dir
- Don't exclude ia64 anymore

* Fri Nov 17 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix up uic (Patch from trolltech) 

* Wed Nov 15 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Build qt-embedded
  changes to base: fix build, fix ISO C99 compliance, fix 64bit support

* Mon Nov 13 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.2.2

* Tue Oct 24 2000 Than Ngo <than@redhat.com>
- call ldconfig for updating (Bug #19687)
- added patch from Trolltech, thanks to Rainer <rms@trolltech.com>

* Wed Oct 18 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Add missing msg2qm, msgmerge, qconfig tools (Bug #18997), introduced
  by broken Makefiles in base
- fix up %%install so it works both with old-style and new-style fileutils
  (fileutils <= 4.0z don't know about -L)

* Fri Oct 13 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Disable exception handling; this speeds up KDE 2.x and reduces its
  memory footprint by 20 MB.

* Tue Oct 10 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- dereference symlinks in include

* Sun Oct  8 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- fix -devel
- update to the new version of 2.2.1 on trolltech.com; the initial tarball
  contained broken docs

* Thu Oct  5 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.2.1

* Mon Sep 25 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Add missing uic

* Thu Sep 21 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Move Qt designer to a different source RPM to get rid of a
  circular dependency (kdelibs2->qt, qt->kdelibs2)
- Enable MNG support
- Don't compile (just include) examples and tutorials
- move the static libraries to a separate package (qt-static).
  They're HUGE, and most people won't ever need them.
- clean up spec file
- fix up dependencies (-devel requires base, -static requires devel,
  Xt requires base)
- add BuildRequires line

* Tue Sep 12 2000 Than Ngo <than@redhat.com>
- update release 2.2.0
- changed copyright to GPL
- added missing static libraries
- made symbolic link for designer to load the help files correct
- made designer and designer-kde2 as sub packages
- added missing templates for designer
- remove jakub patch, since the release 2.2.0 already 
  contains this patch.
- fixed qt again to compile with gcc-2.96
- use make -j for building

* Wed Aug 23 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Work around compiler bugs (Patch from Jakub)
- Use relative symlinks (Bug #16750)

* Mon Aug 21 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- beta2

* Mon Aug 14 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- new qt-copy from KDE2 CVS

* Wed Aug 9 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- official beta 1

* Thu Aug 3 2000 Than Ngo <than@redhat.de>
- rebuilt against the libpng-1.0.8

* Thu Jul 27 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- rebuild (so we have it on all arches)

* Tue Jul 25 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- move man pages to a more reasonable place (this fixes Bug #14126)
- exclude ia64 for now (compiler problems!!!)

* Mon Jul 24 2000 Harald Hoyer <harald@redhat.de>
- modified connect patch to fit qt 2.2.0 beta.

* Thu Jul 20 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- update to current qt-copy; this is now a qt 2.2.0 beta.

* Mon Jul 17 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- update to current qt-copy in kde CVS, required

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jul 11 2000 Harald Hoyer <harald@redhat.de>
- made patch smaller and binary compatible when recompiled with 6.2
- modified connect and moc to cope with the new g++ class layout

* Sun Jul 09 2000 Than Ngo <than@redhat.de>
- rebuilt qt with gcc-2.96-34

* Fri Jul 07 2000 Than Ngo <than@redhat.de>
- rebuilt qt with c++ 2.96

* Mon Jul  3 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix dependancies

* Sun Jul  2 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Use egcs++ for now ** FIXME

* Wed Jun 28 2000 Preston Brown <pbrown@redhat.com>
- fix up qt.sh

* Sun Jun 25 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Build in jpeg and threading support
- Fix a bug in clipboard pasting code

* Wed Jun 07 2000 Preston Brown <pbrown@redhat.com>
- fix qt.{sh,csh}
- use new rpm macro paths
- package man pages

* Fri Jun  2 2000 Bill Nottingham <notting@redhat.com>
- build without optimization on ia64

* Mon May 29 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.1.1

* Thu May 18 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- recompile with correct libstdc++

* Thu Apr 13 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.1.0 final

* Wed Apr  5 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- beta4
- depend on libGL.so.1 rather than Mesa - XFree86 4.0 provides that
  lib, too

* Wed Mar 22 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- beta3

* Tue Mar  7 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- beta2
- fix compilation of the NSPlugin add-on

* Fri Mar  3 2000 Bill Nottingham <notting@redhat.com>
- fix %postun script

* Fri Feb 18 2000 Bernhard Rosenkränzer <bero@redhat.com>
- beta1
- get rid of qt-ImageIO, the functionality is now in the main Qt library
- remove qt-Network, the functionality is now in the main Qt library
- add changes-2.1.0 to %doc

* Thu Feb 17 2000 Preston Brown <pbrown@redhat.com>
- no refcount check on postun script, we want it to happen even on upgrades

* Thu Feb 10 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- new snapshot, should fix QWhatsThisButton
- remove executable permissions from *.pro files

* Mon Feb 07 2000 Preston Brown <pbrown@redhat.com>
- strip binaries in examples, tutorial

* Mon Jan 31 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- new snapshot - should fix the hotkey bug
- Fix up the Makefiles so it compiles

* Tue Jan 18 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- new snapshot - we need those QVariant fixes

* Thu Jan 13 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- switch from glxMesa to Mesa for the GL addon

* Wed Jan 5 2000 Bernhard Rosenkränzer <bero@redhat.com>
- Fix up dependencies
- new snapshot

* Mon Jan 3 2000 Ngo Than <than@redhat.de>
- new snapshot for Red Hat Linux 6.2
- increase version number

* Mon Dec 20 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- new snapshot
- handle RPM_OPT_FLAGS

* Mon Dec 13 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- new snapshot
- -GL requires libGL.so.1 instead of Mesa (might as well be glxMesa
  or some commercial OpenGL)
- -GL BuildPrereqs /usr/X11R6/include/GL/gl.h instead of Mesa-devel
  (might as well be glxMesa or some commercial OpenGL)

* Sun Dec 05 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- update to current RSYNC version
- remove compilation patch - it finally works out of the box

* Wed Oct 27 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- update to current CVS snapshot
- build extensions
- add patch to fix QNetwork compilation

* Sun Oct 24 1999 Bernhard Rosenkraenzer <bero@redhat.de>
- current CVS snapshot
- fix compilation with gcc 2.95.x
- use install -c rather than just install to make BSD install happy

* Mon Oct 11 1999 Bernhard Rosenkraenzer <bero@redhat.de>
- 2.1.0 snapshot (for KDE2)
- Fix typo in spec

* Thu Sep 23 1999 Preston Brown <pbrown@redhat.com>
- don't ship tutorial or example binaries

* Tue Sep 21 1999 Preston Brown <pbrown@redhat.com>
- substitution in tutorial and examples so that dependencies are correct and
  they can be successfully rebuilt.
- switched to completely using QTDIR.  trying to coexist with links into
  /usr/{include,lib} and still compile with qt 1.x is very hard for
  configure scripts to cope with.

* Thu Aug 19 1999 Preston Brown <pbrown@redhat.com>
- implemented QTDIR compatibility.

* Tue Jul 20 1999 Preston Brown <pbrown@redhat.com>
- qt 2.0.1 packaged.

* Wed Jul 14 1999 Preston Brown <pbrown@redhat.com>
- Qt 2.00 packaged.
- examples, html documentation, tutorial moved to /usr/doc

* Sat Apr 17 1999 Preston Brown <pbrown@redhat.com>
- static library supplied in dev package.

* Wed Apr 07 1999 Preston Brown <pbrown@redhat.com>
- turn on internal GIF reading support

* Tue Apr 06 1999 Preston Brown <pbrown@redhat.com>
- strip binaries

* Mon Mar 15 1999 Preston Brown <pbrown@redhat.com>
- upgrade to qt 1.44.

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Tue Jan 19 1999 Preston Brown <pbrown@redhat.com>
- moved includes to /usr/include/qt

* Mon Jan 04 1999 Preston Brown <pbrown@redhat.com>
- made setup phase silent.

* Fri Dec 04 1998 Preston Brown <pbrown@redhat.com>
- upgraded to qt 1.42, released today.

* Tue Dec 01 1998 Preston Brown <pbrown@redhat.com>
- took Arnts RPM and made some minor changes for Red Hat.
