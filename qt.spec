%define KDEDATE 20000721
Name: qt
Summary: The shared library for the Qt GUI toolkit.
Version: 2.2.0
Release: 0.1.%{KDEDATE}j1
Source0: ftp://ftp.troll.no/qt/source/qt-%{version}-20000720.tar.bz2
# Source3 is generated from ftp://ftp.netscape.com/pub/sdk/plugin/unix/unix-sdk-3.0b5.tar.Z
Source3: qt-nsplugin-files.tar.bz2
Patch0: qt-2.1.0-huge_val.patch
Patch1: qt-2.1.1-connect.patch
Patch10:qt-2.2.0-m17n-20000728.diff
Patch11: qt-2.2.0-codec-20000728.diff
URL: http://www.troll.no/
Copyright: QPL
Group: System Environment/Libraries
Buildroot: %{_tmppath}/%{name}-root
Prereq: /sbin/ldconfig
ExcludeArch: ia64

%package devel
Summary: Development files and documentation for the Qt GUI toolkit.
Group: Development/Libraries

%package GL
Summary: An OpenGL add-on for the Qt software toolkit.
Group: System Environment/Libraries
Requires: Mesa
BuildPrereq: Mesa-devel

%package NSPlugin
Summary: An add-on for creating Netscape plug-ins using the Qt GUI toolkit.
Group: System Environment/Libraries

%package Xt
Summary: An Xt (X Toolkit) compatibility add-on for the Qt GUI toolkit.
Group: System Environment/Libraries

%description
Qt is a GUI software toolkit which simplifies the task of writing and
maintaining GUI (Graphical User Interface) applications for the X
Window System. Qt is written in C++ and is fully object-oriented.

This package contains the shared library needed to run Qt
applications, as well as the README files for Qt.

%description devel
The qt-devel package contains the files necessary to develop
applications using the Qt GUI toolkit: the header files, the Qt meta
object compiler, the man pages, the HTML documentation and example
programs.  See http://www.troll.no/products/qt.html for more
information about Qt, or look at /usr/lib/qt/html/index.html, which
provides Qt documentation in HTML format.

Install qt-devel if you want to develop GUI applications using the Qt
toolkit.

%description GL
The qt-GL package contains an OpenGL (3-D graphics) add-on for the Qt
GUI software toolkit.  You'll need to install the Mesa 3-D graphics
library if you want to use qt-GL.

%description NSPlugin
An add-on for developing Netscape plug-ins with the Qt GUI toolkit.

%description Xt
An Xt (X Toolkit) compatibility add-on for the Qt GUI toolkit.

%prep
%setup -q -n qt-copy
%patch0 -p0 -b .hugeval
%patch1 -p1 -b .connect
%patch10 -p1
%patch11 -p1

%build
make -f Makefile.cvs
find . -type d -name CVS | xargs rm -rf
export QTDIR=`/bin/pwd`
OPTFLAGS=`echo $RPM_OPT_FLAGS |sed -e s/-fno-rtti//`
OPTFLAGS=`echo $OPTFLAGS |sed -e s/-fno-exceptions//`
%ifarch ia64
OPTFLAGS=`echo $OPTFLAGS | sed -e s/-O2/-O0/`
%endif
perl -pi -e "s/-O2/$OPTFLAGS/g" configs/linux* configs/gnu* configs/freebsd*

./configure -release -shared -gif -sm -system-zlib -system-libpng \
	-system-jpeg -thread

if [ -x /usr/bin/getconf ] ; then
    NRPROC=$(/usr/bin/getconf _NPROCESSORS_ONLN)
    if [ $NRPROC -eq 0 ] ; then
   NRPROC=1
    fi
else
    NRPROC=1
fi  

make -j $NRPROC

cd extensions/opengl/src
make -j $NRPROC
cd ../../nsplugin/src
tar xIf %{SOURCE3}
make -j $NRPROC 
cd ../../xt/src
make -j $NRPROC

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_libdir}/qt-%{version}/{bin,include,lib}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/{man1,man3}

