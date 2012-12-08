#
# Conditional build:
%bcond_with	bootstrap		# build boostrap

%define		pkgname	composer
%define		php_min_version 5.3.4
%define		subver	alpha6
%define		rel		0.2
%include	/usr/lib/rpm/macros.php
Summary:	Dependency Manager for PHP
Name:		%{pkgname}-php
Version:	1.0.0
Release:	0.%{subver}.%{rel}
License:	MIT
Group:		Development/Languages/PHP
Source0:	https://github.com/composer/composer/archive/%{version}-%{subver}.tar.gz
# Source0-md5:	bb5ad93089d09a1e58cfaf28fb5c2ab4
Source1:	http://getcomposer.org/download/%{version}-%{subver}/%{pkgname}.phar
# Source1-md5:	f9b1dbd4ad0e3707bfe216690b210a7e
Patch0:		nogit.patch
URL:		http://www.getcomposer.org/
BuildRequires:	/usr/bin/php
BuildRequires:	php(phar)
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.461
%if %{without bootstrap}
BuildRequires:	%{name}
%endif
Requires:	php(core) >= %{php_min_version}
Requires:	php(phar)
Suggests:	git-core
Suggests:	mercurial
Suggests:	php(openssl)
Suggests:	php(zip)
Suggests:	subversion
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Composer is a tool for dependency management in PHP. It allows you to
declare the dependent libraries your project needs and it will install
them in your project for you.

%prep
%setup -q -n %{pkgname}-%{version}%{?subver:-%{subver}}
%patch0 -p1

%build
%if %{with bootstrap}
cp -p %{SOURCE1} .
%else
composer install -v

COMPOSER_VERSION=%{version}%{?subver:-%{subver}} \
%{__php} -d phar.readonly=0 ./bin/compile
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
cp -p %{pkgname}.phar $RPM_BUILD_ROOT%{_bindir}/%{pkgname}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md CHANGELOG.md LICENSE PORTING_INFO
%attr(755,root,root) %{_bindir}/composer
