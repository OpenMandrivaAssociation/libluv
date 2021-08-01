%define         major 1
%define         devel %mklibname %{name} %{major} -d

%define         dlver %{version}-0
%define         ver %(echo %{dlver} | tr - .)

%define		libname %mklibname luv %{major}
%define		devname %mklibname -d luv
%define		lualibname %mklibname -d luv-lua

Name:           libluv
Version:        1.41.1
Release:        1
Summary:        Bare libuv bindings for lua
Group:          Development/Other
License:        ASL 2.0
URL:            https://github.com/luvit/luv
Source0:        https://github.com/luvit/luv/releases/download/%{dlver}/luv-%{dlver}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  ninja
BuildRequires:  pkgconfig(libuv)

BuildRequires:  pkgconfig(lua) >= 5.3
BuildRequires:  lua5.3
Requires:       lua5.3

BuildRequires:	pkgconfig(luajit)
BuildRequires:  luajit
Requires:	luajit

%description
libuv bindings for luajit and lua 5.1/5.2/5.3.

This library makes libuv available to lua scripts. It was made for the luvit
project but should usable from nearly any lua project.

%package -n %{libname}
Summary:	Version of libluv built for luajit
Provides:	luajit-luv = %{version}-%{release}
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
Requires:       luajit-luv = %{version}-%{release}
%rename %{name}-devel

%description -n %{devname}
Development package for LUV.

libuv bindings for luajit and lua 5.1/5.2/5.3.

This library makes libuv available to lua scripts. It was made for the luvit
project but should usable from nearly any lua project.

%prep
%autosetup -n luv-%{dlver}
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
    ${LDFLAGS} \
    ..
cd ..

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
    ${LDFLAGS} \
    ..

%build
%ninja_build -C build

%ninja_build -C build-lua

%install
%ninja_install -C build-lua
for i in %{buildroot}%{_libdir}/libluv.so*; do
	mv $i ${i/luv.so/luv-lua.so}
done

%ninja_install -C build

%files -n %{libname}
%{_libdir}/libluv.so.%{major}{,.*}

%files -n %{lualibname}
%{_libdir}/libluv-lua.so*

%files -n %{devname}
%license LICENSE.txt
%doc README.md docs.md
%{_includedir}/luv
%{_libdir}/libluv.so
%{_libdir}/pkgconfig/libluv.pc
