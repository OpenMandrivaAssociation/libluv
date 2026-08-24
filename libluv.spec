%define         major 1
%define         devel %mklibname %{name} %{major} -d

%define         dlver %{version}-2
%define         ver %(echo %{dlver} | tr - .)

%define		libname %mklibname luv %{major}
%define		devname %mklibname -d luv
%define		lualibname %mklibname -d luv-lua

# Bootstrap: libluv:-lua or libluv:-luajit (or both).
%bcond_without lua
%bcond_without luajit

Name:           libluv
Version:        1.48.0
Release:        1
Summary:        Bare libuv bindings for lua
Group:          Development/Other
License:        ASL 2.0
URL:            https://github.com/luvit/luv
Source0:        https://github.com/luvit/luv/releases/download/%{dlver}/luv-%{dlver}.tar.gz#/%{name}-%{dlver}.tar.gz

BuildRequires:  cmake
BuildRequires:  ninja
BuildRequires:  pkgconfig(libuv)

%if %{with lua}
BuildRequires:  pkgconfig(lua) >= 5.3
BuildRequires:  lua5.3
Requires:       lua5.3
%endif

%if %{with luajit}
BuildRequires:	pkgconfig(luajit)
BuildRequires:  luajit
Requires:	luajit
%endif

%description
libuv bindings for luajit and lua 5.1/5.2/5.3.

This library makes libuv available to lua scripts. It was made for the luvit
project but should usable from nearly any lua project.

%package -n %{libname}
Summary:	Version of libluv built for luajit
Provides:	luajit-luv = %{version}-%{release}
Provides:	libluv = %{EVRD}
%rename %{name}

%description -n %{libname}
Version of libluv built for luajit

%package -n %{lualibname}
Summary:	Version of libluv built for lua rather than luajit
Provides:	lua-luv = %{version}-%{release}

%description -n %{lualibname}
Version of libluv built for lua rather than luajit

%package -n %{devname}
Summary:        Bare libuv bindings for lua
Group:          Development/Other
%if %{with luajit}
Requires:       luajit-luv = %{version}-%{release}
%endif
%rename %{name}-devel

%description -n %{devname}
Development package for LUV.

libuv bindings for luajit and lua 5.1/5.2/5.3.

This library makes libuv available to lua scripts. It was made for the luvit
project but should usable from nearly any lua project.

%prep
%autosetup -n luv-%{dlver}
%if %{with luajit}
LDFLAGS="${LDFLAGS:- -Wl,--as-needed -Wl,-z,relro -Wl,-O1 -Wl,--build-id -Wl,--enable-new-dtags}" ; export LDFLAGS
%cmake -GNinja \
    -DBUILD_MODULE=OFF \
    -DBUILD_SHARED_LIBS=ON \
    -DWITH_LUA_ENGINE=LuaJIT \
    -DWITH_SHARED_LIBUV=ON \
    -DLUA_BUILD_TYPE=System \
    -DINSTALL_LIB_DIR=%{_libdir} \
	-DSHAREDLIBS_INSTALL_LIB_DIR=%{_libdir} \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    ..
cd ..
%endif

%if %{with lua}
export CMAKE_BUILD_DIR=build-lua
LDFLAGS="${LDFLAGS:- -Wl,--as-needed -Wl,-z,relro -Wl,-O1 -Wl,--build-id -Wl,--enable-new-dtags}" ; export LDFLAGS
%cmake -GNinja \
    -DBUILD_MODULE=OFF \
    -DBUILD_SHARED_LIBS=ON \
    -DWITH_LUA_ENGINE=Lua \
    -DWITH_SHARED_LIBUV=ON \
    -DLUA_BUILD_TYPE=System \
    -DINSTALL_LIB_DIR=%{_libdir} \
	-DSHAREDLIBS_INSTALL_LIB_DIR=%{_libdir} \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    ..
%endif

%build
%if %{with luajit}
%ninja_build -C build
%endif

%if %{with lua}
%ninja_build -C build-lua
%endif

%install
%if %{with lua}
%ninja_install -C build-lua
for i in %{buildroot}%{_libdir}/libluv.so*; do
	mv $i ${i/luv.so/luv-lua.so}
done
%endif

%if %{with luajit}
%ninja_install -C build
%endif

%if %{with luajit}
%files -n %{libname}
%{_libdir}/libluv.so.%{major}{,.*}
%endif

%if %{with lua}
%files -n %{lualibname}
%{_libdir}/libluv-lua.so*
%endif

%files -n %{devname}
%license LICENSE.txt
%doc README.md docs.md
%{_includedir}/luv
%if %{with luajit}
%{_libdir}/libluv.so
%endif
%{_libdir}/pkgconfig/libluv.pc
