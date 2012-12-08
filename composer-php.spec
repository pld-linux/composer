%define		pkgname	composer
%define		php_min_version 5.3.4
%define		subver	alpha6
%define		rel		0.1
%include	/usr/lib/rpm/macros.php
Summary:	Dependency Manager for PHP
Name:		%{pkgname}-php
Version:	1.0.0
Release:	0.%{subver}.%{rel}
License:	MIT
Group:		Development/Languages/PHP
Source0:	http://getcomposer.org/download/1.0.0-alpha6/%{pkgname}.phar
# Source0-md5:	f9b1dbd4ad0e3707bfe216690b210a7e
URL:		http://www.getcomposer.org/
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.461
Requires:	php(core) >= %{php_min_version}
Requires:	php(phar)
Suggests:	git-core
Suggests:	mercurial
Suggests:	php(openssl)
Suggests:	subversion
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Composer is a tool for dependency management in PHP. It allows you to
declare the dependent libraries your project needs and it will install
them in your project for you.

%prep
%setup -qcT

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
cp -p %{SOURCE0} $RPM_BUILD_ROOT%{_bindir}/%{pkgname}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/composer
