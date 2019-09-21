%define         major 1
%define         devel %mklibname %{name} %{major} -d

%define         dlver 1.30.1-1
%define         ver %(echo %{dlver} | tr - .)
%define         with_lua 1

Name:           libluv
Version:        1.30.1
Release:        1
Summary:        Bare libuv bindings for lua
Group:          Development/Other
License:        ASL 2.0
URL:            https://github.com/luvit/luv
Source0:        https://github.com/luvit/luv/releases/download/%{dlver}/luv-%{dlver}.tar.gz#/%{name}-%{version}.tar.gz
# Missing in tarball, so download manually
Source1:        https://github.com/luvit/luv/raw/master/libluv.pc.in

BuildRequires:  cmake
BuildRequires:  ninja
BuildRequires:  pkgconfig(lua) >= 5.3
BuildRequires:  pkgconfig(libuv)
%if %{with_lua}
BuildRequires:  lua5.3
%endif
BuildRequires:  luajit
Requires:       lua5.3

%description
libuv bindings for luajit and lua 5.1/5.2/5.3.

This library makes libuv available to lua scripts. It was made for the luvit
project but should usable from nearly any lua project.

%package devel
Summary:        Bare libuv bindings for lua
Group:          Development/Other
Requires:       lua-luv = %{version}-%{release}

%description devel
Development package for LUV.

libuv bindings for luajit and lua 5.1/5.2/5.3.

This library makes libuv available to lua scripts. It was made for the luvit
project but should usable from nearly any lua project.

%prep
%autosetup -n luv-%{dlver}
%__cp %{S:1} .

%build
LDFLAGS="${LDFLAGS:- -Wl,--as-needed -Wl,-z,relro -Wl,-O1 -Wl,--build-id -Wl,--enable-new-dtags}" ; export LDFLAGS
%cmake -GNinja \
    -DBUILD_MODULE=OFF \
    -DBUILD_SHARED_LIBS=ON \
%if %{with_lua}
    -DWITH_LUA_ENGINE=Lua \
%endif
    -DWITH_SHARED_LIBUV=ON \
    -DLUA_BUILD_TYPE=System \
    -DINSTALL_LIB_DIR=%{_libdir} \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    ${LDFLAGS} \
    ..

%ninja_build

%install
%ninja_install -C build

%files
%{_libdir}/libluv.so.%{major}{,.*}

%files devel
%license LICENSE.txt
%doc README.md docs.md
%{_includedir}/luv/
%{_libdir}/libluv.so
%{_libdir}/pkgconfig/libluv.pc
