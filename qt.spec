%define qtdir %{_libdir}/%{name}-%{version}
%define type x11
%define rel 5
%define beta 0
Version: 2.3.1

%if "%{type}" == "x11"
Summary: The shared library for the Qt GUI toolkit.
%elseif "%{type}" == "embedded"
Summary: The shared library for the Qt GUI toolkit for framebuffer devices.
%elseif "%{type}" == "nox"
Summary: The shared library for the Qt GUI toolkit.
%endif
%if "%{type}" == "nox"
%define file embedded
%else
%define file %{type}
%endif
%if "%{type}" == "x11"
Name: qt
BuildRequires: XFree86-devel >= 4.0.2
%else
Name: qt-%{type}
%endif
%if "%{beta}" == "0"
Release: %{rel}
Source: ftp://ftp.troll.no/qt/source/qt-%{file}-%{version}.tar.bz2
%else
Release: 0.%{beta}.%{rel}
Source: ftp://ftp.troll.no/qt/source/qt-%{file}-%{version}-%{beta}.tar.bz2
%endif
Source1: qt.fontguess
Patch0: qt-2.1.0-huge_val.patch
Patch1: qt-2.3.1-LPRng.patch
Patch2: qt-2.3.1-glweak.patch
Patch3: qt-2.3.1-qtcopy.patch
# Japanese patches
Patch50: http://www.kde.gr.jp/patch/qt-2.3.1-xim-20010617.diff
Patch51: http://www.kde.gr.jp/patch/qt-2.3.1-qclipboard-20010617.diff
Patch52: http://www.kde.gr.jp/patch/qt-2.3.1-qstring-toDouble-i18n-20010617.diff
Patch53: http://www.kde.gr.jp/patch/qt-2.3.1-qpsprinter-ja-20010620.diff
Patch54: http://www.kde.gr.jp/patch/qt-2.3.1-showFullScreen-fix-20010624.diff
# Patches 100-200 are for Qt-x11 only
Patch100: qt-2.3.0-euro.patch
Patch101: qt-2.3.1-aahack.patch
# Patches 200-300 are for Qt-embedded only
Epoch: 1
URL: http://www.troll.no/
License: GPL/QPL
Group: System Environment/Libraries
Buildroot: %{_tmppath}/%{name}-root
Prereq: /sbin/ldconfig
Prefix: %{qtdir}
BuildRequires: gcc-c++, libstdc++, libstdc++-devel, libmng-devel, glibc-devel, libjpeg-devel, libpng-devel, zlib-devel, libungif-devel, libmng-static

%package devel
%if "%{type}" == "x11"
Summary: Development files and documentation for the Qt GUI toolkit.
%elseif "%{type}" == "embedded"
Summary: Development files and documentation for the Qt GUI toolkit for framebuffer devices.
%elseif "%{type}" == "nox"
Summary: Development files and documentation for the Qt GUI toolkit.
%endif
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%if "%{type}" == "x11"
%package Xt
Summary: An Xt (X Toolkit) compatibility add-on for the Qt GUI toolkit.
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
%endif

%package static
%if "%{type}" == "x11"
Summary: A version of the Qt GUI toolkit for static linking.
%elseif "%{type}" == "embedded"
Summary: Version of the Qt GUI toolkit for framebuffer devices for static linking
%elseif "%{type}" == "nox"
Summary: A version of the Qt GUI toolkit for static linking.
%endif
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}

%package designer
%if "%{type}" == "x11"
Summary: An interface designer for the Qt toolkit.
%elseif "%{type}" == "embedded"
Summary: Interface designer (IDE) for the Qt toolkit for framebuffer devices
%elseif "%{type}" == "nox"
Summary: An interface designer for the Qt toolkit.
%endif
Group: Development/Tools
Requires: %{name}-devel = %{version}-%{release}

%description
Qt is a GUI software toolkit that simplifies the task of writing and
maintaining GUI (Graphical User Interface) applications for the X
Window System. Qt is written in C++ and is fully object-oriented.
This package contains the shared library needed to run Qt
applications, as well as the README files for Qt.

