# Fedora Review: http://bugzilla.redhat.com/188180

# configure options
# -no-pch disables precompiled headers, make ccache-friendly
#define no_pch -no-pch

Summary: Qt toolkit
%if 0%{?fedora} > 8
Name:    qt
Epoch:   1
%else
Name:    qt4
%endif
Version: 4.5.0
Release: 1%{?dist}

License: LGPLv2 or GPLv3 with exceptions
Group: System Environment/Libraries
Url: http://www.qtsoftware.com/
Source0: ftp://ftp.trolltech.com/qt/source/qt-x11-opensource-src-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if "%{name}" != "qt4"
Obsoletes: qt4 < %{version}-%{release}
Provides: qt4 = %{version}-%{release}
%{?_isa:Provides: qt4%{?_isa} = %{version}-%{release}}
%endif

Source4: Trolltech.conf

# See http://bugzilla.redhat.com/223663
%define multilib_archs x86_64 %{ix86} ppc64 ppc s390x s390 sparc64 sparcv9
Source5: qconfig-multilib.h

# multilib hacks 
Patch2: qt-x11-opensource-src-4.2.2-multilib-optflags.patch
Patch3: qt-x11-opensource-src-4.2.2-multilib-QMAKEPATH.patch
Patch5: qt-all-opensource-src-4.4.0-rc1-as_IN-437440.patch
# under GNOME, default to QGtkStyle if available
# (otherwise fall back to QCleanlooksStyle)
Patch9: qt-x11-opensource-src-4.4.0-qgtkstyle.patch
Patch10: qt-x11-opensource-src-4.5.0-rc1-ppc64.patch
## upstreamable bits
# http://bugzilla.redhat.com/485677
Patch50: qt-x11-opensource-src-4.5.0-rc1-qhostaddress.patch

## qt-copy patches
%define qt_copy 20090303
Source1: qt-copy-patches-svn_checkout.sh
%{?qt_copy:Source2: qt-copy-patches-%{qt_copy}svn.tar.bz2}
%{?qt_copy:Provides: qt-copy = %{qt_copy}}
%{?qt_copy:Provides: qt4-copy = %{qt_copy}}

Source11: qt4.sh
Source12: qt4.csh

Source20: assistant.desktop
Source21: designer.desktop
Source22: linguist.desktop
Source23: qtdemo.desktop
Source24: qtconfig.desktop

# upstream qt4-logo, http://trolltech.com/images/products/qt/qt4-logo
Source30: hi128-app-qt4-logo.png
Source31: hi48-app-qt4-logo.png

## optional plugin bits
# set to -no-sql-<driver> to disable
# set to -qt-sql-<driver> to enable *in* qt library
%define mysql -plugin-sql-mysql
%define odbc -plugin-sql-odbc
%define psql -plugin-sql-psql
%define sqlite -plugin-sql-sqlite
%define phonon -phonon
%define webkit -webkit
%define gtkstyle -gtkstyle

#define nas -system-nas-sound
%define nas -no-nas-sound
%if 0%{?fedora} > 4 || 0%{?rhel} > 4
# link dbus
%define dbus -dbus-linked
# dlopen dbus
#define dbus -dbus
BuildRequires: dbus-devel >= 0.62
%endif

# See http://bugzilla.redhat.com/196901
%define _qt4 %{name}
%define _qt4_prefix %{_libdir}/qt4
%define _qt4_bindir %{_qt4_prefix}/bin
# _qt4_datadir is not multilib clean, and hacks to workaround that breaks stuff.
#define _qt4_datadir %{_datadir}/qt4
%define _qt4_datadir %{_qt4_prefix}
%define _qt4_demosdir %{_qt4_prefix}/demos
%define _qt4_docdir %{_docdir}/qt4
%define _qt4_examplesdir %{_qt4_prefix}/examples
%define _qt4_headerdir %{_includedir} 
%define _qt4_libdir %{_libdir}
%define _qt4_plugindir %{_qt4_prefix}/plugins
%define _qt4_sysconfdir %{_sysconfdir}
%define _qt4_translationdir %{_datadir}/qt4/translations

%if "%{_qt4_libdir}" != "%{_libdir}"
Prereq: /etc/ld.so.conf.d
%endif

BuildRequires: cups-devel
BuildRequires: desktop-file-utils
BuildRequires: findutils
BuildRequires: fontconfig-devel
BuildRequires: freetype-devel
BuildRequires: libjpeg-devel
BuildRequires: libmng-devel
BuildRequires: libpng-devel
BuildRequires: libtiff-devel
BuildRequires: freetype-devel
BuildRequires: zlib-devel
BuildRequires: glib2-devel
BuildRequires: openssl-devel
BuildRequires: pkgconfig

## In theory, should be as simple as:
#define x_deps libGL-devel libGLU-devel
## but, "xorg-x11-devel: missing dep on libGL/libGLU" - http://bugzilla.redhat.com/211898 
%define x_deps xorg-x11-devel xorg-x11-Mesa-libGL xorg-x11-Mesa-libGLU
%if 0%{?fedora} > 4 || 0%{?rhel} > 4
%define x_deps libICE-devel libSM-devel libXcursor-devel libXext-devel libXfixes-devel libXft-devel libXi-devel libXinerama-devel libXrandr-devel libXrender-devel libXt-devel libX11-devel xorg-x11-proto-devel libGL-devel libGLU-devel
%endif
BuildRequires: %{x_deps}

%if "%{?nas}" != "-no-nas-sound"
BuildRequires: nas-devel
%endif

%if "%{?mysql}" != "-no-sql-mysql"
BuildRequires: mysql-devel >= 4.0
%endif

%if "%{?phonon}" == "-phonon"
BuildRequires: glib2-devel
BuildRequires: gstreamer-plugins-base-devel 
%endif

%if "%{?gtkstyle}" == "-gtkstyle"
BuildRequires: gtk2-devel
%endif

%if "%{?psql}" != "-no-sql-psql"
BuildRequires: postgresql-devel
# added deps to workaround http://bugzilla.redhat.com/440673
BuildRequires: krb5-devel libxslt-devel openssl-devel pam-devel readline-devel zlib-devel
%endif

%if "%{?odbc}" != "-no-sql-odbc"
BuildRequires: unixODBC-devel
%endif

%if "%{?sqlite}" != "-no-sql-sqlite"
%define _system_sqlite -system-sqlite
BuildRequires: sqlite-devel
%endif

Obsoletes: qgtkstyle < 0.1
Provides:  qgtkstyle = 0.1-1
Obsoletes: qt4-config < 4.5.0
Provides: qt4-config = %{version}-%{release}
Obsoletes: qt4-sqlite < 4.5.0 
Provides: qt4-sqlite = %{version}-%{release}
%if "%{name}" == "qt"
Obsoletes: qt-sqlite < %{?epoch:%{epoch}:}4.5.0
Provides: qt-sqlite = %{?epoch:%{epoch}:}%{version}-%{release}
%endif

