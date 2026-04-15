<?php
$phpDir = '/usr/share/php/';

require_once __DIR__ . '/Autoload/ClassLoader.php';

$loader = new \Composer\Autoload\ClassLoader();

// Composer itself (PSR-4)
$loader->setPsr4('Composer\\', array(__DIR__));

// Dependencies (PSR-4)
$loader->setPsr4('Composer\\CaBundle\\', array($phpDir . 'Composer/CaBundle'));
$loader->setPsr4('Composer\\ClassMapGenerator\\', array($phpDir . 'Composer/ClassMapGenerator'));
$loader->setPsr4('Composer\\MetadataMinifier\\', array($phpDir . 'Composer/MetadataMinifier'));
$loader->setPsr4('Composer\\Pcre\\', array($phpDir . 'Composer/Pcre'));
$loader->setPsr4('Composer\\Semver\\', array($phpDir . 'Composer/Semver'));
$loader->setPsr4('Composer\\Spdx\\', array($phpDir . 'Composer/Spdx'));
$loader->setPsr4('Composer\\XdebugHandler\\', array($phpDir . 'Composer/XdebugHandler'));
$loader->setPsr4('JsonSchema\\', array($phpDir . 'JsonSchema'));
$loader->setPsr4('Psr\\Log\\', array($phpDir . 'Psr/Log'));
$loader->setPsr4('React\\Promise\\', array($phpDir . 'React/Promise'));
$loader->setPsr4('Seld\\JsonLint\\', array($phpDir . 'Seld/JsonLint'));
$loader->setPsr4('Seld\\PharUtils\\', array($phpDir . 'Seld/PharUtils'));
$loader->setPsr4('Seld\\Signal\\', array($phpDir . 'Seld/Signal'));
$loader->setPsr4('Symfony\\Component\\Console\\', array($phpDir . 'Symfony/Component/Console'));
$loader->setPsr4('Symfony\\Component\\Filesystem\\', array($phpDir . 'Symfony/Component/Filesystem'));
$loader->setPsr4('Symfony\\Component\\Finder\\', array($phpDir . 'Symfony/Component/Finder'));
$loader->setPsr4('Symfony\\Component\\Process\\', array($phpDir . 'Symfony/Component/Process'));
$loader->setPsr4('Symfony\\Component\\String\\', array($phpDir . 'Symfony/Component/String'));
$loader->setPsr4('Symfony\\Contracts\\Service\\', array($phpDir . 'Symfony/Contracts/Service'));
$loader->setPsr4('Symfony\\Polyfill\\Php73\\', array($phpDir . 'Symfony/Polyfill/Php73'));
$loader->setPsr4('Symfony\\Polyfill\\Php80\\', array($phpDir . 'Symfony/Polyfill/Php80'));
$loader->setPsr4('Symfony\\Polyfill\\Php81\\', array($phpDir . 'Symfony/Polyfill/Php81'));
$loader->setPsr4('Symfony\\Polyfill\\Php84\\', array($phpDir . 'Symfony/Polyfill/Php84'));

$loader->register();

return $loader;
