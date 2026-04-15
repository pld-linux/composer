#
# Conditional build:
%bcond_with	tests		# build with tests
%bcond_with	online		# online self-test

%if 0%{?_pld_builder:1}
%undefine	with_online
%endif

%define		php_min_version 7.2.5
Summary:	Dependency Manager for PHP
Name:		composer
Version:	2.9.5
Release:	3
License:	MIT
Group:		Development/Languages/PHP
Source0:	https://github.com/composer/composer/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	db62f452564f8042d8206919f9edaf2b
Source2:	https://raw.githubusercontent.com/iArren/%{name}-bash-completion/86a8129/composer
# Source2-md5:	cdeebf0a0da1fd07d0fd886d0461642e
Source3:	autoload.php
Patch0:		autoload.patch
URL:		https://getcomposer.org/
BuildRequires:	php-devel
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.673
%{?with_online:BuildRequires:	%{php_name}-cli}
%if %{with tests}
BuildRequires:	composer >= 2.0.0
BuildRequires:	git-core
BuildRequires:	phpab
BuildRequires:	phpunit >= 4.8
%endif
Requires:	php(core) >= %{php_min_version}
Requires:	php(ctype)
Requires:	php(date)
Requires:	php(filter)
Requires:	php(hash)
Requires:	php(json)
Requires:	php(mbstring)
Requires:	php(openssl)
Requires:	php(pcntl)
Requires:	php(pcre)
Requires:	php(phar)
Requires:	php(posix)
Requires:	php(simplexml)
Requires:	php(spl)
Requires:	php(zip)
Requires:	php(zlib)
Requires:	php-composer-ca-bundle >= 1.5
Requires:	php-composer-class-map-generator >= 1.4.0
Requires:	php-composer-metadata-minifier >= 1.0
Requires:	php-composer-pcre >= 2.3
Requires:	php-composer-semver >= 3.3
Requires:	php-composer-spdx-licenses >= 1.5.7
Requires:	php-composer-xdebug-handler >= 2.0.2
Requires:	php-justinrainbow-json-schema >= 6.5.1
Requires:	php-psr-log >= 1.0
Requires:	php-react-promise >= 3.3
Requires:	php-seld-jsonlint >= 1.4
Requires:	php-seld-phar-utils >= 1.2
Requires:	php-seld-signal-handler >= 2.0
Requires:	php-symfony-Console >= 5.4.47
Requires:	php-symfony-Filesystem >= 5.4.45
Requires:	php-symfony-Finder >= 5.4.45
Requires:	php-symfony-Process >= 5.4.47
Requires:	php-symfony-ServiceContracts >= 2.5
Requires:	php-symfony-String >= 5.4
Requires:	unzip
Suggests:	bash-completion-%{name}
Suggests:	git-core
Suggests:	mercurial
Suggests:	subversion
Conflicts:	composer1
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Composer is a tool for dependency management in PHP.

Composer helps you declare, manage and install dependencies of PHP
projects, ensuring you have the right stack everywhere.

%package -n bash-completion-%{name}
Summary:	Bash completion for Composer
Summary(pl.UTF-8):	bashowe uzupełnianie nazw dla Composera
Group:		Applications/Shells
Requires:	%{name}
Requires:	bash-completion >= 2.0

%description -n bash-completion-%{name}
Bash completion for Composer package and dependency manager.

%description -n bash-completion-%{name} -l pl.UTF-8
Pakiet ten dostarcza bashowe uzupełnianie nazw dla Composera.

%prep
%setup -q
%patch -P0 -p1

mv composer.lock{,.disabled}
# NOTE: do not use %{__php} macro here, need unversioned php binary
%{__sed} -i -e '1s,^#!.*env php,#!/usr/bin/php,' bin/*

cp -p %{SOURCE3} src/Composer/autoload.php

# AutoloadGenerator needs this runtime
mv LICENSE res
# move to Composer dir, this will simplify testing
mv res src/Composer
ln -s src/Composer/res

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%build
%if %{with online}
# always run self-test
%{__php} ./bin/composer diagnose
%endif

%if %{with tests}
phpab -n -o src/bootstrap.php -e '*/Fixtures/*' src/ tests/
echo "require 'src/Composer/autoload.php';" >> src/bootstrap.php
phpunit
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{php_data_dir}/Composer,/var/cache/composer}
cp -a src/Composer $RPM_BUILD_ROOT%{php_data_dir}
install -p bin/composer $RPM_BUILD_ROOT%{_bindir}/%{name}

install -d $RPM_BUILD_ROOT%{bash_compdir}
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{bash_compdir}/composer

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc src/Composer/res/LICENSE
%attr(755,root,root) %{_bindir}/composer
%{php_data_dir}/Composer

# top level cachedir, create user cache dirs here manually
%dir %attr(711,root,http) /var/cache/composer

%files -n bash-completion-%{name}
%defattr(644,root,root,755)
%{bash_compdir}/composer