%description 
Qt is a software toolkit for developing applications.

This package contains base tools, like string, xml, and network
handling.

%package devel
Summary: Development files for the Qt toolkit
Group: Development/Libraries
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: %{name}-x11 
Requires: %{x_deps}
Requires: libpng-devel
Requires: libjpeg-devel
Requires: pkgconfig
%if 0%{?phonon:1}
# No, let's avoid the circular dependency (for now) -- Rex
#Requires: phonon-devel
%endif
%if 0%{?webkit:1}
Obsoletes: WebKit-qt-devel < 1.0.0-1
Provides:  WebKit-qt-devel = 1.0.0-1
%endif
# we strip these from the .pc files to avoid the bogus deps
# -openssl-linked ? -- Rex
#Requires: openssl-devel
# -dbus-linked ? -- Rex
#Requires: dbus-devel
Obsoletes: qt4-designer < %{version}-%{release}
Provides:  qt4-designer = %{version}-%{release}
%if "%{name}" != "qt4"
Obsoletes: qt4-devel < %{version}-%{release}
Provides:  qt4-devel = %{version}-%{release}
%endif

%description devel
This package contains the files necessary to develop
applications using the Qt toolkit.  Includes:
Qt Linguist

%package doc
Summary: API documentation, demos and example programs for %{name}
Group: Documentation
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: %{name}-assistant
%if "%{name}" != "qt4"
Obsoletes: qt4-doc < %{version}-%{release}
Provides:  qt4-doc = %{version}-%{release}
%endif

%description doc
%{summary}.  Includes:
Qt Assistant, Qt Demo

%package odbc 
Summary: ODBC driver for Qt's SQL classes
Group: System Environment/Libraries
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes: qt4-ODBC < %{version}-%{release}
Provides:  qt4-ODBC = %{version}-%{release}
%if "%{name}" != "qt4"
Obsoletes: qt4-odbc < %{version}-%{release}
Provides:  qt4-odbc = %{version}-%{release}
%endif

%description odbc 
%{summary}.

%package mysql 
Summary: MySQL driver for Qt's SQL classes
Group: System Environment/Libraries
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes: qt4-MySQL < %{version}-%{release}
Provides:  qt4-MySQL = %{version}-%{release}
%if "%{name}" != "qt4"
Obsoletes: qt4-mysql < %{version}-%{release}
Provides:  qt4-mysql = %{version}-%{release}
%endif

%description mysql 
%{summary}.

%package postgresql 
Summary: PostgreSQL driver for Qt's SQL classes
Group: System Environment/Libraries
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes: qt4-PostgreSQL < %{version}-%{release}
Provides:  qt4-PostgreSQL = %{version}-%{release}
%if "%{name}" != "qt4"
Obsoletes: qt4-postgresql < %{version}-%{release}
Provides:  qt4-postgresql = %{version}-%{release}
%endif

%description postgresql 
%{summary}.

%package x11
Summary: Qt GUI-related libraries
Group: System Environment/Libraries
%if 0%{?webkit:1}
Obsoletes: WebKit-qt < 1.0.0-1
Provides:  WebKit-qt = 1.0.0-1
%endif
Provides: qt4-assistant = %{version}-%{release}
%if "%{name}" != "qt4"
Provides: %{name}-assistant = %{version}-%{release}
%endif
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
%if "%{name}" != "qt4"
Obsoletes: qt4-x11 < %{version}-%{release}
Provides:  qt4-x11 = %{version}-%{release}
%endif

%description x11
Qt libraries which are used for drawing widgets and OpenGL items.


%prep
%setup -q -n qt-x11-opensource-src-%{version} %{?qt_copy:-a 2}

%if 0%{?qt_copy}
echo "0250" >> patches/DISABLED
test -x apply_patches && ./apply_patches
%endif

# don't use -b on mkspec files, else they get installed too.
# multilib hacks no longer required
%patch2 -p1
%if "%{_qt4_datadir}" != "%{_qt4_prefix}"
%patch3 -p1 -b .multilib-QMAKEPATH
%endif
%patch5 -p1 -b .bz#437440-as_IN-437440
%patch9 -p1 -b .qgtkstyle
%patch10 -p1 -b .ppc64
%patch50 -p1 -b .qhostaddress

