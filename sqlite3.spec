# TODO:
# - some tests fail with tcl8.5, it's tcl fault,
#	if someone REALLY cares (s)he can look into it
# - sqlite binary is linked statically with sqlite library
#
# Conditional build:
%bcond_with	tests		# run tests
%bcond_with	readline	# readline (GPL) instead of libedit
%bcond_without	tcl		# Tcl extension
%bcond_without	doc		# disable documentation building
%bcond_without	unlock_notify	# disable unlock notify API
%bcond_without	load_extension	# enable load extension API
%bcond_with	icu		# ICU tokenizer support
%bcond_without	json1		# json1 extension
%bcond_without	wal_replication		# WAL replication support

%ifarch %{x8664}
%undefine	with_tests
%endif

# disabling tcl currently breaks making test target,
# some hack in Makefile needs to be done
%if %{without tcl}
%undefine	with_tests
%endif

# sqlite3 version with zero padded without any dots (3 08 10 01 is 3.8.10.1)
# but trailing 00 means no 4rd part (3 11 01 00 is 3.11.1)
%define		vnum	3320300
%define		ver		%{lua:vn=rpm.expand("%vnum");v="";for i in string.gmatch(string.format("%08d", vn), "..") do v=v.."."..i:gsub("^0", "");end;v=v:gsub("^.",""):gsub("\.0$","");print(v)}

# wal replication version
%define		walver	3.32.1

%define		tclver		8.6
Summary:	SQLite3 library
Summary(pl.UTF-8):	Biblioteka SQLite3
Name:		sqlite3
Version:	%{ver}
Release:	1
License:	Public Domain
Group:		Libraries
# Source0Download: http://www.sqlite.org/download.html
Source0:	https://www.sqlite.org/2020/sqlite-src-%{vnum}.zip
# Source0-md5:	7c56e491de5ec630def428fae3a13bb4
Patch0:		%{name}-sign-function.patch
# https://github.com/CanonicalLtd/dqlite/issues/91
Patch1:		https://github.com/CanonicalLtd/sqlite/releases/download/version-%{walver}+replication4/sqlite-%{walver}.diff
# Patch1-md5:	17ff8c8e6952445accffbf7fb51d1664
URL:		https://www.sqlite.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
%{!?with_readline:BuildRequires:	libedit-devel}
BuildRequires:	libtool
%{?with_readline:BuildRequires:	readline-devel}
%{?with_load_extension:BuildRequires:	sed >= 4.0}
BuildRequires:	tcl
%{?with_tcl:BuildRequires:	tcl-devel >= %{tclver}}
BuildRequires:	unzip
Requires:	%{name}-libs = %{version}-%{release}
%{?with_icu:Provides:	%{name}(icu) = %{version}}
%{?with_load_extension:Provides:	%{name}(load_extension) = %{version}}
%{?with_unlock_notify:Provides:	%{name}(unlock_notify) = %{version}}
%{?with_wal_replication:Provides:	%{name}(wal_replication) = %{version}}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_ulibdir	/usr/lib

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

%package libs
Summary:	Shared library for the sqlite3 embeddable SQL database engine
Summary(pl.UTF-8):	Biblioteka współdzielona osadzalnego silnika baz danych SQL sqlite3
Group:		Libraries
%{?with_icu:Provides:	%{name}-libs(icu) = %{version}}
%{?with_load_extension:Provides:	%{name}-libs(load_extension) = %{version}}
%{?with_unlock_notify:Provides:	%{name}-libs(unlock_notify) = %{version}}
%{?with_wal_replication:Provides:	%{name}-libs(wal_replication) = %{version}}
Conflicts:	sqlite3 < 3.23.1-2

%description libs
This package contains the SQLite 3 shared library.

%description libs -l pl.UTF-8
Ten pakiet zawiera bibliotekę współdzieloną SQLite 3.

%package devel
Summary:	Header files for SQLite development
Summary(pl.UTF-8):	Pliki nagłówkowe SQLite
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
%if %{with unlock_notify}
Provides:	%{name}-devel(unlock_notify) = %{version}
%endif
%if %{with load_extension}
Provides:	%{name}-devel(load_extension) = %{version}
%endif
%if %{with icu}
Provides:	%{name}-devel(icu) = %{version}
%endif
%{?with_wal_replication:Provides:	%{name}-devel(wal_replication) = %{version}}

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
%if %{with unclock_notify}
Provides:	%{name}-static(unlock_notify)
%endif
%if %{with load_extension}
Provides:	%{name}-static(load_extension)
%endif
%{?with_wal_replication:Provides:	%{name}-static(wal_replication)}

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
%setup -q -n sqlite-src-%{vnum}
%patch0 -p1
%{?with_wal_replication:%patch1 -p1}

