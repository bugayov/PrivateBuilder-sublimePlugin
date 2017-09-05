# insert insert this code into Default (Windows).sublime-keymap:
# [
#     { "keys": ["f5"], "command": "build_current_code" },
# ]

import time
import sublime
import sublime_plugin
import os
from inspect import getmembers
from pprint import pprint
import re
import shutil
import uuid
from datetime import datetime

# { "keys": ["f5"], "command": "my_build_current_code" },
class MyBuildCurrentCodeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        file_name = sublime.active_window().active_view().file_name()
        if (MyBuildCurrentCodeCommand.is_maskfile_valid(file_name, '.app.php')):
            MyBuildCurrentCodeCommand.run_php(file_name)
        elif (MyBuildCurrentCodeCommand.is_maskfile_valid(file_name, '.class.php')):
            MyBuildCurrentCodeCommand.run_php(file_name)
        elif (MyBuildCurrentCodeCommand.is_maskfile_valid(file_name, '.app.js')):
            MyBuildCurrentCodeCommand.run_node(file_name)
        elif (MyBuildCurrentCodeCommand.is_maskfile_valid(file_name, '.csv')):
            MyBuildCurrentCodeCommand.run_anki(file_name)
        elif (MyBuildCurrentCodeCommand.is_maskfile_valid(file_name, '.app.py')):
            MyBuildCurrentCodeCommand.run_python(file_name)
        elif (MyBuildCurrentCodeCommand.is_maskfile_valid(file_name, '.app.java')):
            MyBuildCurrentCodeCommand.run_java(file_name)
        elif (MyBuildCurrentCodeCommand.is_maskfile_valid(file_name, '.sql')):
            count_cursors = len(self.view.sel())
            selected_text = self.view.substr(self.view.sel()[0])
            MyBuildCurrentCodeCommand.exec_mysql(file_name, count_cursors, selected_text)
    def is_maskfile_valid(file, mask):
        a = file.lower().split(mask.lower())
        l = len(a)
        if (l > 0 and a[l-1] == ''):
            return True
        else:
            return False
    def get_file_buffer(file, selected_text):
        file_buffer = file + '.buffer'
        f = open(file_buffer, 'w')
        f.write(selected_text)
        f.close()
        return file_buffer
    def run_php(file):
        sublime.active_window().active_view().window().run_command("save")
        cmd_php = os.path.join(os.path.dirname(__file__), 'cmd_php.php')
        cmd_string = 'php ' + cmd_php + ' "(file)=' + file + '"'
        sublime.active_window().active_view().window().run_command("exec", {
            'shell': True,
            'cmd': cmd_string
        })
        return
    def run_anki(file):
        sublime.active_window().active_view().window().run_command("save")
        cmd_php = os.path.join(os.path.dirname(__file__), 'cmd_anki.php')
        cmd_string = 'php ' + cmd_php + ' "(file)=' + file + '"'
        sublime.active_window().active_view().window().run_command("exec", {
            'shell': True,
            'cmd': cmd_string
        })
        return
    def run_python(file):
        sublime.active_window().active_view().window().run_command("save")
        cmd_php = os.path.join(os.path.dirname(__file__), 'cmd_anki.php')
        cmd_string = 'python ' + file
        sublime.active_window().active_view().window().run_command("exec", {
            'shell': True,
            'cmd': cmd_string
        })
        return
    def run_java(file):
        sublime.active_window().active_view().window().run_command("save")
        cmd_php = os.path.join(os.path.dirname(__file__), 'cmd_anki.php')
        # Поехали, алгоритм компиляции Java-кода
        oldFileName = file
        # Создаём папку, или чистим её, если она создана ранее
        pathJava = os.path.join(os.path.dirname(__file__), 'java')
        if (os.path.exists(pathJava) and  os.path.isdir(pathJava)):
            listDir = os.listdir(pathJava)
            for f in listDir:
                shutil.rmtree(os.path.join(pathJava, f) )
        else:
            os.mkdir(pathJava)

        timestamp1 = datetime.strftime(datetime.now(), "%Y-%m-%d-%H%M%S") + '-' + uuid.uuid4().hex[0:8]
        pathJavaTemp = os.path.join(pathJava, timestamp1)
        os.mkdir(pathJavaTemp)

        newFileNameJava = os.path.join(pathJavaTemp, os.path.basename(oldFileName).split('.')[0] + '.java')
        newFileNameClass = os.path.join(pathJavaTemp, os.path.basename(oldFileName).split('.')[0] + '.class')
        className = os.path.basename(oldFileName).split('.')[0]


        shutil.copy(oldFileName, newFileNameJava)


        cmd_string = 'javac ' + newFileNameJava
        sublime.active_window().active_view().window().run_command("exec", {
            'shell': True,
            'cmd': cmd_string
        })

        # TODO: В обычных языках программирования нужно ожидать окончания процесса
        # но я не знаю, как это делать, поэтому поставил задержку
        time.sleep(1)
        print(newFileNameClass)
        if os.path.isfile(newFileNameClass):
            cmd_string = 'java -classpath ' + pathJavaTemp + ' ' + className
            sublime.active_window().active_view().window().run_command("exec", {
                'shell': True,
                'cmd': cmd_string
            })
        else:
            print ('file not found: ' + newFileNameClass)
        return
    def run_node(file):
        sublime.active_window().active_view().window().run_command("save")
        cmd_string = 'node "' + file + '"'
        sublime.active_window().active_view().window().run_command("exec", {
            'shell': True,
            'cmd': cmd_string
        })
        return
    def exec_mysql(file, count_cursors, selected_text):
        sublime.active_window().active_view().window().run_command("save")
        # cmd_mysql = os.path.join(os.path.dirname(__file__), 'exec_mysql.php')
        settings = sublime.load_settings("Preferences.sublime-settings")
        sql_http_script = settings.get("my_builder_sql_http_script")
        if sql_http_script is None:
            sql_http_script = os.path.join(os.path.dirname(__file__), 'cmd_mysql.php')
        cmd_string = 'php ' + sql_http_script + ' "(file)=' + file + '" "(text)=' + selected_text + '"'
        if (count_cursors > 1):
            # Выводим ошибку - множественный курсор
            cmd_string = 'php "' + sql_http_script + '" "(file)=' + file + '" "(mode)=error" "(error)=Multiple selection is not supported !!!"'
            sublime.active_window().active_view().window().run_command("exec", {
                'shell': True,
                'cmd': cmd_string
            })
        elif (count_cursors == 1 and re.match(r'^[a-zA-Z-][a-zA-Z0-9_-]{1,80}$', selected_text)):
            # Выделенный текст записываем в отдельный файл и выполняем
            # file_buffer = MyBuildCurrentCodeCommand.get_file_buffer(file, selected_text)
            cmd_string = 'php "' + sql_http_script + '" "(file)=' + file + '" "(mode)=db_help" "(db_help)=' + selected_text + '"'
            sublime.active_window().active_view().window().run_command("exec", {
                'shell': True,
                'cmd': cmd_string
            })
        elif (count_cursors == 1 and len(selected_text)>0):
            if re.match(r'^[a-zA-Z][a-zA-Z0-9_]{4,80}$', selected_text):
                print('yes')
            # Выделенный текст записываем в отдельный файл и выполняем
            file_buffer = MyBuildCurrentCodeCommand.get_file_buffer(file, selected_text)
            cmd_string = 'php "' + sql_http_script + '" "(file)=' + file_buffer + '" "(mode)=buffer"'
            sublime.active_window().active_view().window().run_command("exec", {
                'shell': True,
                'cmd': cmd_string
            })
        else:
            # Выполнение скрипта в обычном режиме
            cmd_string = 'php "' + sql_http_script + '" "(file)=' + file + '" "(mode)=file"'
            sublime.active_window().active_view().window().run_command("exec", {
                'shell': True,
                'cmd': cmd_string
            })
        return

