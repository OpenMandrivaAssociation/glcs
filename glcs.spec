%define debug_package	%{nil}

%define name		glcs
%define release		1
%define git             0.6.1
%define version         %{git}
%define develname %mklibname -d glcs
%define libname %mklibname glcs
%define DESTDIR %{buildroot}%{_prefix}
Name:			%{name}
Version:		%{version}
Release:		%{release}
Summary:		ALSA and OpenGL video capture tool
License:		MIT
Group:			Video
URL:			https://github.com/lano1106/glcs
#git clone --recursive https://github.com/lano1106/glcs.git
Source0:		glcs.tar.g 
Source100:      glcs.rpmlintrc
ExclusiveArch:		i586 x86_64
BuildRequires:		cmake 
BuildRequires:		pkgconfig(libpng)
BuildRequires:		pkgconfig(xorg-server)
BuildRequires:		gcc 
BuildRequires:		gcc-c++ 
BuildRequires:		make 
BuildRequires:		libelfhacks-devel
BuildRequires:		libpacketstream-devel
BuildRequires:		pkgconfig(gl)
BuildRequires:		pkgconfig(glu)
BuildRequires:		pkgconfig(ao)
BuildRequires:		pkgconfig(xxf86vm)
BuildRequires:		pkgconfig(alsa)
BuildRequires:      	png-devel
BuildRequires:      	doxygen
Requires:               %{libname}  = %{version}-%{release}
Obsoletes:		glc
Conflicts:		glc


%description	
glcs is an ALSA and OpenGL video capture tool that you 
can use to record the output from opengl applications.

%prep  
%setup -qn %{name}

%build 
%ifarch x86_64
export CFLAGS="$CFLAGS -m64"
%endif
export CC="/usr/bin/gcc -pthread"
./build.sh /usr

%install 
%makeinstall_std -C build

pushd elfhacks/build
%makeinstall_std
popd

pushd packetstream/build
%makeinstall_std
pushd 

install -d -m755 %DESTDIR/share/glcs/scripts
install -m755 scripts/capture.sh %DESTDIR/share/glcs/scripts/capture.sh   
install -m755 scripts/pipe_ffmpeg.sh %DESTDIR/share/glcs/scripts/pipe_ffmpeg.sh   
install -m755 scripts/pipe_ffmpeg.sh %DESTDIR/share/glcs/scripts/webcam_overlay_mix_audio.sh 

doxygen Doxyfile


%ifarch x86_64
install -d   %{buildroot}%{_libdir}
mv %{buildroot}%{_prefix}/lib/{libglc*,libpacketstream*,libelfhacks*} %{buildroot}%{_libdir}/

%endif



%files -n %{name}
%doc COPYING README.md NEWS doc/html doc/latex
%{_bindir}/glc-capture
%{_bindir}/glc-play
%{_datadir}/glcs/scripts

#------------------
%package -n %{libname}
Summary:   Shared library for %{name}
Group:     System/Libraries
Requires:  %{name}

%description -n %{libname}
This project provides a client library for %{name}

%files -n %{libname}
%doc COPYING README.md NEWS
%{_libdir}/libglc*
%{_libdir}/libelfhacks*
%{_libdir}/libpacketstream*
%exclude %{_libdir}/libglc-play.so
%exclude %{_libdir}/libglc-hook.so
%exclude %{_libdir}/libglc-capture.so
%exclude %{_libdir}/libglc-core.so
%exclude %{_libdir}/libglc-export.so
%exclude %{_libdir}/libpacketstream.so
%exclude %{_libdir}/libelfhacks.so

#-----------------
%package -n %{develname}
Summary: Development files for %{name}
Provides: %{name}-devel = %{version}-%{release}
Requires: %{name} = %{version}-%{release}

%description -n %{develname}
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%files -n %{develname}
%doc COPYING README.md NEWS
%{_includedir}/elfhacks.h
%{_includedir}/packetstream.h
%{_libdir}/libglc-play.so
%{_libdir}/libglc-hook.so
%{_libdir}/libglc-capture.so
%{_libdir}/libglc-core.so
%{_libdir}/libglc-export.so
%{_libdir}/libpacketstream.so
%{_libdir}/libelfhacks.so