%if "%{type}" == "x11"
%elseif "%{type}" == "embedded"
%elseif "%{type}" == "nox"
%endif
%description devel
The qt-devel package contains the files necessary to develop
applications using the Qt GUI toolkit: the header files, the Qt meta
object compiler, the man pages, the HTML documentation, and example
programs.

%{_docdir}/%{name}-devel-%{version}/html/index.html, which
%if "%{type}" == "x11"
%elseif "%{type}" == "embedded"
%elseif "%{type}" == "nox"
%endif
%if "%{type}" == "x11"
%description Xt
An Xt (X Toolkit) compatibility add-on for the Qt GUI toolkit.


%description static
The qt-static package contains the files necessary to link
applications to the qt GUI toolkit statically (rather than
dynamically). Statically linked applications do not require the
library to be installed on the system running the application.

%description designer
The qt-designer package contains a user interface designer tool for
the Qt toolkit.

%prep
%if "%{beta}" == "0"
%setup -q -n qt-%{version}
%else
%setup -q -n qt-%{version}-%{beta}
%endif
%if "%{type}" == "nox"
find . |xargs perl -pi -e "s,-fno-rtti,-frtti,g" # We want to compile kdelibs...
%endif
[ -f Makefile.cvs ] && make -f Makefile.cvs # this is for qt-copy in KDE CVS
rm -rf tools/designer/examples
%patch0 -p0 -b .hugeval
%patch1 -p1 -b .lprng
%patch2 -p1 -b .glweak
%patch3 -p1 -b .qtcopy

%if "%{type}" == "x11"
%patch50 -p1 -b .jp1
%patch51 -p1 -b .jp2
%patch52 -p1 -b .jp3
%patch53 -p1 -b .jp4
%patch54 -p1 -b .jp5
%endif

%if "%{type}" == "x11"
%patch100 -p1 -b .euro
%patch101 -p1 -b .aahack
%endif

