#
# Conditional build:
%bcond_without	apidocs	# doxygen apidocs build
%bcond_without	tests	# "scons check" run

%define	svnrev  275
%define	svndate 20131207
Summary:	API for manipulating JSON
Summary(pl.UTF-8):	API do operacji na strukturach JSON
Name:		jsoncpp
Version:	0.6.0
Release:	0.%{svndate}svn%{svnrev}.1
License:	MIT or Public Domain
Group:		Libraries
# Need to use svn.
# svn export https://jsoncpp.svn.sourceforge.net/svnroot/jsoncpp/trunk/jsoncpp jsoncpp
# tar cfj jsoncpp-20120626svn249.tar.bz2 jsoncpp
Source0:	%{name}-%{svndate}svn%{svnrev}.tar.bz2
# Source0-md5:	82a3375d3aa03474c2aad13dc8d48648
Source1:	%{name}.pc
Patch0:		%{name}-optflags.patch
URL:		http://jsoncpp.sourceforge.net/
BuildRequires:	libstdc++-devel
BuildRequires:	python >= 2
BuildRequires:	scons
BuildRequires:	sed >= 4.0
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

%package apidocs
Summary:	API documentation for JSONCPP library
Summary(pl.UTF-8):	Dokumentacja API biblioteki JSONCPP
Group:		Documentation

%description apidocs
API documentation for JSONCPP library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki JSONCPP.

%prep
%setup -q -n %{name}
%patch0 -p1
%{__sed} -i -e '
	s|g++|%{__cxx}| # FIXME: still does not work
	s|@@OPTFLAGS@@|%{rpmcxxflags} -fno-inline-small-functions|
' SConstruct

%build
%scons \
	platform=linux-gcc

# Now, lets make a proper shared lib. :P
%{__cxx} -o libjsoncpp.so.0.0.0 -shared -Wl,-soname,libjsoncpp.so.0 buildscons/linux-gcc-*/src/lib_json/*.os -lpthread %{rpmldflags}

%if %{with tests}
scons platform=linux-gcc check
%endif

%if %{with apidocs}
%{__python} doxybuild.py \
	--dot=/usr/bin/dot \
	--doxygen=/usr/bin/doxygen
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}/jsoncpp,%{_pkgconfigdir}}
install -p libjsoncpp.so.*.*.* $RPM_BUILD_ROOT%{_libdir}
cp -a include/json $RPM_BUILD_ROOT%{_includedir}/jsoncpp
%{__sed} -e 's|@@LIBDIR@@|%{_libdir}|g' %{SOURCE1} > $RPM_BUILD_ROOT%{_pkgconfigdir}/jsoncpp.pc

/sbin/ldconfig -n $RPM_BUILD_ROOT%{_libdir}
ln -s $(basename $RPM_BUILD_ROOT%{_libdir}/libjsoncpp.so.*.*.*) $RPM_BUILD_ROOT%{_libdir}/libjsoncpp.so

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE NEWS.txt README.txt
%attr(755,root,root) %{_libdir}/libjsoncpp.so.0.0.0
%attr(755,root,root) %ghost %{_libdir}/libjsoncpp.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libjsoncpp.so
%{_includedir}/jsoncpp
%{_pkgconfigdir}/jsoncpp.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc dist/doxygen/jsoncpp-api-html-*/*
%endif
