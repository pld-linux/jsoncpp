#
# Conditional build:
%bcond_without	apidocs	# doxygen apidocs build
%bcond_without	tests	# tests during build

Summary:	API for manipulating JSON
Summary(pl.UTF-8):	API do operacji na strukturach JSON
Name:		jsoncpp
Version:	1.6.2
Release:	2
License:	MIT or Public Domain
Group:		Libraries
Source0:	https://github.com/open-source-parsers/jsoncpp/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	5a62da8b5c5b0e46a0e782e7363aee3d
URL:		https://github.com/open-source-parsers/jsoncpp/
BuildRequires:	cmake >= 2.8.5
BuildRequires:	libstdc++-devel
BuildRequires:	python >= 2
%if %{with apidocs}
BuildRequires:	doxygen
BuildRequires:	graphviz
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
JSONCPP provides a simple API to manipulate JSON values, and handle
serialization and unserialization to strings.

%description
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

%description apidocs
API documentation for JSONCPP library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki JSONCPP.

%prep
%setup -q

%build
install -d build
cd build
%cmake .. \
	-DINCLUDE_INSTALL_DIR:PATH=%{_includedir}/%{name} \
	-DARCHIVE_INSTALL_DIR:PATH=%{_lib} \
	-DLIBRARY_INSTALL_DIR:PATH=%{_lib} \
	-DPACKAGE_INSTALL_DIR:PATH=%{_lib}/cmake \
	-DJSONCPP_LIB_BUILD_SHARED=ON \
	-DJSONCPP_WITH_CMAKE_PACKAGE=ON \
	%{!?with_tests:-DJSONCPP_WITH_TESTS=OFF}
cd ..

%if %{with apidocs}
%{__python} doxybuild.py \
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
%doc AUTHORS LICENSE NEWS.txt README.md
%attr(755,root,root) %{_libdir}/libjsoncpp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libjsoncpp.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libjsoncpp.so
%{_includedir}/jsoncpp
%{_pkgconfigdir}/jsoncpp.pc
%{_libdir}/cmake/jsoncpp

%files static
%defattr(644,root,root,755)
%{_libdir}/libjsoncpp.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc dist/doxygen/jsoncpp-api-html-*/*
%endif
