###Товарищ, используй спец.инструмент!
Инструмент для создания структуры проекта и его сборки с шифрованием для [mambalb.dll](https://github.com/CarbisCrew/mamba_library) <br>

Пакет опубликован на pypi, так что пользоваться им должно быть супер-удобно.

####Установка
Открой cmd или PS, как тебе больше нравится, друг!
Установи пакет mamba_toolbox через pip (ТОЛЬКО НЕ УСТАНАВЛИВАЙ ЕГО В VIRTUALENV)
>pip install mamba_toolbox

Теперь открой папку с будущим проектом и делай так:
>mamba new {имя_проекта}

**Имя проекта не должно содержать кирилицы, пробелов и спец.символов!**

После окончания процедуры в папке появится следующая структура:
```
.git/
project_name/
	__main__.py
venv/
.gitignore
mamconf.json
run.py
```

`run.py` - основной файл для отладки. Пропиши его в твой launch.json


`__main__.py` - Файл, который должен содержать точку входа в твое ПО - функцию **start**<br>
В функции start обязательно должно быть обработано исключение **KeyboardInterrupt**

Содержимое файла по-умолчанию:
```python
# -*- encoding=utf-8 -*-
# This file was generated automatically

__version__ = (0, 0, 0, 0)

def start():
    try:
        print("{name} v"+".".join(map(str, __version__)))
        # YOUR CODE HERE
        pass
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    start()
                
```

`mamconf.json` - файл с конфигом для сборщика
Содержимое по-умолчанию:
```json
{
  "project_name": "project_name",
  "crypt_key": "c82e457d814628f34284d732fc5cd5ea",
  "dev_dependencies": [
    "wheel", 
    "pip"
  ],
  "builder": {
    "dist_name": "project_name",
    "tocopy": [],
    "pythonversion": 3.7.9,
    "build_folder": "./build",
    "distribution_folder": "./dist",
    "dependencies_from_requirements_txt": false
  }
}
```

`project_name` - имя твоего проекта<br>
`crypt_key` - автоматически сгенеренный ключ шифрования, с котором будет выполняться сборка твоего проекта<br>
**Эти два параметра пригодятся тебе когда ты будешь делать exe для mambalib.dll**

`dev_dependencies` - `list<str>` - список зависимостей, не включаемых в сборку проекта<br>
`builder` - доп.конфиг для сборки<br>
`dist_name` - название дистрибутива, с ним будет создан архив<br>
`tocopy` - `list<str>` - список относительных и абсолютных путей до папок и файлов, которые должны быть дополнительно скопированы в сборку ПО<br>
`pythonversion` - версия python, для которой писался проект<br>
`build_folder` - относительный путь к папке, где будет сформирован билд проекта<br>
`distribution_folder` - относительный путь до папки, где будет собранный архив с ПО<br>
`dependencies_from_requirements_txt` - флаг, который указывает сборщику устанавливать зависимости из файла requirements.txt (по дефолту - устанавливаются из venv). <b>Файл requirements.txt должен быть в кодировке utf-8<b/>
