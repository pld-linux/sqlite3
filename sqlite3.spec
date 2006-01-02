# TODO:
# - fix lib64 in tcl module
#
# Conditional build:
%bcond_without	tests # don't run tests
%bcond_without	tcl   # disable tcl extension
%bcond_without	docs  # disable documentation building
#
Summary:	SQLite library
Summary(pl):	Biblioteka SQLite
Name:		sqlite3
Version:	3.2.8
Release:	1
License:	LGPL
Group:		Libraries
# Source0Download: http://sqlite.org/download.html
Source0:	http://sqlite.org/sqlite-%{version}.tar.gz
# Source0-md5:	9f2c014aaa46565b8163e047166a5686
Patch0:		%{name}-test-conflict.patch
Patch1:		%{name}-sign-function.patch
URL:		http://sqlite.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	readline-devel
%{?with_tcl:BuildRequires:	tcl-devel}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%ifarch alpha %{x8664}
%undefine	with_tests
%endif

# disabling tcl currently breaks making test target,
# some hack in Makefile needs to be done
%if %{without tcl}
%undefine	with_tests
%endif

%define         _ulibdir        /usr/lib

%description
SQLite is a C library that implements an SQL database engine. A large
subset of SQL92 is supported. A complete database is stored in a
single disk file. The API is designed for convenience and ease of use.
Applications that link against SQLite can enjoy the power and
flexiblity of an SQL database without the administrative hassles of
supporting a separate database server. Because it omits the
client-server interaction overhead and writes directly to disk, SQLite
is also faster than the big database servers for most operations. In
addition to the C library, the SQLite distribution includes a
command-line tool for interacting with SQLite databases and SQLite
bindings for Tcl/Tk.

%description -l pl
SQLite jest bibliotek± jêzyka C, która implementuje silnik baz danych
SQL (obs³ugiwana jest wiêkszo¶æ standardu SQL92). Ca³a baza danych
przechowywana jest w jednym pliku. Aplikacje wykorzystuj±ce tê
bibliotekê charakteryzuj± siê si³± i elastyczno¶ci± SQLowych baz
danych bez konieczno¶ci utrzymywania osobnego serwera baz danych.
Poniewa¿ pomijana jest komunikacja klient-serwer i dane s± zapisywane
bezpo¶rednio na dysku, SQLite jest szybsza od du¿ych serwerów
bazodanowych przy wiêkszo¶ci operacji na bazie danych. Dodatkowo
oprócz biblioteki jêzyka C, dostarczany jest program do zarz±dzania
bazami danych.

%package devel
Summary:	Header files for SQLite development
Summary(pl):	Pliki nag³ówkowe SQLite
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
SQLite is a C library that implements an SQL database engine. A large
subset of SQL92 is supported. A complete database is stored in a
single disk file. The API is designed for convenience and ease of use.
Applications that link against SQLite can enjoy the power and
flexiblity of an SQL database without the administrative hassles of
supporting a separate database server. Because it omits the
client-server interaction overhead and writes directly to disk, SQLite
is also faster than the big database servers for most operations. In
addition to the C library, the SQLite distribution includes a
command-line tool for interacting with SQLite databases and SQLite
bindings for Tcl/Tk.

This package contains the header files needed to develop programs that
use these SQLite.

%description devel -l pl
SQLite jest bibliotek± jêzyka C, która implementuje silnik baz danych
SQL (obs³ugiwana jest wiêkszo¶æ standardu SQL92). Ca³a baza danych
przechowywana jest w jednym pliku. Aplikacje wykorzystuj±ce tê
bibliotekê charakteryzuj± siê si³± i elastyczno¶ci± SQLowych baz
danych bez konieczno¶ci utrzymywania osobnego serwera baz danych.
Poniewa¿ pomijana jest komunikacja klient-serwer i dane s± zapisywane
bezpo¶rednio na dysku, SQLite jest szybsza od du¿ych serwerów
bazodanowych przy wiêkszo¶ci operacji na bazie danych. Dodatkowo
oprócz biblioteki jêzyka C, dostarczany jest program do zarz±dzania
bazami danych.

Pakiet zawiera pliki nagówkowe niezbedne do kompilowania programów
u¿ywaj±cych biblioteki SQLite.

%package static
Summary:	Static libraries for SQLite development
Summary(pl):	Statyczne biblioteki SQLite
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
SQLite is a C library that implements an SQL database engine. A large
subset of SQL92 is supported. A complete database is stored in a
single disk file. The API is designed for convenience and ease of use.
Applications that link against SQLite can enjoy the power and
flexiblity of an SQL database without the administrative hassles of
supporting a separate database server. Because it omits the
client-server interaction overhead and writes directly to disk, SQLite
is also faster than the big database servers for most operations. In
addition to the C library, the SQLite distribution includes a
command-line tool for interacting with SQLite databases and SQLite
bindings for Tcl/Tk.

This package contains the static SQLite libraries.

%description static -l pl
SQLite jest bibliotek± jêzyka C, która implementuje silnik baz danych
SQL (obs³ugiwana jest wiêkszo¶æ standardu SQL92). Ca³a baza danych
przechowywana jest w jednym pliku. Aplikacje wykorzystuj±ce tê
bibliotekê charakteryzuj± siê si³± i elastyczno¶ci± SQLowych baz
danych bez konieczno¶ci utrzymywania osobnego serwera baz danych.
Poniewa¿ pomijana jest komunikacja klient-serwer i dane s± zapisywane
bezpo¶rednio na dysku, SQLite jest szybsza od du¿ych serwerów
bazodanowych przy wiêkszo¶ci operacji na bazie danych. Dodatkowo
oprócz biblioteki jêzyka C, dostarczany jest program do zarz±dzania
bazami danych.

Pakiet zawiera statyczne biblioteki SQLite.

%package -n tcl-%{name}
Summary:        sqlite3 tcl extension
Summary(pl):    Rozszerzenie sqlite3 dla Tcl
Group:          Development/Languages/Tcl

%description -n tcl-%{name}
sqlite3 tcl extension.

%description -l pl -n tcl-%{name}
Rozszerzenie sqlite3 dla Tcl.

%prep
%setup -q -n sqlite-%{version}
%patch0 -p1
%patch1 -p1
sed -i 's/mkdir doc/#mkdir doc/' Makefile*

%build
%{__libtoolize}
cp -f /usr/share/automake/config.sub .
%{__aclocal}
%{__autoconf}
%configure \
	%{?with_tcl:--with-tcl=%{_ulibdir}} \
	%{!?with_tcl:--disable-tcl} \
	--enable-threadsafe
%{__make}

%if %{with docs}
%{__make} doc
%endif

%{?with_tests:LC_ALL=C %{__make} test}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_includedir},%{_libdir},%{_mandir}/man1}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install sqlite3.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/sqlite3
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%{_mandir}/man1/sqlite3.1*

%files devel
%defattr(644,root,root,755)
%doc doc/*
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/sqlite3.h
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%if %{with tcl}
%files -n tcl-%{name}
%defattr(644,root,root,755)
%dir %{_ulibdir}/tcl*/sqlite3
%attr(755,root,root) %{_ulibdir}/tcl*/sqlite3/*.so
%{_ulibdir}/tcl*/sqlite3/*.tcl
%endif
