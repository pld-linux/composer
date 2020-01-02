<?php
$phpDir = defined('PHP_DATADIR') && PHP_DATADIR ? PHP_DATADIR . '/php/' : '/usr/share/php/';

// Use Symfony autoloader
if (!isset($loader) || !($loader instanceof \Symfony\Component\ClassLoader\ClassLoader)) {
    if (!class_exists('Symfony\\Component\\ClassLoader\\ClassLoader', false)) {
        require_once $phpDir . '/Symfony/Component/ClassLoader/ClassLoader.php';
    }

    $loader = new \Symfony\Component\ClassLoader\ClassLoader();
    $loader->register();
}

$baseDir = dirname(__DIR__);

$loader->addPrefixes(array(
    'Composer\\'  => $baseDir,
    // Dependencies
    'Composer\\CaBundle\\' => array($phpDir),
    'Composer\\Semver\\' => array($phpDir),
    'Composer\\Spdx\\' => array($phpDir),
    'Composer\\XdebugHandler\\' => array($phpDir),
    'JsonSchema' => array($phpDir),
    'Psr\\Log\\' => array($phpDir),
    'Seld\\JsonLint' => array($phpDir),
    'Seld\\PharUtils\\' => array($phpDir),
    'Symfony\\Component\\Console\\' => array($phpDir),
    'Symfony\\Component\\Filesystem\\' => array($phpDir),
    'Symfony\\Component\\Finder' => array($phpDir),
    'Symfony\\Component\\Process\\' => array($phpDir),
));

return $loader;