# Get rid of bad RPATHs
perl -pi -e "s|^SYSCONF_RPATH_QT.*|SYSCONF_RPATH_QT        = -Wl,-rpath,%{qtdir}/lib|g" configs/*


%build
find . -type d -name CVS | xargs rm -rf
export QTDIR=`/bin/pwd`
OPTFLAGS=`echo $RPM_OPT_FLAGS |sed -e s/-fno-rtti/-frtti/`

perl -pi -e "s/-O2/$OPTFLAGS -fno-exceptions/g" configs/linux* configs/gnu* configs/freebsd*

if [ -x /usr/bin/getconf ] ; then
    NRPROC=$(/usr/bin/getconf _NPROCESSORS_ONLN)
    if [ $NRPROC -eq 0 ] ; then
   NRPROC=1
    fi
else
    NRPROC=1
fi

# build static libraries first,
# don't build examples, tools and tutorials with static libraries here
%if "%{type}" == "x11"
./configure -release -static -gif -xft -sm -system-libmng -system-zlib \
	-system-libpng -system-jpeg -no-g++-exceptions -thread <<EOF
yes
EOF
%elseif "%{type}" == "embedded" || "%{type}" == "nox"
./configure -release -static -gif -no-sm -thread -system-zlib \
	-system-libpng -system-libmng -system-jpeg -no-g++-exceptions \
	-accel-voodoo3 -accel-mach64 -accel-matrox \
	-qvfb -vnc <<EOF
yes
5
v,4,8,16,24,32
EOF
%endif

make src-moc src-mt sub-src -j $NRPROC
%if "%{type}" == "x11"
make SYSCONF_CXX="g++ -fPIC" SYSCONF_CC="gcc -fPIC" -C extensions/xt/src -j $NRPROC
%endif

# build shared libraries
%if "%{type}" == "x11"
./configure -release -shared -gif -xft -sm -system-libmng -system-zlib \
	-system-libpng -system-jpeg -no-g++-exceptions -thread <<EOF
yes
EOF
%elseif "%{type}" == "embedded" || "%{type}" == "nox"
./configure -release -shared -gif -no-sm -thread -system-zlib \
        -system-libpng -system-libmng -system-jpeg -no-g++-exceptions \
        -accel-voodoo3 -accel-mach64 -accel-matrox \
	-qvfb -vnc <<EOF
yes
5
v,4,8,16,24,32
EOF
%endif

make src-moc src-mt sub-src sub-tools -j $NRPROC
%if "%{type}" == "x11"
make -C extensions/xt/src -j $NRPROC
%elseif "%{type}" == "embedded" || "%{type}" == "nox"
make -C tools/designer -j $NRPROC
%endif

%install
rm -rf $RPM_BUILD_ROOT
export QTDIR=`/bin/pwd`

mkdir -p $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/{bin,include,lib}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/{man1,man3}

# strip binaries
for i in bin/*; do
  strip -R .comment $i || :
done

# install shared and static libraries
install -m 755 bin/* $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/bin
install -m 755 lib/* $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/lib

%if "%{type}" == "x11"
ln -sf libqt.so.%{version} $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/lib/libqt.so.2.3
ln -sf libqt.so.%{version} $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/lib/libqt.so.2
ln -sf libqt.so.%{version} $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/lib/libqt.so
ln -sf libqt-mt.so.%{version} $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/lib/libqt-mt.so.2.3
ln -sf libqt-mt.so.%{version} $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/lib/libqt-mt.so.2
ln -sf libqt-mt.so.%{version} $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/lib/libqt-mt.so
%else
ln -sf libqte.so.%{version} $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/lib/libqte.so.2.3
ln -sf libqte.so.%{version} $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/lib/libqte.so.2
ln -sf libqte.so.%{version} $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/lib/libqte.so
ln -sf libqte-mt.so.%{version} $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/lib/libqte-mt.so.2.3
ln -sf libqte-mt.so.%{version} $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/lib/libqte-mt.so.2
ln -sf libqte-mt.so.%{version} $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/lib/libqte-mt.so
%endif
ln -sf libqutil.so.1.0.0 $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/lib/libqutil.so.1.0
ln -sf libqutil.so.1.0.0 $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/lib/libqutil.so.1
ln -sf libqutil.so.1.0.0 $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/lib/libqutil.so
%if "%{type}" == "x11"
ln -sf libqxt.so.0.3.0 $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/lib/libqxt.so.0.3
ln -sf libqxt.so.0.3.0 $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/lib/libqxt.so.0
ln -sf libqxt.so.0.3.0 $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/lib/libqxt.so
%endif

# install man pages
cp -fR src/moc/moc.1 $RPM_BUILD_ROOT%{_mandir}/man1
cp -fR doc/man/man3/* $RPM_BUILD_ROOT%{_mandir}/man3
rm -rf doc/man

%if "%{type}" != "x11"
# Rename man pages, we don't want to conflict with the x11 Qt
for i in $RPM_BUILD_ROOT%{_mandir}/man1/*; do
	mv $i `echo $i |sed -e "s/\.1/-%{type}.1/"`
done
for i in $RPM_BUILD_ROOT%{_mandir}/man3/*; do
	mv $i `echo $i |sed -e "s/\.3/-%{type}.3/"`
done
%endif

# Compensate for Qt's broken Makefiles
for i in makeqpf mergetr msg2qm qconfig; do
	make -C tools/$i
	strip -R .comment tools/$i/$i
	install -m 755 tools/$i/$i $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/bin
done

# clean up
make -C tutorial clean
make -C examples clean
find examples -name Makefile | xargs perl -pi -e 's|\.\./\.\.|\$\(QTDIR\)|'
find examples -type f -perm 755 | xargs strip -R .comment || :
find tutorial -name Makefile | xargs perl -pi -e 's|\.\./\.\.|\$\(QTDIR\)|'
find tutorial -type f -perm 755 | xargs strip -R .comment || :

for a in */*/Makefile ; do
  sed 's|^SYSCONF_MOC.*|SYSCONF_MOC		= %{qtdir}/bin/moc|' < $a > ${a}.2
  mv -v ${a}.2 $a