%{__sed} -i 's/mkdir doc/#mkdir doc/' Makefile.in

if [ "$(cat VERSION)" != "%{version}" ]; then
	echo "Tarball content doesn't match version %{version}." >&2
	exit 1
fi

%build
%{__libtoolize}
cp -f /usr/share/automake/config.sub .
%{__aclocal}
%{__autoconf} --force
append-cppflags() {
	CPPFLAGS="$CPPFLAGS $*"
}
append-libs() {
	LIBS="$LIBS $*"
}
export CPPFLAGS="%{rpmcflags}"
export LIBS
%if %{with tcl}
export TCLLIBDIR="%{tcl_sitearch}/sqlite3"
%endif

append-cppflags -DSQLITE_DISABLE_DIRSYNC=1 -DSQLITE_SECURE_DELETE

# Support for optional ORDER BY and LIMIT clause on UPDATE and DELETE statements
append-cppflags -DSQLITE_ENABLE_UPDATE_DELETE_LIMIT

# Support column metadata functions.
# http://sqlite.org/c3ref/column_database_name.html
# http://sqlite.org/c3ref/table_column_metadata.html
append-cppflags -DSQLITE_ENABLE_COLUMN_METADATA

# Support Full-Text Search versions 3 and 4.
# http://sqlite.org/fts3.html
#append-cppflags -DSQLITE_ENABLE_FTS3 -DSQLITE_ENABLE_FTS3_PARENTHESIS -DSQLITE_ENABLE_FTS4 -DSQLITE_ENABLE_FTS4_UNICODE61
append-cppflags -DSQLITE_ENABLE_FTS3 -DSQLITE_ENABLE_FTS3_PARENTHESIS
append-cppflags -DSQLITE_ENABLE_FTS3_TOKENIZER

# Support R*Trees.
# http://sqlite.org/rtree.html
append-cppflags -DSQLITE_ENABLE_RTREE

# Support Geopoly module (new as of 3.25.0)
# https://www.sqlite.org/geopoly.html
append-cppflags -DSQLITE_ENABLE_GEOPOLY

# Support soundex() function.
# http://sqlite.org/lang_corefunc.html#soundex
#append-cppflags -DSQLITE_SOUNDEX

# Support dbstat virtual table.
# https://www.sqlite.org/dbstat.html
append-cppflags -DSQLITE_ENABLE_DBSTAT_VTAB

# Support for session extension (record changes to a changeset).
# https://www.sqlite.org/sessionintro.html
append-cppflags -DSQLITE_ENABLE_SESSION -DSQLITE_ENABLE_PREUPDATE_HOOK

%if %{with unlock_notify}
# Support unlock notification.
# http://sqlite.org/unlock_notify.html
append-cppflags -DSQLITE_ENABLE_UNLOCK_NOTIFY
%endif

%if %{with icu}
append-cppflags -DSQLITE_ENABLE_ICU
append-libs "-licui18n -licuuc"
%endif

%if %{with load_extension}
append-libs "-ldl"
%endif

%if %{with wal_replication}
# A patched version of SQLite with support for WAL-based replication
append-cppflags -DSQLITE_ENABLE_WAL_REPLICATION
%endif

%configure \
	%{?with_readline:--disable-editline} \
	%{!?with_tcl:--disable-tcl}%{?with_tcl:--with-tcl=%{_ulibdir}} \
	%{__enable_disable load_extension load-extension} \
	%{__enable_disable json1} \
	--enable-threadsafe \
	--enable-fts5

%{__make}

%if %{with doc}
%{__make} doc
%endif

%{?with_tests:LC_ALL=C %{__make} test}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/%{_lib},%{_bindir},%{_includedir},%{_libdir},%{_mandir}/man1}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__mv} $RPM_BUILD_ROOT%{_libdir}/lib*.so.* $RPM_BUILD_ROOT/%{_lib}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.so
ln -sf /%{_lib}/$(cd $RPM_BUILD_ROOT/%{_lib}; echo lib*.so.*.*) \
	$RPM_BUILD_ROOT%{_libdir}/libsqlite3.so

cp -p sqlite3.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libsqlite3.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libsqlite3.so.0

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/sqlite3
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
