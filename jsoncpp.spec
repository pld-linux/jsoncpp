#
# Conditional build:
%bcond_without	tests		# build without tests

%define	svnrev  251
%define	svndate 20120626
Summary:	API for manipulating JSON
Name:		jsoncpp
Version:	0.6.0
Release:	0.%{svndate}svn%{svnrev}.1
License:	MIT or Public Domain
Group:		Libraries
URL:		http://jsoncpp.sourceforge.net/
# Need to use svn.
# svn export https://jsoncpp.svn.sourceforge.net/svnroot/jsoncpp/trunk/jsoncpp jsoncpp
# tar cfj jsoncpp-20120626svn249.tar.bz2 jsoncpp
Source0:	%{name}-%{svndate}svn%{svnrev}.tar.bz2
# Source0-md5:	cc7964a0787959111ef3d9965287dd3e
Source1:	%{name}.pc
Patch0:		%{name}-optflags.patch
BuildRequires:	scons
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
JSONCPP provides a simple API to manipulate JSON values, and handle
serialization and unserialization to strings.

%package devel
Summary:	Headers	and libraries for JSONCPP
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Headers and libraries for JSONCPP.

%prep
%setup -q -n %{name}
%patch0 -p1
%{__sed} -i -e '
	s|g++|%{__cxx}| # FIXME: still does not work
	s|@@OPTFLAGS@@|%{rpmcxxflags}|
' SConstruct

%build
%scons \
	platform=linux-gcc

# Now, lets make a proper shared lib. :P
%{__cxx} -o libjsoncpp.so.0.0.0 -shared -Wl,-soname,libjsoncpp.so.0 buildscons/linux-gcc-*/src/lib_json/*.os -lpthread %{rpmldflags}

%if %{with tests}
scons platform=linux-gcc check
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

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS.txt README.txt version
%attr(755,root,root) %{_libdir}/libjsoncpp.so.0.0.0
%ghost %{_libdir}/libjsoncpp.so.0

%files devel
%defattr(644,root,root,755)
%doc doc/*
%{_includedir}/jsoncpp
%{_libdir}/libjsoncpp.so
%{_pkgconfigdir}/jsoncpp.pc
