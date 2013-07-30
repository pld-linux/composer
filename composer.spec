#
# NOTE
# - release tarballs: http://getcomposer.org/download/

# Conditional build:
%bcond_with	bootstrap		# build boostrap

%define		php_min_version 5.3.4
%define		subver	alpha7
%define		rel		0.16
%include	/usr/lib/rpm/macros.php
Summary:	Dependency Manager for PHP
Name:		composer
Version:	1.0.0
Release:	0.%{subver}.%{rel}
License:	MIT
Group:		Development/Languages/PHP
#Source0:	https://github.com/composer/composer/archive/%{version}-%{subver}.tar.gz
Source0:	http://github.com/composer/composer/tarball/master?/%{name}.tgz
# Source0-md5:	661b31437f47e3ff23e616ab3fb21831
Source1:	http://getcomposer.org/download/%{version}-%{subver}/%{name}.phar
# Source1-md5:	f9b1dbd4ad0e3707bfe216690b210a7e
Patch0:		nogit.patch
Patch1:		no-bundle-symfony.patch
Patch2:		system-symfony.patch
URL:		http://www.getcomposer.org/
BuildRequires:	/usr/bin/php
BuildRequires:	php(ctype)
BuildRequires:	php(hash)
BuildRequires:	php(json)
BuildRequires:	php(openssl)
BuildRequires:	php(phar)
BuildRequires:	php(zip)
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.461
%if %{without bootstrap}
BuildRequires:	%{name}
%endif
Requires:	php(core) >= %{php_min_version}
Requires:	php(hash)
Requires:	php(phar)
Requires:	php-symfony2-Console >= 2.1
Requires:	php-symfony2-Finder >= 2.1
Requires:	php-symfony2-Process >= 2.1
Suggests:	git-core
Suggests:	mercurial
Suggests:	php(openssl)
Suggests:	php(zip)
Suggests:	subversion
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir		%{_datadir}/%{name}

%description
Composer is a tool for dependency management in PHP. It allows you to
declare the dependent libraries your project needs and it will install
them in your project for you.

%prep
%setup -qc
mv composer-composer-*/* .
%patch0 -p1
%patch1 -p1

mv composer.lock{,.disabled}
%{__sed} -i -e '1s,^#!.*env php,#!%{__php},' bin/*

%build
%if %{with bootstrap}
composer='%{__php} %{SOURCE1}'
%else
composer=composer
%endif
if [ ! -d vendor ]; then
	COMPOSER_HOME=${PWD:=$(pwd)} \
	$composer install --prefer-dist -v
	%{__patch} -p1 < %{PATCH2}
fi

V=$(echo composer-composer-*)
V=${V#composer-composer-}
COMPOSER_VERSION=%{version}%{?subver:-%{subver}}${V:+-g$V} \
%{__php} -d phar.readonly=0 ./bin/compile

# sanity check
%{__php} composer.phar --version

install -d build
%{__php} -r '$phar = new Phar($argv[1]); $phar->extractTo($argv[2]);' composer.phar build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_appdir}}
cd build
cp -a bin src res vendor $RPM_BUILD_ROOT%{_appdir}
ln -s %{_appdir}/bin/%{name} $RPM_BUILD_ROOT%{_bindir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md CHANGELOG.md LICENSE PORTING_INFO
%attr(755,root,root) %{_bindir}/composer
%dir %{_appdir}
%dir %{_appdir}/bin
%attr(755,root,root) %{_appdir}/bin/*
%{_appdir}/res
%{_appdir}/src
%{_appdir}/vendor