strip -R .comment bin/{mergetr,moc,msg2qm}
install -m 755 bin/* $RPM_BUILD_ROOT%{_libdir}/qt-%{version}/bin
cp lib/libqt.so.%{version} $RPM_BUILD_ROOT%{_libdir}/qt-%{version}/lib
ln -sf libqt.so.%{version} $RPM_BUILD_ROOT%{_libdir}/qt-%{version}/lib/libqt.so.2
ln -sf libqt.so.2 $RPM_BUILD_ROOT%{_libdir}/qt-%{version}/lib/libqt.so
cp -fR src/moc/moc.1 $RPM_BUILD_ROOT%{_mandir}/man1
cp doc/man/man3/* $RPM_BUILD_ROOT%{_mandir}/man3


for i in libqgl.a libqnp.a libqxt.a; do
  cp lib/$i $RPM_BUILD_ROOT%{_libdir}/qt-%{version}/lib
done

make -C tutorial clean
make -C examples clean
find examples -name Makefile | xargs perl -pi -e 's|\.\./\.\.|\$\(QTDIR\)|'
find examples -type f -perm 755 | xargs strip -R .comment || :
find tutorial -name Makefile | xargs perl -pi -e 's|\.\./\.\.|\$\(QTDIR\)|'
find tutorial -type f -perm 755 | xargs strip -R .comment || :

for a in */*/Makefile ; do
  sed 's-^SYSCONF_MOC.*-SYSCONF_MOC		= /usr/bin/moc-' < $a > ${a}.2
  mv -v ${a}.2 $a
done

rm -f include/qt_mac.h include/qt_windows.h
cp -fR include/. $RPM_BUILD_ROOT%{_libdir}/qt-%{version}/include
chmod -R a+r $RPM_BUILD_ROOT%{_libdir}/qt-%{version}/lib/libqt.so*

mkdir -p $RPM_BUILD_ROOT/etc/profile.d
cat > $RPM_BUILD_ROOT/etc/profile.d/qt.sh <<EOF
# Qt initialization script (sh)
if [ -z "\$QTDIR" ] ; then
	QTDIR="/usr/lib/qt-%{version}"
fi
export QTDIR
EOF

chmod 755 $RPM_BUILD_ROOT/etc/profile.d/qt.sh

cat > $RPM_BUILD_ROOT/etc/profile.d/qt.csh <<EOF
# Qt initialization script (csh)
if ( \$?QTDIR ) then
         exit
endif
setenv QTDIR /usr/lib/qt-%{version}
EOF

chmod 755 $RPM_BUILD_ROOT/etc/profile.d/qt.csh

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man3
mv doc/man/man3/* $RPM_BUILD_ROOT%{_mandir}/man3
rm -rf doc/man

%clean
rm -rf $RPM_BUILD_ROOT

%post
if ! grep -q '^/usr/lib/qt-%{version}/lib$' /etc/ld.so.conf; then
  echo "/usr/lib/qt-%{version}/lib" >> /etc/ld.so.conf
fi
/sbin/ldconfig

%postun
if [ $1 = 0 ]; then
  grep -v '^/usr/lib/qt-%{version}/lib$' /etc/ld.so.conf > /etc/ld.so.conf.new 2>/dev/null
  cat /etc/ld.so.conf.new > /etc/ld.so.conf
  rm -f /etc/ld.so.conf.new
  /sbin/ldconfig
fi

%triggerpostun -- qt < 2.1.0-4.beta1
if ! grep -q '^/usr/lib/qt-%{version}/lib$' /etc/ld.so.conf; then
  echo "/usr/lib/qt-%{version}/lib" >> /etc/ld.so.conf
fi
/sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc ANNOUNCE FAQ LICENSE.QPL PORTING README README.QT changes-2.1.0
%dir /usr/lib/qt-%{version}
%dir /usr/lib/qt-%{version}/lib
/usr/lib/qt-%{version}/lib/libqt.so.%{version}
/usr/lib/qt-%{version}/lib/libqt.so.2

%files devel
%defattr(-,root,root,-)
%attr(0755,root,root) %config /etc/profile.d/*
%{_libdir}/qt-%{version}/bin
%{_libdir}/qt-%{version}/include
%{_libdir}/qt-%{version}/lib/libqt.so
%{_mandir}/*/*
%doc doc/*
%doc examples
%doc tutorial

%files GL
%defattr(-,root,root,-)
%{_libdir}/qt-%{version}/lib/libqgl.a

%files NSPlugin
%defattr(-,root,root,-)
%{_libdir}/qt-%{version}/lib/libqnp.a

%files Xt
%defattr(-,root,root,-)
%{_libdir}/qt-%{version}/lib/libqxt.a

%changelog
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
