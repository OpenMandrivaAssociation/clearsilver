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
Patch3:		clearsilver-ruby-1.9.patch
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
%patch3 -p1 -b .ruby19~

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
cd python
LDSHARED="gcc -shared -lz %{ldflags}" python setup.py build

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


%changelog
* Wed Feb 15 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 0.10.5-5
+ Revision: 774115
- fix python extension build
- fix build against ruby 1.9 (P3, from Fedora)
- clean up python install etc..
- fix python version macro
- fix man page being packaged into two packages
- use %%bcond
- cleanups
- mass rebuild of perl extensions against perl 5.14.2

* Wed Nov 03 2010 Michael Scherer <misc@mandriva.org> 0.10.5-4mdv2011.0
+ Revision: 592730
- rebuild for python 2.7

* Tue Jul 20 2010 Jérôme Quelin <jquelin@mandriva.org> 0.10.5-3mdv2011.0
+ Revision: 555700
- rebuild

* Thu Sep 10 2009 Thierry Vignaud <tv@mandriva.org> 0.10.5-2mdv2010.0
+ Revision: 437056
- rebuild

* Thu Jan 08 2009 Jérôme Soyer <saispo@mandriva.org> 0.10.5-1mdv2009.1
+ Revision: 327100
- Rediff patch and upgrade

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Michael Scherer <misc@mandriva.org>
    - update to new version 0.10.5

* Mon Jan 21 2008 Thierry Vignaud <tv@mandriva.org> 0.10.4-3mdv2008.1
+ Revision: 155657
- rebuild for new perl
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Fri Dec 14 2007 Thierry Vignaud <tv@mandriva.org> 0.10.4-2mdv2008.1
+ Revision: 119948
- do package README.MandrivaLinux
- s/mandrake/mandriva/
- fix man pages

* Sun May 27 2007 Pascal Terjan <pterjan@mandriva.org> 0.10.4-2mdv2008.0
+ Revision: 31642
- use Development/Ruby for tuby sub package


* Mon Dec 18 2006 Michael Scherer <misc@mandriva.org> 0.10.4-1mdv2007.0
+ Revision: 98546
- update to 0.10.4

* Mon Dec 11 2006 Michael Scherer <misc@mandriva.org> 0.10.3-2mdv2007.1
+ Revision: 94813
- rebuild for new python

* Wed Nov 01 2006 Michael Scherer <misc@mandriva.org> 0.10.3-1mdv2007.1
+ Revision: 74904
- fix ruby binding build, remove useless macros
- update to version 0.10.3
- fix building of perl module
- bunzip patch
- Import clearsilver

