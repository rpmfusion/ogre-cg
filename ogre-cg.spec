Name:           ogre-cg
Version:        1.4.7
Release:        2%{?dist}
Summary:        Object-Oriented Graphics Rendering Engine
License:        LGPLv2+
Group:          System Environment/Libraries
URL:            http://www.ogre3d.org/
# This is http://downloads.sourceforge.net/ogre/ogre-v%(echo %{version} | tr . -).tar.bz2
# stripped all except CgProgramManager plugin and core files needed to build it
Source0:        ogre-%{version}-cg.tar.bz2
# Patch striping everything except CgProgramManager from compilation
Patch0:         ogre-1.4.9-cg.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  zziplib-devel libXaw-devel libXrandr-devel libXxf86vm-devel
BuildRequires:  autoconf automake libtool

# We are building only plugin, so we need main lib
BuildRequires:  ogre-devel
# Cg package
BuildRequires:  Cg
ExclusiveArch:  i386 x86_64

Requires:       ogre = %{version}

%description
This package contains the OGRE CgProgramManager plugin.


%prep
%setup -q -n ogre
%patch0 -p1

# Rebuilding autotools-generated files
autoreconf -v -f -i


%build
%configure --enable-cg --disable-devil --disable-freeimage --disable-openexr
# Don't use rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/OGRE/*.la


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS BUGS COPYING
%{_libdir}/OGRE/*.so


%changelog
* Sun Sep 18 2008 Alexey Torkhov <atorkhov@gmail.com> 1.4.7-2
- Packaged OGRE 1.4.7 Cg plugin basing on Fedora package by Hans de Goede.
