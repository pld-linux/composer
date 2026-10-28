#!/bin/sh
# Regenerate the vendor/ archive (Source1) from upstream composer.lock.
# usage: ./update-source.sh [version]   (default: Version from the spec)
set -e

dir=$(cd "$(dirname "$0")" && pwd)
cd "$dir"
pkg=$(basename "$dir")
specfile=$pkg.spec
php=${PHP:-php}

oldversion=$(awk '/^Version:/{print $2; exit}' $specfile)
version=${1:-$oldversion}
tarball=composer-$version.tar.gz
vendor=$pkg-vendor-$version.tar.xz

test -f $tarball || wget -nv -O $tarball https://github.com/composer/composer/archive/$version/$tarball

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT INT TERM

# installer of the same version, checked against the published checksum
wget -nv -O $tmp/composer.phar https://getcomposer.org/download/$version/composer.phar
sum=$(wget -qO- https://getcomposer.org/download/$version/composer.phar.sha256sum | awk '{print $1}')
echo "$sum  $tmp/composer.phar" | sha256sum -c -

tar xzf $tarball -C $tmp
cd $tmp/composer-$version
export COMPOSER_ROOT_VERSION=$version COMPOSER_HOME=$tmp/home COMPOSER_CACHE_DIR=$tmp/cache COMPOSER_NO_INTERACTION=1
# 2.2 picks a random autoloader suffix; pin it to the lock's content-hash as 2.3+ does
hash=$(sed -n 's/^ *"content-hash": "\([0-9a-f]*\)".*/\1/p' composer.lock)
mkdir $COMPOSER_HOME
echo "{\"config\": {\"autoloader-suffix\": \"$hash\"}}" > $COMPOSER_HOME/config.json
$php $tmp/composer.phar install --no-dev --no-plugins --no-scripts --no-progress --quiet
# the phar ships whitespace-stripped sources; dump again with this tree so
# vendor/composer/ClassLoader.php is the tag's own file
$php bin/composer dump-autoload --no-dev --no-plugins --no-scripts --quiet
cmp vendor/composer/ClassLoader.php src/Composer/Autoload/ClassLoader.php
$php <<'EOF'
<?php
$lock = json_decode(file_get_contents('composer.lock'), true);
$inst = json_decode(file_get_contents('vendor/composer/installed.json'), true);
$inst = isset($inst['packages']) ? $inst['packages'] : $inst;
$want = $got = array();
foreach ($lock['packages'] as $p) $want[$p['name']] = $p['version'];
foreach ($inst as $p) $got[$p['name']] = $p['version'];
ksort($want); ksort($got);
if ($want !== $got) { fwrite(STDERR, "vendor/ does not match composer.lock\n"); exit(1); }
echo count($got), " packages, matching composer.lock\n";
EOF

tar --sort=name --owner=0 --group=0 --numeric-owner --mode=u+rwX,go+rX,go-w \
	--mtime=@$(stat -c %Y composer.json) -cf - vendor | xz -T1 -9 > "$dir/$vendor"
cd "$dir"

if [ "$version" != "$oldversion" ]; then
	sed -i -e "s/^\(Version:[[:space:]]*\).*/\1$version/" -e "s/^\(Release:[[:space:]]*\).*/\11/" $specfile
fi
../builder -ncs -5 $specfile
