# TODO:
# - some tests fail with tcl8.5, it's tcl fault,
#	if someone REALLY cares (s)he can look into it
# - alpha build fail:
#   tclsh ./tool/mksqlite3c.tcl
#   tclsh: allocatestack.c:404: allocate_stack: Assertion `size != 0' failed.
#   make: *** [sqlite3.c] Aborted
#
# Conditional build:
%bcond_with	tests	# run tests
%bcond_without	tcl	# disable tcl extension
%bcond_without	doc	# disable documentation building
#
%ifarch alpha sparc %{x8664}
%undefine	with_tests
%endif

# disabling tcl currently breaks making test target,
# some hack in Makefile needs to be done
%if !%{with tcl}
%undefine	with_tests
%endif

%define		_ulibdir	/usr/lib
%define		tclver		8.5

Summary:	SQLite library
Summary(pl.UTF-8):	Biblioteka SQLite
Name:		sqlite3
Version:	3.6.1
Release:	1
License:	LGPL
Group:		Libraries
# Source0Download: http://www.sqlite.org/download.html
Source0:	http://www.sqlite.org/sqlite-%{version}.tar.gz
# Source0-md5:	eeef61635d89710bb8d976c2a0b99841
Patch0:		%{name}-sign-function.patch
Patch1:		%{name}-pkgconfig.patch
URL:		http://www.sqlite.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	readline-devel
%{?with_tcl:BuildRequires:	tcl-devel}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%description -l pl.UTF-8
SQLite jest biblioteką języka C, która implementuje silnik baz danych
SQL (obsługiwana jest większość standardu SQL92). Cała baza danych
przechowywana jest w jednym pliku. Aplikacje wykorzystujące tę
bibliotekę charakteryzują się siłą i elastycznością SQLowych baz
danych bez konieczności utrzymywania osobnego serwera baz danych.
Ponieważ pomijana jest komunikacja klient-serwer i dane są zapisywane
bezpośrednio na dysku, SQLite jest szybsza od dużych serwerów
bazodanowych przy większości operacji na bazie danych. Dodatkowo
oprócz biblioteki języka C, dostarczany jest program do zarządzania
bazami danych.

%package devel
Summary:	Header files for SQLite development
Summary(pl.UTF-8):	Pliki nagłówkowe SQLite
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

%description devel -l pl.UTF-8
SQLite jest biblioteką języka C, która implementuje silnik baz danych
SQL (obsługiwana jest większość standardu SQL92). Cała baza danych
przechowywana jest w jednym pliku. Aplikacje wykorzystujące tę
bibliotekę charakteryzują się siłą i elastycznością SQLowych baz
danych bez konieczności utrzymywania osobnego serwera baz danych.
Ponieważ pomijana jest komunikacja klient-serwer i dane są zapisywane
bezpośrednio na dysku, SQLite jest szybsza od dużych serwerów
bazodanowych przy większości operacji na bazie danych. Dodatkowo
oprócz biblioteki języka C, dostarczany jest program do zarządzania
bazami danych.

Pakiet zawiera pliki nagówkowe niezbedne do kompilowania programów
używających biblioteki SQLite.

%package static
Summary:	Static libraries for SQLite development
Summary(pl.UTF-8):	Statyczne biblioteki SQLite
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

%description static -l pl.UTF-8
SQLite jest biblioteką języka C, która implementuje silnik baz danych
SQL (obsługiwana jest większość standardu SQL92). Cała baza danych
przechowywana jest w jednym pliku. Aplikacje wykorzystujące tę
bibliotekę charakteryzują się siłą i elastycznością SQLowych baz
danych bez konieczności utrzymywania osobnego serwera baz danych.
Ponieważ pomijana jest komunikacja klient-serwer i dane są zapisywane
bezpośrednio na dysku, SQLite jest szybsza od dużych serwerów
bazodanowych przy większości operacji na bazie danych. Dodatkowo
oprócz biblioteki języka C, dostarczany jest program do zarządzania
bazami danych.

Pakiet zawiera statyczne biblioteki SQLite.

%package -n tcl-%{name}
Summary:	sqlite3 tcl extension
Summary(pl.UTF-8):	Rozszerzenie sqlite3 dla Tcl
Group:		Development/Languages/Tcl

%description -n tcl-%{name}
sqlite3 tcl extension.

%description -n tcl-%{name} -l pl.UTF-8
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
CFLAGS="%{rpmcflags} -DSQLITE_ENABLE_COLUMN_METADATA=1"
export CFLAGS
%configure \
	%{?with_tcl:--with-tcl=%{_ulibdir}} \
	%{!?with_tcl:--disable-tcl} \
	--enable-threadsafe
%{__make}

%if %{with doc}
%{__make} doc
%endif

%{?with_tests:LC_ALL=C %{__make} test}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_includedir},%{_libdir},%{_mandir}/man1}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	TCLLIBDIR=%{_libdir}/tcl%{tclver}

%if %{with tcl}
sed -i -e "s#$RPM_BUILD_ROOT##g" $RPM_BUILD_ROOT%{_libdir}/tcl%{tclver}/sqlite3/pkgIndex.tcl
%endif

install sqlite3.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/sqlite3
%attr(755,root,root) %{_libdir}/libsqlite3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsqlite3.so.0
%{_mandir}/man1/sqlite3.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsqlite3.so
%{_libdir}/libsqlite3.la
%{_includedir}/sqlite3.h
%{_includedir}/sqlite3ext.h
%{_pkgconfigdir}/sqlite3.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libsqlite3.a

%if %{with tcl}
%files -n tcl-%{name}
%defattr(644,root,root,755)
%dir %{_libdir}/tcl*/sqlite3
%attr(755,root,root) %{_libdir}/tcl%{tclver}/sqlite3/libtclsqlite3.so
%{_libdir}/tcl%{tclver}/sqlite3/pkgIndex.tcl
%endif
