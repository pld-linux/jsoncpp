#
# Conditional build:
%bcond_without	apidocs		# doxygen apidocs build
%bcond_without	static_libs	# static library
%bcond_without	tests		# tests during build

Summary:	API for manipulating JSON
Summary(pl.UTF-8):	API do operacji na strukturach JSON
Name:		jsoncpp
Version:	1.9.5
Release:	3
License:	MIT or Public Domain
Group:		Libraries
#Source0Download: https://github.com/open-source-parsers/jsoncpp/releases
Source0:	https://github.com/open-source-parsers/jsoncpp/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	d6c8c609f2162eff373db62b90a051c7
Patch0:		%{name}-cmake-prefer-shared.patch
URL:		https://github.com/open-source-parsers/jsoncpp/
BuildRequires:	cmake >= 3.8.0
BuildRequires:	libstdc++-devel >= 6:4.8.1
BuildRequires:	python3
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.605
%if %{with apidocs}
BuildRequires:	doxygen
BuildRequires:	graphviz
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
JSONCPP provides a simple API to manipulate JSON values, and handle
serialization and unserialization to strings.

%description -l pl.UTF-8
JSONCPP udostępnia proste API do operacji na wartościach JSON oraz
obsługi serializacji oraz deserializacji z łańcuchów znaków.

%package devel
Summary:	Header files for JSONCPP library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki JSONCPP
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for JSONCPP library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki JSONCPP.

%package static
Summary:	Static JSONCPP library
Summary(pl.UTF-8):	Statyczna biblioteka JSONCPP
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static JSONCPP library.

%description static -l pl.UTF-8
Statyczna biblioteka JSONCPP.

%package apidocs
Summary:	API documentation for JSONCPP library
Summary(pl.UTF-8):	Dokumentacja API biblioteki JSONCPP
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for JSONCPP library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki JSONCPP.

%prep
%setup -q
%patch0 -p1

%build
install -d build
cd build
%cmake .. \
	-DBUILD_OBJECT_LIBS=OFF \
	%{!?with_static_libs:-DBUILD_STATIC_LIBS=OFF} \
	-DCMAKE_INSTALL_INCLUDEDIR:PATH=%{_includedir}/%{name} \
	-DJSONCPP_WITH_CMAKE_PACKAGE=ON \
	%{!?with_tests:-DJSONCPP_WITH_TESTS=OFF} \
	-DSTATIC_SUFFIX=
cd ..
%{__make} -C build

%if %{with apidocs}
ln -sf build/version .
%{__python3} doxybuild.py \
	--dot=/usr/bin/dot \
	--doxygen=/usr/bin/doxygen
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE README.md
%attr(755,root,root) %{_libdir}/libjsoncpp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libjsoncpp.so.25

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libjsoncpp.so
%{_includedir}/jsoncpp
%{_pkgconfigdir}/jsoncpp.pc
%{_libdir}/cmake/jsoncpp

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libjsoncpp.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc dist/doxygen/jsoncpp-api-html-*/*
%endif
