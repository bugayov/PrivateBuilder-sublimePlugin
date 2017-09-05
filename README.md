# PrivateBuilder-sublimePlugin

Плагин позволяет выполнять скрипты (с определенной маской) прямо из Sublime Text 3.
На данный момент поддерживаются такие типы файлов:
* .app.php - для выполнения тестовых примеров на PHP
* .class.php - для отладки отдельного класса
* .app.js - выполнение тестовыз примеров на Node.js (JavaScript)
* .csv - пример обработки CSV
* .app.py - для выполнения тестовых примеров на Python
* .app.java - для выполнения тестовых примеров на Java
* .sql - для выполнения тестовых примеров на SQL (неободим внешний скрипт)

Кроме того, есть возможность исправить код PHP в стандарт PSR-2 (Необходим внешний скрипт php-cs-fixer)


### Default Shortcuts

* Выполение текущего скрипта: _f5_
* Исправление PHP PSR-2: _ctrl + shift + f5_


### Settings

insert insert this code into `Preferences.sublime-settings`:
```javascript
[
    "my_builder_php_cs_fixer": "/..path_to_php_cs_fixer../php-cs-fixer.phar",
    "my_builder_sql_http_script": "/..path_to_sql_http../sql_http/index.php",
]
```

insert insert this code into `Default (Linux).sublime-keymap` or `Default (Windows).sublime-keymap`:
```javascript
[
    { "keys": ["f5"], "command": "my_build_current_code" },
    { "keys": ["ctrl+shift+f5"], "command": "my_build_php_cs_fixer" },
]
```