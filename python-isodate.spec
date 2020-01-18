%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python2_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

%global modulename isodate
%global with_python3 0

Name:           python-%{modulename}
Version:        0.5.4
Release:        8%{?dist}
Summary:        An ISO 8601 date/time/duration parser and formatter
Group:          Development/Languages
License:        BSD
URL:            http://pypi.python.org/pypi/%{modulename}
Source0:        %{modulename}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif # if with_python3

%description
This module implements ISO 8601 date, time and duration parsing. The
implementation follows ISO8601:2004 standard, and implements only date/time
representations mentioned in the standard. If something is not mentioned there,
then it is treated as non existent, and not as an allowed option.

For instance, ISO8601:2004 never mentions 2 digit years. So, it is not intended
by this module to support 2 digit years. (while it may still be valid as ISO
date, because it is not explicitly forbidden.) Another example is, when no time
zone information is given for a time, then it should be interpreted as local
time, and not UTC.

As this module maps ISO 8601 dates/times to standard Python data types, like
date, time, datetime and timedelta, it is not possible to convert all possible
ISO 8601 dates/times. For instance, dates before 0001-01-01 are not allowed by
the Python date and datetime classes. Additionally fractional seconds are
limited to microseconds. That means if the parser finds for instance
nanoseconds it will round it to microseconds.

%if 0%{?with_python3}
%package -n python3-%{modulename}
Summary:        An ISO 8601 date/time/duration parser and formatter
Group:          Development/Languages

%description -n python3-%{modulename}
This module implements ISO 8601 date, time and duration parsing. The
implementation follows ISO8601:2004 standard, and implements only date/time
representations mentioned in the standard. If something is not mentioned there,
then it is treated as non existent, and not as an allowed option.

For instance, ISO8601:2004 never mentions 2 digit years. So, it is not intended
by this module to support 2 digit years. (while it may still be valid as ISO
date, because it is not explicitly forbidden.) Another example is, when no time
zone information is given for a time, then it should be interpreted as local
time, and not UTC.

As this module maps ISO 8601 dates/times to standard Python data types, like
date, time, datetime and timedelta, it is not possible to convert all possible
ISO 8601 dates/times. For instance, dates before 0001-01-01 are not allowed by
the Python date and datetime classes. Additionally fractional seconds are
limited to microseconds. That means if the parser finds for instance
nanoseconds it will round it to microseconds.
%endif

%prep
%setup -qn %{modulename}-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6
%{__python2} setup.py build
%else
CFLAGS="%{optflags}" %{__python2} -c 'import setuptools; execfile("setup.py")' build
%endif

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
rm -rf %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
popd
%endif

%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
%else
%{__python2} -c 'import setuptools; execfile("setup.py")' install --skip-build --root %{buildroot}
%endif

%clean
rm -rf %{buildroot}

%check
%{__python2} setup.py test

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py test
popd
%endif


%files
%defattr(-,root,root,-)
%doc CHANGES.txt README.rst TODO.txt
%{python2_sitelib}/%{modulename}*.egg-info
%{python2_sitelib}/%{modulename}

%if 0%{?with_python3}
%files -n python3-%{modulename}
%doc CHANGES.txt README.rst TODO.txt
%{python3_sitelib}/%{modulename}-*.egg-info
%{python3_sitelib}/%{modulename}
%endif 

%changelog
* Tue Dec  5 2017 Oyvind Albrigtsen <oalbrigt@redhat.com> - 0.5.4-8
- Initial build for RHEL7

  Resolves: rhbz#1511223

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 12 2016 Charalampos Stratakis <cstratak@redhat.com> - 0.5.4-4
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.4-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Nov 19 2015 John Matthews <jwmatthews@gmail.com> - 0.5.4-1
- Update to 0.5.4

* Tue Nov 03 2015 Robert Kuska <rkuska@redhat.com> - 0.5.0-5
- Rebuilt for Python3.5 rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Fri Apr 18 2014 Dan Scott <dan@coffeecode.net> - 0.5.0-1
- Update to 0.5.0
- Add a Python3 build
- Run unit tests
- Remove python-setuptools-devel BR per https://fedoraproject.org/wiki/Changes/Remove_Python-setuptools-devel

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 26 2012 James Laska <jlaska@redhat.com> - 0.4.7-1
- Update to 0.4.7

* Mon Jan 23 2012 James Laska <jlaska@redhat.com> - 0.4.6-1
- Update to 0.4.6

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Sep 28 2011 James Laska <jlaska@redhat.com> - 0.4.4-1
- Initial package build
