#
# Conditional build:
%bcond_without	tests		# build with tests

# NOTE
# - release tarballs: http://getcomposer.org/download/

%define		rel		15
#define		githash	5744981
# $ git rev-list 1.0.0-alpha11..%{githash} --count
#define		commits	216
%define		subver	alpha11
%define		php_min_version 5.3.4
%include	/usr/lib/rpm/macros.php
Summary:	Dependency Manager for PHP
Name:		composer
Version:	1.0.0
Release:	%{rel}.%{subver}%{?commits:.%{commits}}%{?githash:.g%{githash}}
License:	MIT
Group:		Development/Languages/PHP
#Source0:       https://github.com/composer/composer/archive/%{githash}/%{name}-%{version}-%{subver}-%{commits}-g%{githash}.tar.gz
Source0:	https://github.com/composer/composer/archive/%{version}-%{subver}/%{name}-%{version}-%{subver}.tar.gz
# Source0-md5:	5e4ff16cff75fae31285196c5f51a8f8
Source2:	https://raw.githubusercontent.com/iArren/%{name}-bash-completion/86a8129/composer
# Source2-md5:	cdeebf0a0da1fd07d0fd886d0461642e
Source3:	autoload.php
Patch0:		autoload.patch
Patch1:		update-memory-limit.patch
Patch2:		svn-ignore-externals.patch
Patch3:		version.patch
URL:		http://www.getcomposer.org/
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.673
%if %{with tests}
BuildRequires:	phpab
BuildRequires:	phpunit
%endif
Requires:	php(core) >= %{php_min_version}
Requires:	php(ctype)
Requires:	php(date)
Requires:	php(filter)
Requires:	php(hash)
Requires:	php(json)
Requires:	php(openssl)
Requires:	php(pcre)
Requires:	php(phar)
Requires:	php(posix)
Requires:	php(simplexml)
Requires:	php(spl)
Requires:	php(zip)
Requires:	php(zlib)
Requires:	php-composer-semver >= 1.0.0
Requires:	php-composer-spdx-licenses >= 1.0.0
Requires:	php-justinrainbow-json-schema >= 1.4
Requires:	php-seld-jsonlint >= 1.1.2
Requires:	php-seld-phar-utils >= 1.0.0
Requires:	php-symfony2-ClassLoader >= 2.7.7
Requires:	php-symfony2-Console >= 2.7.7
Requires:	php-symfony2-Finder >= 2.7.7
Requires:	php-symfony2-Process >= 2.7.7
Suggests:	bash-completion-%{name}
Suggests:	git-core
Suggests:	mercurial
Suggests:	subversion
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
%setup -qc -n %{name}-%{version}-%{release}
mv composer-*/* .
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

mv composer.lock{,.disabled}
# NOTE: do not use %{__php} macro here, need unversioned php binary
%{__sed} -i -e '1s,^#!.*env php,#!/usr/bin/php,' bin/*

cp -p %{SOURCE3} src/Composer/autoload.php

# move to Composer dir, this will simplify testing
mv res src/Composer
ln -s src/Composer/res

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

# needs newer phpunit:
# missing method PHPUnit_Framework_MockObject_Builder_InvocationMocker::willReturn()
rm tests/Composer/Test/EventDispatcher/EventDispatcherTest.php
rm tests/Composer/Test/IO/ConsoleIOTest.php
rm tests/Composer/Test/Package/Loader/RootPackageLoaderTest.php
rm tests/Composer/Test/Package/RootAliasPackageTest.php
rm tests/Composer/Test/Package/Version/VersionGuesserTest.php
rm tests/Composer/Test/Util/GitHubTest.php

%build
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
%doc README.md CHANGELOG.md LICENSE PORTING_INFO
%attr(755,root,root) %{_bindir}/composer
%{php_data_dir}/Composer

# top level cachedir, create user cache dirs here manually
%dir %attr(711,root,http) /var/cache/composer

%files -n bash-completion-%{name}
%defattr(644,root,root,755)
%{bash_compdir}/composer
