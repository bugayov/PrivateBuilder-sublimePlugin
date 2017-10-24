<?php

namespace bugayov\PrivateBuilder;

/**
* Вспомагательный класс для идентификации PHP-скрипта из редактора Sublime Text 3
*/
class PrivatBuilderSublimePlugin
{
    private static $instance;  // экземпляр объекта
    private $args;
    private $scriptName;
    /**
     * Защищаем от создания через new Singleton
     */
    private function __construct() {
        $this->args = [];
        if (isset($_SERVER["argv"][1])) {
            foreach ($_SERVER["argv"] as $key => $value) {
                $l = explode('=', $value);
                if (count($l) === 2) {
                    $paramName = trim(strtolower($l[0]), ' ()[]');
                    if (strlen($paramName) > 0) {
                        $this->args[$paramName] = trim($l[1], ' ()[]"');
                    }
                }
            }
        }
        if (isset($this->args['file']) && file_exists($this->args['file'])) {
            $this->scriptName = $this->args['file'];
        } else {
            $this->scriptName = '';
        }
    }
    private function __clone()    { /* ... @return Singleton */ }  // Защищаем от создания через клонирование
    private function __wakeup()   { /* ... @return Singleton */ }  // Защищаем от создания через unserialize
    public static function getInstance() {    // Возвращает единственный экземпляр класса. @return Singleton
        if ( empty(self::$instance) ) {
            self::$instance = new self();
        }
        return self::$instance;
    }
    public function getScript() {
        return $this->scriptName;
    }
}

// Позволяет подгружать классы, которые расположены в одной папке со скриптом
spl_autoload_register(function ($className) {
    $charItems = explode('\\', $className);
    $f = $charItems[count($charItems)-1];
    $path = dirname(PrivatBuilderSublimePlugin::getInstance()->getScript());
    $fileName = $path . DIRECTORY_SEPARATOR . $f . '.php';
    $fileNameClass = $path . DIRECTORY_SEPARATOR . $f . '.class.php';
    if (file_exists($fileName)) {
        require_once($fileName);
    } elseif (file_exists($fileNameClass)) {
        require_once($fileNameClass);
    } else {
    }
});

// Поехали! запускаем наш скрипт:
$scriptName = PrivatBuilderSublimePlugin::getInstance()->getScript();
if (strlen($scriptName) > 0) {
    echo '[cmd_php.php]' . $scriptName;
    echo "\n" . '===============================================================================' . "\n";
    require_once($scriptName);
    echo "\n" . '===============================================================================' . "\n";
}