done

rm -f include/qt_mac.h include/qt_windows.h
rm -f include/jri.h include/jritypes.h include/npapi.h include/npupp.h

cp -frL include/. $RPM_BUILD_ROOT%{qtdir}/include || \
	cp -fr include/. $RPM_BUILD_ROOT%{qtdir}/include
%if "%{type}" == "x11"
chmod -R a+r $RPM_BUILD_ROOT%{qtdir}/lib/libqt.so*
%else
chmod -R a+r $RPM_BUILD_ROOT%{qtdir}/lib/libqte.so*
%endif

%if "%{type}" == "embedded" || "%{type}" == "nox"
cp -aR etc $RPM_BUILD_ROOT%{qtdir}
%endif

mkdir -p $RPM_BUILD_ROOT/etc/profile.d
cat > $RPM_BUILD_ROOT/etc/profile.d/qt.sh <<EOF
# Qt initialization script (sh)
if [ -z "\$QTDIR" ] ; then
	QTDIR="%{qtdir}"
fi
export QTDIR
EOF

chmod 755 $RPM_BUILD_ROOT/etc/profile.d/qt.sh

cat > $RPM_BUILD_ROOT/etc/profile.d/qt.csh <<EOF
# Qt initialization script (csh)
if ( \$?QTDIR ) then
         exit
endif
setenv QTDIR %{qtdir}
EOF

chmod 755 $RPM_BUILD_ROOT/etc/profile.d/qt.csh

mkdir -p $RPM_BUILD_ROOT/usr/bin
%if "%{type}" == "x11"
for i in moc uic designer makeqpf mergetr msg2qm qconfig qt20fix qtrename140 findtr; do
	ln -sf ../lib/%{name}-%{version}/bin/$i $RPM_BUILD_ROOT/usr/bin
done
%else
for i in moc uic designer makeqpf mergetr msg2qm qconfig qt20fix qtrename140 findtr; do
	ln -sf ../lib/%{name}-%{version}/bin/$i $RPM_BUILD_ROOT/usr/bin/$i-%{type}
done
%endif

# make symbolic link to qt docdir
if echo %{_docdir} | grep  share >& /dev/null ; then
  ln -s  ../../share/doc/%{name}-devel-%{version} $RPM_BUILD_ROOT%{qtdir}/doc
else
  ln -s  ../../doc/%{name}-devel-%{version} $RPM_BUILD_ROOT%{qtdir}/doc
fi

# Install the qt.fontguess file
mkdir -p $RPM_BUILD_ROOT/etc
install -c -m 644 %{SOURCE1} $RPM_BUILD_ROOT/etc

%clean
rm -rf $RPM_BUILD_ROOT

%post
%if "%{type}" == "x11"
grep -v '^%{_libdir}/qt-2' /etc/ld.so.conf >/etc/ld.so.conf.new
mv -f /etc/ld.so.conf.new /etc/ld.so.conf
%else
grep -v '^%{_libdir}/qt-%{type}-2' /etc/ld.so.conf >/etc/ld.so.conf.new
mv -f /etc/ld.so.conf.new /etc/ld.so.conf
%endif
echo "%{qtdir}/lib" >> /etc/ld.so.conf
/sbin/ldconfig

%postun
if [ $1 = 0 ]; then
  grep -v '^%{qtdir}/lib$' /etc/ld.so.conf > /etc/ld.so.conf.new 2>/dev/null
  mv -f /etc/ld.so.conf.new /etc/ld.so.conf
fi
/sbin/ldconfig

%triggerpostun -- qt < 2.1.0-4.beta1
if ! grep -q '^%{qtdir}/lib$' /etc/ld.so.conf; then
  echo "%{qtdir}/lib" >> /etc/ld.so.conf
