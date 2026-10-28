#
# Conditional build:
%bcond_with	online		# online self-test

%if 0%{?_pld_builder:1}
%undefine	with_online
%endif

%define		php_min_version 7.2.5
Summary:	Dependency Manager for PHP
Name:		composer
Version:	2.10.3
Release:	1
License:	MIT
Group:		Development/Languages/PHP
Source0:	https://github.com/composer/composer/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	ee742fb3f7deca7a211e9394f154ce67
# vendor/ installed from upstream composer.lock, as in the official phar;
# regenerate with ./update-source.sh [version]
Source1:	%{name}-vendor-%{version}.tar.xz
# Source1-md5:	cfb1c7633fede80fbd1b13742bce8fa4
Source2:	https://raw.githubusercontent.com/iArren/%{name}-bash-completion/86a8129/composer
# Source2-md5:	cdeebf0a0da1fd07d0fd886d0461642e
URL:		https://getcomposer.org/
BuildRequires:	php-devel
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.673
%{?with_online:BuildRequires:	%{php_name}-cli}
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
%setup -q -a1

# NOTE: do not use %{__php} macro here, need unversioned php binary
%{__sed} -i -e '1s,^#!.*env php,#!/usr/bin/php,' bin/composer

%build
%if %{with online}
# always run self-test
%{__php} ./bin/composer diagnose
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{name}/bin,%{php_data_dir}/Composer,/var/cache/composer}
# AutoloadGenerator copies LICENSE from the top of the tree into generated autoloaders
cp -a LICENSE res src vendor $RPM_BUILD_ROOT%{_datadir}/%{name}
install -p bin/composer $RPM_BUILD_ROOT%{_datadir}/%{name}/bin
# command line tools of the bundled libraries, composer does not run them
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/%{name}/vendor/{bin,justinrainbow/json-schema/bin,seld/jsonlint/bin}
ln -s %{_datadir}/%{name}/bin/composer $RPM_BUILD_ROOT%{_bindir}/%{name}
# library autoloader for compatibility (satis)
ln -s %{_datadir}/%{name}/vendor/autoload.php $RPM_BUILD_ROOT%{php_data_dir}/Composer/autoload.php

install -d $RPM_BUILD_ROOT%{bash_compdir}
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{bash_compdir}/composer

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/composer
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/bin
%attr(755,root,root) %{_datadir}/%{name}/bin/composer
%{_datadir}/%{name}/LICENSE
%{_datadir}/%{name}/res
%{_datadir}/%{name}/src
%{_datadir}/%{name}/vendor
%dir %{php_data_dir}/Composer
%{php_data_dir}/Composer/autoload.php

# top level cachedir, create user cache dirs here manually
%dir %attr(711,root,http) /var/cache/composer

%files -n bash-completion-%{name}
%defattr(644,root,root,755)
%{bash_compdir}/composer
