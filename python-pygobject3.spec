#
# Conditional build:
%bcond_without	python2		# Python 2.x module
%bcond_without	python3		# Python 3.x module

%define		module	pygobject
Summary:	Python bindings for GObject library
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki GObject
Name:		python-%{module}3
Version:	3.4.2
Release:	1
License:	LGPL v2+
Group:		Libraries/Python
Source0:	http://ftp.gnome.org/pub/GNOME/sources/pygobject/3.4/%{module}-%{version}.tar.xz
# Source0-md5:	a17b3897507f179d643e02f5abf111ac
URL:		http://www.pygtk.org/
Patch0:		link.patch
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake >= 1:1.11
BuildRequires:	glib2-devel >= 1:2.34.0
BuildRequires:	gobject-introspection-devel >= 1.34.1.1
BuildRequires:	libffi-devel >= 3.0
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(libffi) >= 3.0
BuildRequires:	rpm-pythonprov
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%if %{with python2}
BuildRequires:	python-devel >= 1:2.6
BuildRequires:	python-pycairo-devel >= 1.2.0
%pyrequires_eq	python-modules
%endif
%if %{with python3}
BuildRequires:	python3 >= 3.2.2-3
BuildRequires:	python3-devel >= 3.2.2-3
BuildRequires:	python3-modules >= 3.2.2-3
BuildRequires:	python3-pycairo-devel >= 1.10.0
%endif
Requires:	glib2 >= 1:2.34.0
Requires:	gobject-introspection >= 1.34.1.1
Conflicts:	python-pygobject < 2.28.6-3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python bindings for GObject library.

%description -l pl.UTF-8
Wiązania Pythona do biblioteki GObject.

%package common-devel
Summary:	Python bindings for GObject library
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki GObject
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.34.0
Requires:	libffi-devel >= 3.0

%description common-devel
This package contains headers files required to build wrappers for
GObject addon libraries so that they interoperate with Python
bindings.

%description common-devel -l pl.UTF-8
Pakiet zawiera pliki nagłówkowe wymagane do zbudowania funkcji do
biblioteki GObject, tak by mogły te biblioteki kooperowaći z
wiązaniami Pythona.

%package devel
Summary:	Python bindings for GObject library
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki GObject
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-common-devel = %{version}-%{release}
Requires:	glib2-devel >= 1:2.34.0
Requires:	libffi-devel >= 3.0
Requires:	python-devel >= 1:2.6

%description devel
This package contains files required to build wrappers for GObject
addon libraries so that they interoperate with Python bindings.

%description devel -l pl.UTF-8
Pakiet zawiera pliki wymagane do zbudowania funkcji do biblioteki
GObject, tak by mogły te biblioteki kooperować z wiązaniami Pythona.

%package -n python3-pygobject3
Summary:	Python 3.x bindings for GObject library
Summary(pl.UTF-8):	Wiązania Pythona 3.x do biblioteki GObject
Group:		Libraries/Python
Requires:	glib2 >= 1:2.34.0
Requires:	gobject-introspection >= 1.34.1.1
Conflicts:	python3-pygobject < 2.28.6-3

%description -n python3-pygobject3
Python 3.x bindings for GObject library.

%description -n python3-pygobject3 -l pl.UTF-8
Wiązania Pythona 3.x do biblioteki GObject.

%package -n python3-pygobject3-devel
Summary:	Python bindings for GObject library
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki GObject
Group:		Development/Languages/Python
Requires:	%{name}-common-devel = %{version}-%{release}
Requires:	glib2-devel >= 1:2.34.0
Requires:	libffi-devel >= 3.0
Requires:	python3-devel >= 3.1
Requires:	python3-pygobject3 = %{version}-%{release}

%description -n python3-pygobject3-devel
This package contains files required to build wrappers for GObject
addon libraries so that they interoperate with Python bindings.

%description -n python3-pygobject3-devel -l pl.UTF-8
Pakiet zawiera pliki wymagane do zbudowania funkcji do biblioteki
GObject, tak by mogły te biblioteki kooperować z wiązaniami Pythona.

%package examples
Summary:	Example programs for GObject library
Summary(pl.UTF-8):	Programy przykładowe dla biblioteki GObject
Group:		Development/Languages/Python
Requires:	%{name}-devel = %{version}-%{release}