fi
/sbin/ldconfig


%files
%defattr(-,root,root,-)
%if "%{type}" == "x11"
%doc ANNOUNCE FAQ LICENSE.QPL PORTING README* changes*
%else
%doc README* changes*
%endif
%dir %{qtdir}
%dir %{qtdir}/lib
%config(noreplace) /etc/qt.fontguess
%if "%{type}" == "x11"
%{qtdir}/lib/libqt.so.*
%{qtdir}/lib/libqt-mt.so.*
%else
%{qtdir}/lib/libqte.so.*
%{qtdir}/lib/libqte-mt.so.*
%endif
%{qtdir}/lib/libqutil.so.*
%if "%{type}" == "embedded" || "%{type}" == "nox"
%dir %{qtdir}/etc
%dir %{qtdir}/etc/fonts
%dir %{qtdir}/etc/sounds
%{qtdir}/etc/fonts/*
%{qtdir}/etc/sounds/*
%endif

%files devel
%defattr(-,root,root,-)
%if "%{type}" == "x11"
%attr(0755,root,root) %config /etc/profile.d/*
%endif
%{qtdir}/bin/moc
%{qtdir}/bin/uic
%{qtdir}/bin/findtr
%{qtdir}/bin/qt20fix
%{qtdir}/bin/qtrename140
%{qtdir}/bin/makeqpf
%{qtdir}/bin/mergetr
%{qtdir}/bin/msg2qm
%{qtdir}/bin/qconfig
%{qtdir}/include
%{qtdir}/doc
%if "%{type}" == "x11"
%{qtdir}/lib/libqt.so
%{qtdir}/lib/libqt-mt.so
%else
%{qtdir}/lib/libqte.so
%{qtdir}/lib/libqte-mt.so
%endif
%{qtdir}/lib/libqutil.so
%{_mandir}/*/*
%{_bindir}/moc*
%{_bindir}/uic*
%{_bindir}/findtr*
%{_bindir}/qt20fix*
%{_bindir}/qtrename140*
%{_bindir}/makeqpf*
%{_bindir}/mergetr*
%{_bindir}/msg2qm*
%{_bindir}/qconfig*

%doc doc/*
%doc examples
%doc tutorial

%if "%{type}" == "x11"
%post Xt -p /sbin/ldconfig
%postun Xt -p /sbin/ldconfig

%files Xt
%defattr(-,root,root,-)
%{qtdir}/lib/libqxt.so*
%endif

%files static
%defattr(-,root,root,-)
%{qtdir}/lib/*.a

%files designer
%defattr(-,root,root,-)
%{_bindir}/designer*
%{qtdir}/bin/designer

%changelog
* Mon Aug 27 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.3.1-5
- Build libqxt with -fPIC (#49960)

* Mon Aug 20 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.3.1-4
- Add qt.fontguess file (fixes Japanese/Korean/Chinese)
- Merge fixes from KDE's qt-copy CVS tree, primarily printing fixes
- Remove rpath references to build directories (#51956)

* Wed Aug  8 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.3.1-3
- Add a hack to get nice anti-aliased fonts out of the box

* Sat Jul 28 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.3.1-2
- Add Japanese patches

* Sat Jun 16 2001 Than Ngo <than@redhat.com> 2.3.1-1
- update to 2.3.1 release
- remove some patch files which are included in 2.3.1
- adapt 2 patch files for 2.3.1

* Tue Jun 12 2001 Harald Hoyer <harald@redhat.de> 2.3.0-7
- added weak symbols to remove GL dependency

* Fri Apr 27 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.3.0-6
- Fix crashes on ia64, Patch from Bill Nottingham <notting@redhat.com>
- Allow building qt-nox

* Fri Apr 20 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.3.0-5
- Make sure uic and designer use the libqutil from the source tree, not
  a previously installed one.
  Linking uic-x11 against libqutil-embedded is definitely not a feature. ;)
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
