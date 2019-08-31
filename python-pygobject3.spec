#
# Conditional build:
%bcond_without	python2		# Python 2.x module
%bcond_without	python3		# Python 3.x module
%bcond_without	doc		# Sphinx documentation
%bcond_with	tests		# unit tests (fail at the beginning as of 3.30.1)

%define		module	pygobject
Summary:	Python bindings for GObject library
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki GObject
Name:		python-pygobject3
Version:	3.32.2
Release:	1
License:	LGPL v2+
Group:		Libraries/Python
Source0:	http://ftp.gnome.org/pub/GNOME/sources/pygobject/3.32/%{module}-%{version}.tar.xz
# Source0-md5:	92ffa25351782feb96362f0dace2089f
URL:		https://wiki.gnome.org/Projects/PyGObject
BuildRequires:	cairo-gobject-devel
BuildRequires:	glib2-devel >= 1:2.48.0
BuildRequires:	gobject-introspection-devel >= 1.46.0
BuildRequires:	libffi-devel >= 3.0
BuildRequires:	pkgconfig
BuildRequires:	rpm-pythonprov
%{?with_doc:BuildRequires:	sphinx-pdg}
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%if %{with python2}
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-pycairo-devel >= 1.11.1
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-pytest
%endif
%endif
%if %{with python3}
BuildRequires:	python3 >= 1:3.5
BuildRequires:	python3-devel >= 1:3.5
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-pycairo-devel >= 1.11.1
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pytest
%endif
%endif
Requires:	glib2 >= 1:2.48.0
Requires:	gobject-introspection >= 1.46.0
Requires:	python-modules >= 1:2.7
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
Requires:	glib2-devel >= 1:2.48.0
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
Summary:	Python 2 bindings for GObject library - development metapackage
Summary(pl.UTF-8):	Wiązania Pythona 2 do biblioteki GObject - metapakiet programistyczny
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-common-devel = %{version}-%{release}
Requires:	glib2-devel >= 1:2.48.0
Requires:	libffi-devel >= 3.0
Requires:	python-devel >= 1:2.7

%description devel
This metapackage gathers files required to develop GObject bindings
for Python 2.

%description devel -l pl.UTF-8
Ten metapakiet gromadzi pliki wymagane do tworzenia wiązań biblioteki
GObject dla Pythona 2.

%package -n python3-pygobject3
Summary:	Python 3.x bindings for GObject library
Summary(pl.UTF-8):	Wiązania Pythona 3.x do biblioteki GObject
Group:		Libraries/Python
Requires:	glib2 >= 1:2.48.0
Requires:	gobject-introspection >= 1.46.0
Conflicts:	python3-pygobject < 2.28.6-3

%description -n python3-pygobject3
Python 3.x bindings for GObject library.

%description -n python3-pygobject3 -l pl.UTF-8
Wiązania Pythona 3.x do biblioteki GObject.

%package -n python3-pygobject3-devel
Summary:	Python 3 bindings for GObject library - development metapackage
Summary(pl.UTF-8):	Wiązania Pythona 3 do biblioteki GObject - metapakiet programistyczny
Group:		Development/Languages/Python
Requires:	%{name}-common-devel = %{version}-%{release}
Requires:	glib2-devel >= 1:2.48.0
Requires:	libffi-devel >= 3.0
Requires:	python3-devel >= 1:3.5
Requires:	python3-pygobject3 = %{version}-%{release}

%description -n python3-pygobject3-devel
This metapackage gathers files required to develop GObject bindings
for Python 3.

%description -n python3-pygobject3-devel -l pl.UTF-8
Ten metapakiet gromadzi pliki wymagane do tworzenia wiązań biblioteki
GObject dla Pythona 3.

%package apidocs
Summary:	API documentation for Python GObject library
Summary(pl.UTF-8):	Dokumentacja biblioteki Pythona GObject
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for Python GObject library.

%description apidocs -l pl.UTF-8
Dokumentacja biblioteki Pythona GObject.

%package examples
Summary:	Example programs for GObject library
Summary(pl.UTF-8):	Programy przykładowe dla biblioteki GObject
Group:		Development/Languages/Python
Requires:	%{name}-devel = %{version}-%{release}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description examples
This package contains example programs for GObject library.

%description examples -l pl.UTF-8
Ten pakiet zawiera przykładowe programy dla biblioteki GObject.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
%{__make} -C docs
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

cp -a examples/*.py $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc NEWS README.rst
%dir %{py_sitedir}/gi
%attr(755,root,root) %{py_sitedir}/gi/_gi.so
%attr(755,root,root) %{py_sitedir}/gi/_gi_cairo.so
%{py_sitedir}/gi/*.py[co]
%dir %{py_sitedir}/gi/overrides
%{py_sitedir}/gi/overrides/*.py[co]
%dir %{py_sitedir}/gi/repository
%{py_sitedir}/gi/repository/*.py[co]
%dir %{py_sitedir}/pygtkcompat
%{py_sitedir}/pygtkcompat/*.py[co]
%{py_sitedir}/PyGObject-%{version}-py*.egg-info

%files common-devel
%defattr(644,root,root,755)
%{_includedir}/pygobject-3.0
%{_pkgconfigdir}/pygobject-3.0.pc

%files devel
%defattr(644,root,root,755)
%endif

%if %{with python3}
%files -n python3-pygobject3
%defattr(644,root,root,755)
%doc NEWS README.rst
%dir %{py3_sitedir}/gi
%attr(755,root,root) %{py3_sitedir}/gi/_gi.cpython*.so
%attr(755,root,root) %{py3_sitedir}/gi/_gi_cairo.cpython*.so
%{py3_sitedir}/gi/*.py
%{py3_sitedir}/gi/__pycache__
%dir %{py3_sitedir}/gi/overrides
%{py3_sitedir}/gi/overrides/*.py
%{py3_sitedir}/gi/overrides/__pycache__
%dir %{py3_sitedir}/gi/repository
%{py3_sitedir}/gi/repository/*.py*
%{py3_sitedir}/gi/repository/__pycache__
%dir %{py3_sitedir}/pygtkcompat
%{py3_sitedir}/pygtkcompat/*.py
%{py3_sitedir}/pygtkcompat/__pycache__
%{py3_sitedir}/PyGObject-%{version}-py*.egg-info

%files -n python3-pygobject3-devel
%defattr(644,root,root,755)
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/{_images,_static,devguide,guide,*.html,*.js}
%endif

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