%description examples
This package contains example programs for GObject library.

%description examples -l pl.UTF-8
Ten pakiet zawiera przykładowe programy dla biblioteki GObject.

%package apidocs
Summary:	pygobject API documentation
Summary(pl.UTF-8):	Dokumentacja API pygobject
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
pygobject API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API pygobject.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%if %{with python3}
mkdir py3
cd py3
../%configure \
	PYTHON=/usr/bin/python3 \
	PYTHON_LIBS=-lpython3 \
	--disable-silent-rules
%{__make}
cd ..
%endif
%if %{with python2}
mkdir py2
cd py2
../%configure \
	PYTHON=%{__python} \
	PYTHON_LIBS=-lpython \
	--disable-silent-rules
%{__make}
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%if %{with python3}
%{__make} -C py3 -j 1 install \
	DESTDIR=$RPM_BUILD_ROOT \
	TARGET_DIR=%{_gtkdocdir}/%{module}
%endif
%if %{with python2}
%{__make} -C py2 -j 1 install \
	DESTDIR=$RPM_BUILD_ROOT \
	TARGET_DIR=%{_gtkdocdir}/%{module}
%endif

cp -a examples/*.py $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%if %{with python2}
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/gi/{*/,}/*.la
%py_postclean
%endif
%if %{with python3}
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/gi/{*/,}*.la
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post	-n python3-pygobject3 -p /sbin/ldconfig
%postun	-n python3-pygobject3 -p /sbin/ldconfig

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/libpyglib-gi-2.0-python.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpyglib-gi-2.0-python.so.0
%dir %{py_sitedir}/gi
%dir %{py_sitedir}/gi/overrides
%{py_sitedir}/gi/overrides/*.py[co]
%dir %{py_sitedir}/gi/repository
%{py_sitedir}/gi/repository/*.py[co]
%{py_sitedir}/gi/*.py[co]
%attr(755,root,root) %{py_sitedir}/gi/_gi.so
%attr(755,root,root) %{py_sitedir}/gi/_gi_cairo.so
%dir %{py_sitedir}/gi/_glib
%attr(755,root,root) %{py_sitedir}/gi/_glib/_glib.so
%{py_sitedir}/gi/_glib/*.py[co]
%dir %{py_sitedir}/gi/_gobject
%attr(755,root,root) %{py_sitedir}/gi/_gobject/_gobject.so
%{py_sitedir}/gi/_gobject/*.py[co]
%{py_sitedir}/pygobject-%{version}-py*.egg-info

%files common-devel
%defattr(644,root,root,755)
%{_includedir}/pygobject-3.0
%{_pkgconfigdir}/pygobject-3.0.pc

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpyglib-gi-2.0-python.so
%endif

%if %{with python3}
%files -n python3-pygobject3
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/libpyglib-gi-2.0-python3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpyglib-gi-2.0-python3.so.0
%dir %{py3_sitedir}/gi
%dir %{py3_sitedir}/gi/overrides
%{py3_sitedir}/gi/overrides/*.py*
#%{py3_sitedir}/gi/overrides/__pycache__
%dir %{py3_sitedir}/gi/repository
%{py3_sitedir}/gi/repository/*.py*
#%{py3_sitedir}/gi/repository/__pycache__
%{py3_sitedir}/gi/*.py*
#%{py3_sitedir}/gi/__pycache__
%attr(755,root,root) %{py3_sitedir}/gi/_gi.*so
%attr(755,root,root) %{py3_sitedir}/gi/_gi_cairo.*so
%dir %{py3_sitedir}/gi/_glib
%attr(755,root,root) %{py3_sitedir}/gi/_glib/_glib.*so
%{py3_sitedir}/gi/_glib/*.py*
#%{py3_sitedir}/glib/__pycache__
%dir %{py3_sitedir}/gi/_gobject
%attr(755,root,root) %{py3_sitedir}/gi/_gobject/_gobject.*so
%{py3_sitedir}/gi/_gobject/*.py*
#%{py3_sitedir}/gobject/__pycache__
%{py3_sitedir}/pygobject-%{version}-py*.egg-info

%files -n python3-pygobject3-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpyglib-gi-2.0-python3.so
%endif

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}

#%files apidocs
#%defattr(644,root,root,755)
#%{_gtkdocdir}/%{module}
