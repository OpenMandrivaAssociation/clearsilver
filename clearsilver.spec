%bcond_without	ruby
%bcond_without	python
%bcond_without	perl

Summary:	ClearSilver HTML template system
Name:		clearsilver
Version:	0.10.5
Release:	5
License:	Apache License style
Group:		Networking/WWW
Source0:	http://www.clearsilver.net/downloads/%{name}-%{version}.tar.bz2
Patch0:		clearsilver-0.10.5-mandriva.patch
Patch1:		clearsilver-0.10.5-regression.patch
Patch2:		test.patch
URL:		http://www.clearsilver.net/
BuildRequires:	zlib-devel
%if %{with python}
BuildRequires:	python-devel
%endif
%if %{with perl}
BuildRequires:	perl-devel
%endif
%if %{with ruby}
BuildRequires:	ruby-devel >= 1.4.5
%endif

%description
ClearSilver is a fast, powerful, and language-neutral HTML template system.
In both static content sites and dynamic HTML applications, it provides a
separation between presentation code and application logic which makes
working with your project easier.

Because it's written as a C-library, and exported to scripting languages
like Python and Perl via modules, it is extremely fast compared to template
systems written in a script language.

%package	devel
Summary:	ClearSilver development package
Group:		Development/C

%description devel
This package provides needed files to develop extension
to ClearSilver.

%if %{with python}
%package -n	python-%{name}
Summary:	Neotonic ClearSilver Python Module
Group:		Development/Python
Requires:	clearsilver = %{version}

%description -n	python-%{name}
This package provides a python interface to the
clearsilver CGI kit and templating system.
%endif

%if %{with perl}
%package -n	perl-ClearSilver
Summary:	Neotonic ClearSilver Perl Module
Group:		Development/Perl
Requires:	clearsilver = %{version}

%description -n perl-ClearSilver
The clearsilver-perl package provides a perl interface to the
clearsilver templating system.
%endif

%if %{with ruby}
%package -n	ruby-%{name}
Summary:	Neotonic ClearSilver Ruby Module
Group:		Development/Ruby
Requires:	clearsilver = %{version}

%description -n	ruby-%{name}
The clearsilver-ruby package provides a ruby interface to the
clearsilver templating system.
%endif

%prep
%setup -q
%patch0 -p0
%patch1 -p1
%patch2 -p0

%build
%configure	--disable-apache \
		--disable-java \
		--disable-csharp \
%if %{with ruby}
		--enable-ruby \
%else
		--disable-ruby \
%endif
%if %{with perl}
		--enable-perl \
%else
		--disable-perl \
%endif
%if %{with python}
		--enable-python
%else
		--disable-python
%endif
perl -pi -e 's#install.rb install$#install.rb install --prefix=%{buildroot}#' ruby/Makefile
perl -pi -e 's/555/755/' ruby/install.rb

%make

cat > README.MandrivaLinux << EOF
This package only includes python, perl and ruby bindings.

Java needs a JVM, so this cannot be done for the moment.
C# didn't compile.

EOF
%install
perl -pi -e 's#/usr/local/#/usr/#' scripts/document.py
%if %{with perl}
cd perl
perl Makefile.PL INSTALLDIRS=vendor
%makeinstall_std
cd ..
%endif
%makeinstall_std

%if %{with python}
cd python
python setup.py install --root=%{buildroot}
cd ..
%endif

#
# TODO add script ( in script/ subdir )
# emacs mode
%files
%doc CS_LICENSE INSTALL LICENSE README README.MandrivaLinux scripts/cs_lint.py contrib/cs-mode.el
%{_bindir}/*
%{_mandir}/man3/*.3.*

%files devel
%defattr(-,root,root)
%{_includedir}/ClearSilver/
%{_libdir}/libneo_cgi.a
%{_libdir}/libneo_cs.a
%{_libdir}/libneo_utl.a

%if %{with python}
%files -n python-%{name}
%doc README.python
%{python_sitearch}/neo_cgi.so
%{python_sitearch}/clearsilver-%{version}-py%{py_ver}.egg-info
%endif

%if %{with perl}
%files -n perl-ClearSilver
%{perl_vendorlib}/*/ClearSilver.pm
%{perl_vendorlib}/*/auto/ClearSilver/ClearSilver.so
%dir %{perl_vendorlib}/*/auto/ClearSilver/
%{_mandir}/man3/*.3pm*
%endif

%if %{with ruby}
%defattr(-,root,root)
%{ruby_sitelibdir}/neo.rb
%{ruby_sitearchdir}/hdf.so
%endif

#%if %{with apache_subpackage}
#%files apache
#%{apache_libexec}/mod_ecs.so
#%endif