# { "keys": ["ctrl+shift+f5"], "command": "my_build_php_cs_fixer" },
class MyBuildPhpCsFixerCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        file_name = sublime.active_window().active_view().file_name()
        if (MyBuildPhpCsFixerCommand.is_maskfile_valid(file_name, '.php')):
            MyBuildPhpCsFixerCommand.run_php_cs_fixer(file_name)
    def is_maskfile_valid(file, mask):
        a = file.lower().split(mask.lower())
        l = len(a)
        if (l > 0 and a[l-1] == ''):
            return True
        else:
            return False
    def run_php_cs_fixer(file):
        sublime.active_window().active_view().window().run_command("save")
        settings = sublime.load_settings("Preferences.sublime-settings")
        php_cs_fixer = settings.get("my_builder_php_cs_fixer")
        if php_cs_fixer is None:
            cmd_string = 'php ' + os.path.join(os.path.dirname(__file__), 'cmd_php_cs_fixer.php') + ' "(message)=Параметры не настроены!"'
        elif os.path.isfile(php_cs_fixer):
            cmd_string = 'php ' + php_cs_fixer + ' fix ' + file + ' --level=psr2'
        else:
            cmd_string = 'php ' + os.path.join(os.path.dirname(__file__), 'cmd_php_cs_fixer.php') + ' "(message)='+php_cs_fixer+'"'
        sublime.active_window().active_view().window().run_command("exec", {
            'shell': True,
            'cmd': cmd_string
        })