# drop -fexceptions from $RPM_OPT_FLAGS
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's|-fexceptions||g'`

## customize our platform
%if "%{_lib}" == "lib64"
%define platform linux-g++-64
%else
%define platform linux-g++
%endif

sed -i \
  -e "s|-O2|$RPM_OPT_FLAGS|g" \
  -e "s|g++.conf|g++-multilib.conf|g" mkspecs/%{platform}/qmake.conf

sed -e "s|^QMAKE_CFLAGS_RELEASE|#QMAKE_CFLAGS_RELEASE|g" \
  mkspecs/common/g++.conf > mkspecs/common/g++-multilib.conf
  
## FIXME, http://bugzilla.redhat.com/230224
# On the surface, looks like a good idea to strip -I/usr/include, -L/usr/lib, 
# but it turns out qmake-consuming apps expect/use QMAKE_INCDIR_QT directly 
# (e.g. PyQt4, texmaker), and don't cope with null values
#if "%{_qt4_headerdir}" == "%{_includedir}"
#sed -i -e "s|^QMAKE_INCDIR_QT.*=.*|QMAKE_INCDIR_QT       =|" mkspecs/common/linux.conf
#endif
%if "%{_qt4_libdir}" == "%{_libdir}"
  sed -i -e "s|^QMAKE_LIBDIR_QT.*=.*|QMAKE_LIBDIR_QT       =|" mkspecs/common/linux.conf
%endif

# undefine QMAKE_STRIP, so we get useful -debuginfo pkgs
sed -i -e "s|^QMAKE_STRIP.*=.*|QMAKE_STRIP             =|" mkspecs/common/linux.conf 

# set correct lib path
if [ "%{_lib}" == "lib64" ] ; then
  sed -i -e "s,/usr/lib /lib,/usr/%{_lib} /%{_lib},g" config.tests/{unix,x11}/*.test
  sed -i -e "s,/lib /usr/lib,/%{_lib} /usr/%{_lib},g" config.tests/{unix,x11}/*.test
fi


%build

# build shared, threaded (default) libraries
./configure -v \
  -confirm-license \
  -optimized-qmake \
  -prefix %{_qt4_prefix} \
  -bindir %{_qt4_bindir} \
  -datadir %{_qt4_datadir} \
  -demosdir %{_qt4_demosdir} \
  -docdir %{_qt4_docdir} \
  -examplesdir %{_qt4_examplesdir} \
  -headerdir %{_qt4_headerdir} \
  -libdir %{_qt4_libdir} \
  -plugindir %{_qt4_plugindir} \
  -sysconfdir %{_qt4_sysconfdir} \
  -translationdir %{_qt4_translationdir} \
  -platform %{platform} \
  -release \
  -shared \
  -cups \
  -fontconfig \
  -largefile \
  -gtkstyle \
  -qt-gif \
  -no-rpath \
  -reduce-relocations \
  -no-separate-debug-info \
  %{?phonon} %{!?phonon:-no-phonon} \
  %{?no_pch} \
  -sm \
  -stl \
  -system-libmng \
  -system-libpng \
  -system-libjpeg \
  -system-libtiff \
  -system-zlib \
  -xinput \
  -xcursor \
  -xfixes \
  -xinerama \
  -xshape \
  -xrandr \
  -xrender \
  -xkb \
  -glib \
  -openssl-linked \
  -xmlpatterns \
  %{?dbus} %{!?dbus:-no-dbus} \
  %{?webkit} %{!?webkit:-no-webkit } \
  %{?nas} \
  %{?mysql} \
  %{?psql} \
  %{?odbc} \
  %{?sqlite} %{?_system_sqlite}

make %{?_smp_mflags}


%install
rm -rf %{buildroot}

make install INSTALL_ROOT=%{buildroot}

# Add desktop file(s)
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --vendor="qt4" \
  %{SOURCE20} %{SOURCE21} %{SOURCE22} %{SOURCE23} %{SOURCE24}

## pkg-config
# strip extraneous dirs/libraries 
# FIXME?: qt-4.5 seems to use Libs.private properly, so this hackery should 
#         no longer be required -- Rex
# safe ones
glib2_libs=$(pkg-config --libs glib-2.0 gobject-2.0 gthread-2.0)
ssl_libs=$(pkg-config --libs openssl)
for dep in \
  -laudio -ldbus-1 -lfreetype -lfontconfig ${glib2_libs} \
  -ljpeg -lm -lmng -lphonon -lpng ${ssl_libs} -lsqlite3 -lphonon -lz \
  -L/usr/X11R6/%{_lib} -L%{_libdir} ; do
  sed -i -e "s|$dep ||g" %{buildroot}%{_qt4_libdir}/lib*.la ||:
  sed -i -e "s|$dep ||g" %{buildroot}%{_qt4_libdir}/pkgconfig/*.pc
  sed -i -e "s|$dep ||g" %{buildroot}%{_qt4_libdir}/*.prl
done
# riskier
for dep in -lXrender -lXrandr -lXcursor -lXfixes -lXinerama -lXi -lXft -lXt -lXext -lX11 -lSM -lICE -ldl -lpthread ; do
  sed -i -e "s|$dep ||g" %{buildroot}%{_qt4_libdir}/lib*.la ||:
  sed -i -e "s|$dep ||g" %{buildroot}%{_qt4_libdir}/pkgconfig/*.pc 
  sed -i -e "s|$dep ||g" %{buildroot}%{_qt4_libdir}/*.prl
done

# nuke dangling reference(s) to %buildroot
sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" %{buildroot}%{_qt4_libdir}/*.prl

%if "%{_qt4_docdir}" != "%{_qt4_prefix}/doc"
# -doc make symbolic link to _qt4_docdir
rm -rf %{buildroot}%{_qt4_prefix}/doc
ln -s  ../../share/doc/qt4 %{buildroot}%{_qt4_prefix}/doc
%endif

# let rpm handle binaries conflicts
mkdir %{buildroot}%{_bindir}
pushd %{buildroot}%{_qt4_bindir}
for i in * ; do
  case "${i}" in
    assistant|designer|linguist|lrelease|lupdate|moc|qmake|qtconfig|qtdemo|uic)
      mv $i ../../../bin/${i}-qt4
      ln -s ../../../bin/${i}-qt4 .
      ln -s ../../../bin/${i}-qt4 $i
      ;;
    *)
      mv $i ../../../bin/
      ln -s ../../../bin/$i .
      ;;
  esac
done
popd

# _debug lib symlinks (see bug #196513)
pushd %{buildroot}%{_qt4_libdir}
for lib in libQt*.so ; do
  ln -s $lib $(basename $lib .so)_debug.so
done
for lib in libQt*.a ; do
  ln -s $lib $(basename $lib .a)_debug.a
done
popd

# .la files, die, die, die.
rm -f %{buildroot}%{_qt4_libdir}/lib*.la

%ifarch %{multilib_archs}
# multilib: qconfig.h
  mv %{buildroot}%{_qt4_headerdir}/Qt/qconfig.h %{buildroot}%{_qt4_headerdir}/QtCore/qconfig-%{_arch}.h
  install -p -m644 -D %{SOURCE5} %{buildroot}%{_qt4_headerdir}/QtCore/qconfig-multilib.h
  ln -sf qconfig-multilib.h %{buildroot}%{_qt4_headerdir}/QtCore/qconfig.h
  ln -sf ../QtCore/qconfig.h %{buildroot}%{_qt4_headerdir}/Qt/qconfig.h

%if "%{_qt4_datadir}" != "%{_qt4_prefix}"
# multilib: mkspecs hacks, unfortunately, breaks some stuff
  mkdir %{buildroot}%{_qt4_prefix}/mkspecs
  mv %{buildroot}%{_qt4_datadir}/mkspecs/{default,linux-g++*,qconfig.pri} \
     %{buildroot}%{_qt4_prefix}/mkspecs/
  ln -s %{_qt4_datadir}/mkspecs/common %{buildroot}%{_qt4_prefix}/mkspecs/common
%endif
%endif

# qt4.(sh|csh), currently unused
%if 0
install -p -m755 -D %{SOURCE11} %{buildroot}/etc/profile.d/qt4.sh
install -p -m755 -D %{SOURCE12} %{buildroot}/etc/profile.d/qt4.csh
sed -i \
  -e "s|@@QT4DIR@@|%{_qt4_prefix}|" \
  -e "s|@@QT4DOCDIR@@|%{_qt4_docdir}|" \
  %{buildroot}/etc/profile.d/qt4.*
%endif


%if "%{_qt4_libdir}" != "%{_libdir}"
  mkdir -p %{buildroot}/etc/ld.so.conf.d
  echo "%{_qt4_libdir}" > %{buildroot}/etc/ld.so.conf.d/qt4-%{_arch}.conf
%endif

# Trolltech.conf
install -p -m644 -D %{SOURCE4} %{buildroot}%{_qt4_sysconfdir}/Trolltech.conf

# qt4-logo (generic) icons
install -p -m644 -D %{SOURCE30} %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/qt4-logo.png
install -p -m644 -D %{SOURCE31} %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/qt4-logo.png
# linguist icons
for icon in tools/linguist/linguist/images/icons/linguist-*-32.png ; do
  size=$(echo $(basename ${icon}) | cut -d- -f2)
  install -p -m644 -D ${icon} %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/linguist4.png
done

# Qt.pc
cat >%{buildroot}%{_libdir}/pkgconfig/Qt.pc<<EOF
prefix=%{_qt4_prefix}
bindir=%{_qt4_bindir}
datadir=%{_qt4_datadir}
demosdir=%{_qt4_demosdir}
docdir=%{_qt4_docdir}
examplesdir=%{_qt4_examplesdir}
headerdir=%{_qt4_headerdir}
libdir=%{_qt4_libdir}
plugindir=%{_qt4_plugindir}
qmake=%{_qt4_bindir}/qmake
sysconfdir=%{_qt4_sysconfdir}
translationdir=%{_qt4_translationdir}

Name: Qt
Description: Qt Configuration
Version: %{version}
EOF

# rpm macros
mkdir -p %{buildroot}%{_sysconfdir}/rpm
cat >%{buildroot}%{_sysconfdir}/rpm/macros.qt4<<EOF
%%_qt4 %{name}
%%_qt4_version %{version}
%%_qt4_prefix %%{_libdir}/qt4
%%_qt4_bindir %%{_qt4_prefix}/bin
%%_qt4_datadir %%{_qt4_prefix}
%%_qt4_demosdir %%{_qt4_prefix}/demos
%%_qt4_docdir %%{_docdir}/qt4
%%_qt4_examples %%{_qt4_prefix}/examples
%%_qt4_headerdir %%{_includedir}
%%_qt4_libdir %%{_libdir}
%%_qt4_plugindir %%{_qt4_prefix}/plugins
%%_qt4_qmake %%{_qt4_bindir}/qmake
%%_qt4_sysconfdir %%{_sysconfdir}
%%_qt4_translationdir %%{_datadir}/qt4/translations 
EOF

# create/own %%_qt4_plugindir/styles
mkdir %{buildroot}%{_qt4_plugindir}/styles

%if 0%{?phonon:1}
# if building with phonon support, nuke it
rm -f  %{buildroot}%{_qt4_libdir}/libphonon*
rm -rf %{buildroot}%{_qt4_headerdir}/phonon/
rm -rf %{buildroot}%{_qt4_headerdir}/Qt/phonon/
# compat symlink ?  maybe put into phonon-devel instead ?
#ln -s %{_includedir}/KDE/Phonon %{buildroot}%{_qt4_headerdir}/Qt/phonon/
#ln -s ../KDE/Phonon %{buildroot}%{_qt4_headerdir}/Qt/phonon/
rm -rf %{buildroot}%{_libdir}/pkgconfig/phonon.pc
rm -f %{buildroot}%{_qt4_plugindir}/phonon_backend/libphonon_gstreamer.so
%endif


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post devel
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:

%postun devel
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:

%post x11
/sbin/ldconfig
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:

%postun x11
/sbin/ldconfig
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:


%files
%defattr(-,root,root,-)
%doc README* LGPL_EXCEPTION.txt LICENSE.LGPL LICENSE.GPL3
#config /etc/profile.d/qt4.*
%if "%{_qt4_libdir}" != "%{_libdir}"
/etc/ld.so.conf.d/*
%dir %{_qt4_libdir}
%endif
%dir %{_qt4_prefix}
%if "%{_qt4_bindir}" == "%{_bindir}"
%{_qt4_prefix}/bin
%else
%dir %{_qt4_bindir}
%endif
%if "%{_qt4_datadir}" != "%{_datadir}/qt4"
%dir %{_datadir}/qt4
%else
%dir %{_qt4_datadir}
%endif
%if "%{_qt4_sysconfdir}" != "%{_sysconfdir}"
%dir %{_qt4_sysconfdir}
%endif
%config(noreplace) %{_qt4_sysconfdir}/Trolltech.conf
%{_qt4_datadir}/phrasebooks/
%{_qt4_libdir}/libQtCore.so.*
%if 0%{?dbus:1}
%if "%{_qt4_bindir}" != "%{_bindir}"
%{_bindir}/qdbus
%endif
%{_qt4_bindir}/qdbus
%{_qt4_libdir}/libQtDBus.so.*
%endif
%{_qt4_libdir}/libQtNetwork.so.*
%{_qt4_libdir}/libQtScript.so.*
%{_qt4_libdir}/libQtSql.so.*
%{_qt4_libdir}/libQtTest.so.*
%{_qt4_libdir}/libQtXml.so.*
%{_qt4_libdir}/libQtXmlPatterns.so.*
%{_qt4_libdir}/libQtScriptTools.so.*
%dir %{_qt4_plugindir}
%dir %{_qt4_plugindir}/sqldrivers/
%{_qt4_plugindir}/sqldrivers/libqsqlite*
%{_qt4_translationdir}/

%files x11 
%defattr(-,root,root,-)
%{_sysconfdir}/rpm/macros.*
%{_qt4_libdir}/libQt3Support.so.*
%{_qt4_libdir}/libQtAssistantClient.so.*
%{_qt4_libdir}/libQtCLucene.so.*
%{_qt4_libdir}/libQtDesigner.so.*
%{_qt4_libdir}/libQtDesignerComponents.so.*
%{_qt4_libdir}/libQtGui.so.*
%{_qt4_libdir}/libQtHelp.so.*
%{_qt4_libdir}/libQtOpenGL.so.*
%{_qt4_libdir}/libQtSvg.so.*
%{?webkit:%{_qt4_libdir}/libQtWebKit.so.*}
%{_qt4_plugindir}/*
%exclude %{_qt4_plugindir}/designer
%exclude %{_qt4_plugindir}/sqldrivers
%if "%{_qt4_bindir}" != "%{_bindir}"
%{_bindir}/assistant*
%{?dbus:%{_bindir}/qdbusviewer}
%{_bindir}/qt*config*
%endif
%{_qt4_bindir}/assistant*
%{?dbus:%{_qt4_bindir}/qdbusviewer}
%{_qt4_bindir}/qt*config*
%{_datadir}/applications/*qtconfig*.desktop
%{_datadir}/icons/hicolor/*/apps/qt4-logo.*

%files devel
%defattr(-,root,root,-)
%{_qt4_bindir}/lconvert
%{_qt4_bindir}/lrelease*
%{_qt4_bindir}/lupdate*
%{_qt4_bindir}/moc*
%{_qt4_bindir}/pixeltool*
%{_qt4_bindir}/qmake*
%{_qt4_bindir}/qt3to4
%{_qt4_bindir}/rcc*
%{_qt4_bindir}/uic*
%{_qt4_bindir}/qcollectiongenerator
%if 0%{?dbus:1}
%{_qt4_bindir}/qdbuscpp2xml
%{_qt4_bindir}/qdbusxml2cpp
%endif
%{_qt4_bindir}/qhelpconverter
%{_qt4_bindir}/qhelpgenerator
%{_qt4_bindir}/xmlpatterns
%if "%{_qt4_bindir}" != "%{_bindir}"
%{_bindir}/lconvert
%{_bindir}/lrelease*
%{_bindir}/lupdate*
%{_bindir}/pixeltool*
%{_bindir}/moc*
%{_bindir}/qmake*
%{_bindir}/qt3to4
%{_bindir}/rcc*
%{_bindir}/uic*
%{_bindir}/designer*
%{_bindir}/linguist*
%{_bindir}/qcollectiongenerator
%if 0%{?dbus:1}
%{_bindir}/qdbuscpp2xml
%{_bindir}/qdbusxml2cpp
%endif
%{_bindir}/qhelpconverter
%{_bindir}/qhelpgenerator
%{_bindir}/xmlpatterns
%endif
%if "%{_qt4_headerdir}" != "%{_includedir}"
%dir %{_qt4_headerdir}/
%endif
%{_qt4_headerdir}/*
%{_qt4_datadir}/mkspecs/
%if "%{_qt4_datadir}" != "%{_qt4_prefix}"
%{_qt4_prefix}/mkspecs/
%endif
%{_qt4_datadir}/q3porting.xml
%{_qt4_libdir}/libQt*.so
# remaining static lib: libQtUiTools.a 
%{_qt4_libdir}/libQt*.a
%{_qt4_libdir}/libQt*.prl
%{_libdir}/pkgconfig/*.pc
# Qt designer
%{_qt4_bindir}/designer*
%{_qt4_plugindir}/designer/
%{_datadir}/applications/*designer*.desktop
# Qt Linguist
%{_qt4_bindir}/linguist*
%{_datadir}/applications/*linguist*.desktop
%{_datadir}/icons/hicolor/*/apps/linguist4.*

%files doc
%defattr(-,root,root,-)
%dir %{_qt4_docdir}/
%{_qt4_docdir}/html
%{_qt4_docdir}/qch/
%{_qt4_docdir}/src/
%{_qt4_prefix}/doc
%{_qt4_demosdir}/
%{_qt4_examplesdir}/
# Qt Assistant (bin moved to -x11)
%{_datadir}/applications/*assistant*.desktop
# Qt Demo
%{_qt4_bindir}/qt*demo*
%if "%{_qt4_bindir}" != "%{_bindir}"
%{_bindir}/qt*demo*
%endif
%{_datadir}/applications/*qtdemo*.desktop

%if "%{?odbc}" == "-plugin-sql-odbc"
%files odbc 
%defattr(-,root,root,-)
%{_qt4_plugindir}/sqldrivers/libqsqlodbc*
%endif

%if "%{?psql}" == "-plugin-sql-psql"
%files postgresql 
%defattr(-,root,root,-)
%{_qt4_plugindir}/sqldrivers/libqsqlpsql*
%endif

%if "%{?mysql}" == "-plugin-sql-mysql"
%files mysql 
%defattr(-,root,root,-)
%{_qt4_plugindir}/sqldrivers/libqsqlmysql*
%endif


%changelog
* Tue Mar 03 2009 Than Ngo <than@redhat.com> - 4.5.0-1
- 4.5.0

* Fri Feb 27 2009 Rex Dieter <rdieter@fedoraproject.org> - 1:4.5.0-0.8.20090224
- 20090224 snapshot
- adjust pkgconfig hackery

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.5.0-0.7.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 22 2009 Rex Dieter <rdieter@fedoraproject.org> 4.5.0-0.5.rc1
- revert license, change won't land until official 4.5.0 release
- workaround broken qhostaddress.h (#485677)
- Provides: qgtkstyle = 0.1

* Fri Feb 20 2009 Rex Dieter <rdieter@fedoraproject.org> 4.5.0-0.4.rc1
- saner versioned Obsoletes
- -gtkstyle, Obsoletes: qgtkstyle < 0.1
- enable phonon support and associated hackery

* Mon Feb 16 2009 Than Ngo <than@redhat.com> 4.5.0-0.3.rc1
- fix callgrindChildExitCode is uninitialzed

* Sun Feb 15 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.5.0-0.2.rc1
- qt-copy-patches-20090215
- License: +LGPLv2

* Wed Feb 11 2009 Than Ngo <than@redhat.com> - 4.5.0-0.rc1.0
- 4.5.0 rc1

* Thu Feb 05 2009 Rex Dieter <rdieter@fedoraproject.org> 4.4.3-16
- track branches/qt-copy/4.4, and backout previous trunk(qt45) ones

* Mon Feb 02 2009 Than Ngo <than@redhat.com> 4.4.3-15
- disable 0269,0270,0271 patches, it causes issue in systray

* Thu Jan 29 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.4.3-14
- qt-copy-patches-20090129

* Mon Jan 26 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.4.3-13
- Provides: qt4%%{?_isa} = %%version-%%release
- add %%_qt4 to macros.qt4

* Thu Jan 22 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.4.3-12 
- respin (mysql)

* Fri Jan 16 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.4.3-11
- rebuild for new OpenSSL

* Mon Jan 12 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.4.3-10
- drop qt-x11-opensource-src-4.3.4-no-hardcoded-font-aliases.patch (#447298),
  in favor of qt-copy's 0263-fix-fontconfig-handling.diff

* Mon Jan 12 2009 Than Ngo <than@redhat.com> - 4.4.3-9
- qt-copy-patches-20090112

* Tue Dec 30 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.3-8
- qt-copy-patches-20081225

* Fri Dec 12 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.3-7
- rebuild for pkgconfig deps

* Wed Nov 12 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.3-6
- qt-copy-patches-20081112

* Tue Nov 11 2008 Than Ngo <than@redhat.com> 4.4.3-5
- drop 0256-fix-recursive-backingstore-sync-crash.diff, it's
  included in qt-copy-pathes-20081110

* Mon Nov 10 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.3-4
- qt-copy-patches-20081110

* Mon Nov 10 2008 Than Ngo <than@redhat.com> 4.4.3-3
- apply 0256-fix-recursive-backingstore-sync-crash.diff

* Thu Nov 06 2008 Than Ngo <than@redhat.com> 4.4.3-2
- bz#468814, immodule selection behavior is unpredictable without QT_IM_MODULE,
  patch from Peng Wu
- backport fix from 4.5

* Sun Sep 28 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.3-1
- 4.4.3

* Wed Sep 24 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.2-2
- omit systray patch (for now)

* Sat Sep 20 2008 Than Ngo <than@redhat.com> 4.4.2-1
- 4.4.2

* Mon Sep 08 2008 Rex Dieter <rdieter@fedoraproject.org> - 4.4.1-3
- apply QMAKEPATH portion of multilib patch only if needed
- qt-copy-patches-20080908

* Wed Aug 06 2008 Than Ngo <than@redhat.com> -  4.4.1-2
- fix license tag
- fix Obsoletes: qt-sqlite (missing epoch)

* Tue Aug 05 2008 Than Ngo <than@redhat.com> -  4.4.1-1
- 4.4.1

* Tue Aug 05 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-17
- fold -sqlite subpkg into main (#454930)

* Wed Jul 23 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-16
- qt-copy-patches-20080723 (kde#162793)
- omit deprecated phonon bits

* Sat Jul 19 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-15
- fix/workaround spec syntax 

* Sat Jul 19 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-14
- macros.qt4: fix %%_qt4_datadir, %%_qt4_translationdir

* Thu Jul 17 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-13
- (re)fix qconfig-multilib.h for sparc64

* Fri Jul 11 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-12
- qt-copy-patches-20080711

* Mon Jun 23 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-11
- fix dbus conditional (#452487)

* Sat Jun 14 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-10
- strip -lsqlite3 from .pc files (#451490)

* Sat Jun 14 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.4.0-9
- restore -qt4 suffixes

* Fri Jun 13 2008 Than Ngo <than@redhat.com> 4.4.0-8
- drop qt wrapper, make symlinks to /usr/bin

* Tue Jun 10 2008 Than Ngo <than@redhat.com> 4.4.0-7
- fix #450310, multilib issue 

* Fri Jun 06 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-6
- qt-copy-patches-20080606
- drop BR: libungif-devel (not used)
- move libQtXmlPatters, -x11 -> main
- move qdbuscpp2xml, qdbusxml2cpp, xmlpatters, -x11 -> -devel

* Tue May 27 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.4.0-5
- under GNOME, default to QGtkStyle if available

* Mon May 19 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.4.0-4
- don't hardcode incorrect font substitutions (#447298)

* Fri May 16 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-3
- qt-copy-patches-20080516

* Tue May 13 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.4.0-2
- revert _qt4_bindir change for now, needs more work (#446167)

* Tue May 06 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-1
- qt-4.4.0

* Tue Apr 29 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-0.6.rc1
- -webkit (include in -x11 subpkg), drop separate -webkit-devel
- omit qt4-wrapper.sh deps (since it's not used atm)
- qt-copy-patches-20080429
- Obsoletes/Provides: WebKit-qt(-devel) <|= 1.0.0-1  (#442200)

* Thu Apr 24 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-0.5.rc1
- strip -lssl -lcrypto from *.pc files too

* Tue Apr 08 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.4.0-0.4.rc1
- updated patch for #437440 ([as-IN] Consonant combination issue) by Pravin Satpute
- port the patch to Qt 4.4 (the code moved to harfbuzz) and reenable it

* Fri Apr 04 2008 Rex Dieter <rdieter@fedoraproject.org> 4.4.0-0.3.rc1
- qt-4.4.0-rc1
- -xmlpatterns (and drop -no-exceptions)
- -reduce-relocations, -dbus-linked, -openssl-linked
- -no-nas
- -no-phonon (-no-gstreamer), -no-webkit (for now, at least until
  conflicts with WebKit-qt and kdelibs4 are sorted out)
- %%_qt4_bindir -> %%_bindir, avoid qt4-wrapper hackage (#277581, #422291)
- qtconfig.desktop: NoDisplay=true (#244879)

* Wed Apr 02 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.3.4-10
- look for OpenSSL using versioned sonames (#432271)

* Wed Mar 26 2008 Than Ngo <than@redhat.com> 4.3.4-9
- apply patch bz#437440 to fix [as-IN] Consonant combination issue, thanks to Pravin Satpute

* Sun Mar 23 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.3.4-8
- -x11: add missing Provides: qt4-assistant when building as qt

* Thu Mar 13 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.3.4-7
- fix Requires of main package to include Epoch (thanks to Christopher Aillon)

* Wed Mar 12 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.3.4-6
- rename to qt on Fedora >= 9

* Mon Mar 10 2008 Rex Dieter <rdieter@fedoraproject.org> 4.3.4-5
- -x11: move qdbusviewer here

* Wed Mar 05 2008 Than Ngo <than@redhat.com> 4.3.4-4
- upstream patch to fix 4.3 regression

* Fri Feb 29 2008 Than Ngo <than@redhat.com> 4.3.4-3
- respin aliasing.patch, it's safer

* Thu Feb 28 2008 Than Ngo <than@redhat.com> 4.3.4-2
- fix aliasing violations that caused qmake crash

* Fri Feb 22 2008 Rex Dieter <rdieter@fedoraproject.org> 4.3.4-1
- qt-4.3.4

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 4.3.3-9
- Autorebuild for GCC 4.3

* Tue Feb 19 2008 Rex Dieter <rdieter@fedoraproject.org> 4.3.3-8
- qt-copy patches 20080219
- drop -optimized-qmake, for now, to avoid qmake segfaults (gcc43 issue?) 

* Fri Feb 15 2008 Rex Dieter <rdieter@fedoraproject.org> 4.3.3-7
- %%qt_datadir: %%_datadir/qt4 -> %%_libdir/qt4

* Wed Jan 30 2008 Rex Dieter <rdieter@fedoraproject.org> 4.3.3-6
- qt-copy 20080130 patch set (helps address previous 0180-window-role BIC)
- Trolltech.conf: (default) fontsize=10
- License: GPLv2 with exceptions or QPL

* Thu Jan 24 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.3-5
- License: GPLv2 or QPL
- qt-copy patches

* Thu Jan 17 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.3-4
- Qt.pc: fix typo for demosdir (use %%_qt4_demosdir)

* Mon Jan 07 2008 Than Ngo <than@redhat.com> 4.3.3-3
- apply patch from Dirk Müller to fix strict aliasing violations in tool classes

* Fri Dec 21 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.3-2
- -doc: Requires: %%name-assistant, omit assistant bin, 
  -x11: Provides: %%name-assistant (#147948)

* Wed Dec 05 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.3-1
- qt-4.3.3

* Tue Dec 04 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.2-7
- move assistant to -x11, leave .desktop in -doc (#147948)

* Sun Dec 02 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.2-6
- move qdbus to main pkg (#407861)

* Mon Oct 22 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.2-5
- -optimized-qmake

* Fri Oct 19 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.2-4
- slowdown with 4.3.2 (#334281)

* Tue Oct 16 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.2-2
- create/own %%_qt4_plugindir/styles

* Thu Oct 04 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.2-1
- qt-4.3.2
- (re)fix ppc64 segfaults, ppc64 fix upstreamed (previous patch was 
  inadvertantly not applied) (#246324)

* Fri Sep 14 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.1-8
- -x11: Req: redhat-rpm-config rpm, app-wrapper/multilib fun (#277581)

* Thu Sep 13 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.1-7
- include qt4-logo icon, used by qtdemo/qtconfig (#241452)
- linguist.desktop: use new linguist4 icons
- -devel,-x11: %%post/%%postun scriptlets (icons, mimetypes)

* Thu Sep 13 2007 Than Ngo <than@redhat.com> -  4.3.1-4
- fixed bz241452, add qtdemo/qtconfig icons
- fixed bz249242, designer4 - segmentation fault on s390x

* Wed Aug 23 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.1-3
- ppc64 patch (#246324)

* Fri Aug 10 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.1-2
- License: GPLv2 (see also GPL_EXCEPTIONS*.txt)
- omit needless %%check
- (re)add package review comment/reference

* Thu Aug 09 2007 Than Ngo <than@redhat.com> -  4.3.1-1
- update to 4.3.1

* Wed Aug 08 2007 Than Ngo <than@redhat.com> 4.3.0-11
- add %%_qt4_version

* Tue Aug 07 2007 Than Ngo <than@redhat.com> 4.3.0-10
- cleanup

* Sun Jul 15 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.0-9
- multilib broken: qconfig.h (#248768)
- +%%_qt4_demosdir,%%_qt4_examplesdir
- + Qt.pc, provide pkgconfig access to qt4 macros/variables

* Thu Jul 05 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.0-8
- fix %%_qt4_prefix/doc symlink

* Thu Jun 28 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.0-7
- prepare for possible rename qt4 -> qt (+Provides: qt4)
- make _qt4_* macro usage consistent (with %%check's)

* Sat Jun 23 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.0-5
- fix rpm macros, (%%_qt_plugindir, %%_qt4_translationdir}

* Thu Jun 21 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.0-4
- .desktop Category cleanup

* Thu Jun 21 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.0-3
- cleanup qconfig.h/multilib bits, add s390x/s390

* Wed May 30 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.0-2
- ExclusiveArch: %%ix86 -> i386 (for koji)

* Wed May 30 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.0-1
- qt-4.3.0(final)

* Fri May 04 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.3.0-0.5.rc1
- update to 4.3.0 RC1
- drop LD_RUN_PATH hack

* Fri May 04 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.3.0-0.3.snapshot20070423
- update to qt-4.3.0-snapshot-20070423
- build with SSL support (BR openssl-devel)
- drop upstreamed mysql_config.patch

* Wed May 02 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.3.0-0.2.beta
- qt-4.3.0beta
- -system-libtiff, BR: libtiff-devel

* Wed May 02 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.2.3-8
- QFileDialog file wrapping patch (qt#153635, rh#236908)
- License: GPL, dropping LICENSE.QPL (#237702)

* Thu Mar 29 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.2.3-7
- CVE-2007-0242, utf8-bug-qt4-2.diff

* Thu Mar 22 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.2.3-6
- -system-sqlite, BR: sqlite-devel
- drop mysql_config hackery

* Wed Mar 21 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.2.3-5
- strip (all) glib2 libs from .pc files
- prepend _ to rpm macros
- drop Obsoletes: qt4-debug

* Thu Mar 15 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.2.3-3
- make /etc/rpm/macros.qt4 owned only by qt4-devel

* Thu Mar 15 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.2.3-2
- fix mkspecs/common availability (#232392)

* Tue Mar 13 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.2.3-1
- qt-4.2.3
- multilib: move all arch-specific mkspecs bits to %%qt4_prefix/mkspecs (#223663)
- +%%_sysconfdir/rpm/macros.qt4
- +%%config %%qt4_sysconfdir/Trolltech.conf

* Tue Mar 06 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.2.2-8
- multilib: qconfig.pri, /etc/profile.d/* (#223663)

* Mon Mar 05 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.2.2-7
- fixup qconfig-multilib.h for powerpc/powerpc64 (#223663)
- include qt-copy's 0154-qdbuscpp2xml-moc_path.diff (#230875)

* Wed Feb 28 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.2.2-5
- fixup qconfig-multilib.h (#223663)
- qt4.(sh|csh): define QMAKESPEC (#223663)
- null'ify QMAKE_LIBDIR_QT, leave QMAKE_INCDIR_QT alone for now. (#230224)

* Tue Feb 27 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.2.2-3
- drop ./configure -no-reduce-exports (ie, support visibility) 
- multilib issues (#223663)

* Wed Dec 06 2006 Rex Dieter <rexdieter[AT]users.sf.net. 4.2.2-2
- respin for postgresql

* Fri Dec 01 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.2.2-1
- qt-4.2.2 (#218575)

* Wed Nov 15 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.2.1-3
- move libQtDesigner to -x11

* Mon Oct 23 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.2.1-2
- use respun upstream 4.2.1 tarball
- fix pre-modular-X libGL/libGLU deps (#211898)

* Sun Oct 22 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.2.1-1
- qt-4.2.1

* Wed Oct 04 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.2.0-1
- qt-4.2.0(final)

* Thu Sep 28 2006 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.2.0-0.9.20060927
- update to qt-4.2.0-snapshot-20060927
- update QDBus executable names
- -x11: exclude plugins/designer (which belong to -devel)
- BuildConflicts: qt4-devel
- drop -fno-strict-aliasing hack (fc5+)

* Wed Sep 27 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.2.0-0.8.rc1
- qtconfig.desktop: Categories=+AdvancedSettings;Settings

* Fri Sep 08 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.2.0-0.7.rc1
- 4.2.0-rc1

* Fri Aug 28 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.2.0-0.6.20060821
- update to 4.2.0-snapshot-20060821 (same as today's qt-copy)
- -no-separate-debug-info
- - ./configure -xfixes, BR: libXfixes-devel

* Mon Aug 07 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.2.0-0.5.tp1
- fix empty -debuginfo
- use $RPM_OPT_FLAGS

* Thu Jul 20 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.2.0-0.4.tp1
- strip -laudio, -ldbus-1, -lglib-2.0 from .pc files

* Thu Jul 20 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.2.0-0.3.tp1
- -no-reduce-exports (for now)
- -fno-strict-aliasing (fc5+)

* Fri Jul 07 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.2.0-0.2.tp1
- -system-nas-sound, BR: nas-devel (bug # 197937)
- -qdbus (fc6+, BR: dbus-devel >= 0.62)
- -glib (BR: glib2-devel)

* Fri Jun 30 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.2.0-0.1.tp1
- 4.2.0-tp1 (technology preview 1)

* Thu Jun 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.4-5
- make FHS-friendly (bug #196901)
- cleanup %%_bindir symlinks, (consistently) use qt4 postfix

* Wed Jun 28 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.4-4
- x11: split-out gui(x11) from non-gui bits (bug #196899)

* Mon Jun 26 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.4-3
- -debug: drop, adds nothing over -debuginfo, make lib..._debug 
  symlinks instead (bug #196513)
- assistant.desktop: fix tooltip (bug #197039)

* Mon Jun 26 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.4-2
- -devel: include -debug libs (bug #196513)
- -devel: move libQtDesigner here
- -config: mash into main pkg, should be multilib friendly now

* Fri Jun 23 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.4-1
- 4.1.4

* Tue Jun 20 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.3-9
- make each sql plugin optional

* Fri Jun 09 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.3-8
- qmake.conf: undefine QMAKE_STRIP to get useful -debuginfo (bug #193602)
- move (not symlink) .pc files into %%_libdir/pkgconfig

* Thu Jun 08 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.3-7
- *really* fix qt4-wrapper.sh for good this time.

* Mon May 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.3-6
- make qt4-wrapper.sh use rpm when pkg-config/qt4-devel isn't
  installed (#193369)

* Fri May 26 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.3-5
- strip -lXi from .pc files (#193258)
- simplify sql plugin builds via %%buildSQL macro
- -libdir %%qt_libdir 

* Wed May 24 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.3-4
- move (most) %%dir ownership (back) to main pkg

* Sun May 21 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.3-3
- fix %%mysql_libs macro

* Sat May 20 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.3-2
- -mysql: use mysql_config for setting cflags/ldflags.
- -mysql: BR: mysql-devel > 4.0

* Sat May 20 2006 Laurent Rineau <laurent.rineau__fc_extra@normalesup.org>
- Fix the last reference to %{qtdir}/lib: use %{_lib} instead of "lib".
- Fix the ownership of subpackages: they need to own parents of directories they install files in.

* Fri May 19 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.3-1
- 4.1.3
- %%qtdir/lib/*.pc -> %%qtdir/%%_lib/*.pc 
  (hopefully, the last hardcoded reference to %%qtdir/lib)

* Fri May 19 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-20
- fix some unowned dirs
- try harder to purge %%builddir from .pc,.prl files
- -docdir %%_docdir/%%name-doc-%%version, since we use %%doc macro in main pkg
- -doc: own %%qt_docdir
- use qt4-wrapper.sh to ensure launch of qt4 versions of apps that
  (may) overlap with those from qt3 
- use %%qtdir/%%_lib in ld.so.conf.d/*.conf files too

* Tue May 16 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-19
- drop libQtAssistantClient,libQtUiTools shlib patches

* Tue May 16 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-18
- %%_bindir symlinks: qtconfig4 -> qt4config, qtdemo4 -> qt4demo
- -libdir %%qtdir/%%_lib, simplifies %%_lib != lib case
- -docdir %%_docdir/%%name-%%version
- build shared versions of libQtAssistantClient,libQtUiTools too
- strip extraneous -L paths, libs from *.prl files too

* Tue May 16 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-17
- .desktop: Qt -> Qt4, and Comment= (where missing)
- -devel: include -designer here, Obsoletes/Provides: %%name-designer.
   It's small, simplifies things... one less subpkg to worry about.
- -doc: include %%qtdir/doc symlink here
- -docdir %%_docdir/%%name-doc-%%version

* Mon May 15 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-16
- set/use RPM_OPT_FLAGS only for our platform
- (really) don't give %%_bindir symlink for qt3to4 another "4" suffix
- don't add 4 suffix to uic3, rcc (they don't conflict with qt(3)-devel)
- -devel: add  linguist.desktop
- -doc: move assistant here, Provides: %%{name}-assistant, add assistant.desktop
- -doc: add qtdemo.desktop
- -doc: Requires qt4 (instead of qt4-devel)
- assistant4.patch: search for assistant4 instead of (qt3's) assistant in $PATH 
- -qtconfig: add qtconfig.desktop
- updated %%sumaries to mention where (some) tools are, including assistant, linguist,
  qtdemo

* Mon May 15 2006 Laurent Rineau <laurent.rineau__fc_extra@normalesup.org> - 4.1.2-15
- Rename -docs to -doc.
- Files in the -doc subpackage are no longer in %%doc.
- Move qtdemo to the subpackage -doc.
- Fix symlinks in %%{_bindir}.
- Only modify mkspecs/linux-g++*/qmake.conf, instead of all mkspecs/*/qmake.conf.

* Sun May 14 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-14
- remove MapNotify from .desktop file(s).
- install -m644 LICENSE.*
- -docs: don't mark examples as %doc
- drop unused %%debug macro

* Sat May 13 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-13
- include unpackaged pkgconfig files

* Sat May 13 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-12
- fix typos so it actually builds.

* Sat May 13 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-11
- drop optional ld.so.conf.d usage, make mandatory
- make %%_bindir symlinks to all %%qtdir/bin stuff (even qt3to4)
- pkgconfig files: hardlinks -> relative symlinks, strip -L%{_libdir}/mysql
  and -L%%{_builddir}/qt-x11-opensource-src-%%version/lib
- cleanup/simplify Summary/%%description entries
- $RPM_BUILD_ROOT -> %%buildroot, $RPM_BUILD_DIR -> %%_builddir

* Sat May 13 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-10
- cleanup/simplify license bits, include LICENSE.QPL
- drop unused -styles/-Xt subpkg reference
- drop unused motif extention bits
- drop initialpreference from .desktop files

* Fri May 12 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-9
- drop reference to non-existent config.test/unix/checkavail

* Fri May 12 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-8
- simplify build* macros
- lower-case all subpkgs (ie, -MySQL -> -mysql )
- drop BR: perl, sed

* Thu May 11 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-7
- rework %%post/%%postun, mostly to placate rpmlint
- drop Prefix:
- drop use of qt4.(sh|csh), they're empty atm anyway
- use Source'd designer.desktop (instead of inline cat/echo)
- symlinks to %%_bindir: qmake4, designer4, qtconfig4
- drop qtrc, qt4 doesn't use it.
- -docs subpkg for API html docs, demos, examples.
- BR: libXcursor-devel libXi-devel (fc5+)

* Thu Apr 27 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-6
- devel: Requires: pkgconfig

* Sat Apr 15 2006 Simon Perreault <nomis80@nomis80.org> 4.1.2-5
- Disable C++ exceptions.

* Mon Apr 10 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-4
- qt4.(sh|csh): place-holders only, don't define QTDIR (and QTLIB)
  as that (potentially) conflicts with qt-3.x.

* Thu Apr 06 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-2
- -devel: Drop (artificial) Conflicts: qt-devel
- fix %%ld_so_conf_d usage
- %%qtdir/%%_lib symlink

* Wed Apr 05 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.1.2-1
- drop Epoch
- cleanup (a lot!)

* Tue Dec 20 2005 Than Ngo <than@redhat.com> 1:4.1.0-0.1
- update to 4.1.0

* Fri Sep 09 2005 Than Ngo <than@redhat.com> 1:4.0.1-0.1
- update to 4.0.1

