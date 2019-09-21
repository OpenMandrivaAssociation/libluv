%define major 1
%define libname %mklibname luv %{major}
%define devname %mklibname -d luv %{major}

Summary:	Bare libuv bindings for lua
Name:		libluv
Version:	1.30.1
Release:	1
License:	LGPLv2+
Group:		System/Libraries
Url:		https://github.com/luvit
Source0:	https://github.com/luvit/luv/archive/%{version}-1.tar.gz
Source1:	https://github.com/keplerproject/lua-compat-5.3/raw/master/c-api/compat-5.3.h
Source2:	https://github.com/keplerproject/lua-compat-5.3/raw/master/c-api/compat-5.3.c
BuildRequires:	pkgconfig(libuv)
BuildRequires:	pkgconfig(luajit)
BuildRequires:	cmake

%description
This library makes libuv available to lua scripts.
It was made for the luvit project but should usable from nearly any lua project.

%package -n %{libname}
Summary:	Bare libuv bindings for lua
Group:		System/Libraries

%description -n %{libname}
This library makes libuv available to lua scripts.
It was made for the luvit project but should usable from nearly any lua project.

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package includes the development files for %{name}.

%prep
%setup -q -n luv-%{version}-1
%autopatch -p1
mkdir -p src/c-api/
install -m 0644 %{SOURCE2} %{SOURCE1} src/c-api/

%build
cmake -DWITH_SHARED_LIBUV=ON -DLUA_BUILD_TYPE=System -DBUILD_MODULE=OFF -DBUILD_SHARED_LIBS=ON -DCMAKE_INSTALL_PREFIX=%{_prefix} -DINSTALL_LIB_DIR=%{_libdir} .
#cmake -DWITH_SHARED_LIBUV=ON -DLUA_BUILD_TYPE=System -DBUILD_MODULE=OFF -DBUILD_SHARED_LIBS=ON
%make_build

%install
%make_install

%files -n %{libname}
%{_libdir}/%{name}.so.%{major}*

%files -n %{devname}
%{_includedir}/luv
%{_libdir}/libluv.so
%{_libdir}/pkgconfig/libluv.pc
