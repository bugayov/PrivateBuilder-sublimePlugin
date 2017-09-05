<?php

$p = array();
if (isset($_SERVER["argv"][1])) {
    foreach ($_SERVER["argv"] as $key => $value) {
        $l = explode('=', $value);
        if (count($l) == 2) {
            $paramName = trim(strtolower($l[0]), ' ()[]');
            if (strlen($paramName) > 0) {
                $p[$paramName] = trim($l[1]);
            }
        }
    }
}
$instruction = '
Для нормальной работы php-cs-fixer необходимо установить сам скрипт.
Его необходимо скачать отсюда: https://github.com/FriendsOfPHP/PHP-CS-Fixer
Затем, необходимо прописать путь к файлу в настроках Sublime Text 3, например:

insert insert this code into Preferences.sublime-settings:
[
    "my_builder_php_cs_fixer": "/..path_to_php_cs_fixer../php-cs-fixer.phar",
]

Также рекомендуется произвести настройки keymap, полная инструкуия по адресу:
https://github.com/bugayov/PrivateBuilder-sublimePlubin

████████████████████████████████████████████████████████
█────█─██─█────█████────█───█████───█───█──█──█───█────█
█─██─█─██─█─██─█████─██─█─███████─████─███───██─███─██─█
█────█────█────█───█─████───█───█───██─████─███───█────█
█─████─██─█─████████─██─███─█████─████─███───██─███─█─██
█─████─██─█─████████────█───█████─███───█──█──█───█─█─██
████████████████████████████████████████████████████████
Спасибо сервису, который помог написать красиво :-)
http://vkontakte.doguran.ru/kak-pisat-simvolami.php
';
if (isset($p)) {
    echo '[cmd_php.php]' . $p['file'];
    echo "\n" . '===============================================================================' . "\n";
    print_r($p);
    echo $instruction;
    echo "\n" . '===============================================================================' . "\n";
}
