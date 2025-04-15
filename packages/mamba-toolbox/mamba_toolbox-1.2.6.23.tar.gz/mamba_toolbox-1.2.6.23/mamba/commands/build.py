from os.path import relpath
import click
import shutil
import os
import json
import hashlib
from json import JSONDecodeError
from ..tools import download_from_url, progressBar, unzip, zipdir, pip_install, checkout
import re

def get_config():
    try:
        return json.loads(open(os.path.join(os.getcwd(), 'mamconf.json')).read())
    except FileNotFoundError as e:
        print('Fatal: Mamba build configuration not found: '+str(e))
    except JSONDecodeError as e:
        print('Fatal: Unnable to parse json config: '+str(e))
    
    exit()

def rc4_encrypt(data, key):
    x = 0
    box = list(range(256))
    for i in range(256):
        x = (x + box[i] + ord(key[i % len(key)])) % 256
        box[i], box[x] = box[x], box[i]
    x = 0
    y = 0
    out = []
    for char in data:
        x = (x + 1) % 256
        y = (y + box[x]) % 256
        box[x], box[y] = box[y], box[x]
        out.append((ord(char)  ^ box[(box[x] + box[y]) % 256]).to_bytes(2, byteorder='big'))
    return b''.join(out)
   

@click.command('build')
def build_package():
    config: dict = get_config()
    PROJECT_NAME = config['project_name']
    checkout(PROJECT_NAME)
    CWD = os.getcwd()
    DEV_DEPS = config['dev_dependencies']
    SRC_PROJECT_FOLDER = os.path.join(CWD, PROJECT_NAME)
    KEY = hashlib.md5(config['crypt_key'].encode()).hexdigest().upper()
    TOCOPY = config['builder']['tocopy']
    BUILD_HERE = os.path.abspath(config['builder']['build_folder'])
    TMP_FOLDER = os.path.join(BUILD_HERE, "__TMP__")
    PYTHON_FOLDER = os.path.join(BUILD_HERE, 'python')
    DST_PROJECT_FOLDER = os.path.join(BUILD_HERE, PROJECT_NAME)
    DIST_HERE = os.path.abspath(config['builder']['distribution_folder'])
    EXT = '.mb'
    DEPS_FROM_REQUIREMENTS = config['builder'].get("dependencies_from_requirements_txt", False)
    
    print('Checking folders...')
    if not os.path.exists(SRC_PROJECT_FOLDER):
        print('Fatal: src project folder "{}" not found.'.format(SRC_PROJECT_FOLDER))
        exit()
    print('SRC project folder OK')

    os.makedirs(DST_PROJECT_FOLDER, exist_ok=True)
    print('DST project folder OK')
    os.makedirs(TMP_FOLDER, exist_ok=True)
    print('TMP project folder OK')
    os.makedirs(DIST_HERE, exist_ok=True)
    print('Distribution folder project folder OK')

    print('Preparing python')
    if os.path.exists(PYTHON_FOLDER):
        print('Python found. Skipping.')
    else:
        os.makedirs(PYTHON_FOLDER, exist_ok=True)
        zipname = f'python-{config["builder"]["pythonversion"]}-embed-win32.zip'
        python_url = f'https://www.python.org/ftp/python/{config["builder"]["pythonversion"]}/{zipname}'
        zippath = os.path.join(TMP_FOLDER, zipname)
        
        download_from_url(python_url, zippath)
        unzip(zippath, PYTHON_FOLDER)
    shutil.rmtree(TMP_FOLDER, onerror=lambda _,_1,_2: None)

    shutil.copyfile(os.path.join(PYTHON_FOLDER, 'vcruntime140.dll'), os.path.join(BUILD_HERE, 'vcruntime140.dll'))
    shutil.copyfile(os.path.join(PYTHON_FOLDER, 'sqlite3.dll'), os.path.join(BUILD_HERE, 'sqlite3.dll'))

    
    # copy "tocopy"

    for route in TOCOPY:
        if os.path.isfile(route):
            os.makedirs(os.path.dirname(os.path.join(BUILD_HERE, route)), exist_ok=True)
            print('Copying file {}'.format(route))
            shutil.copyfile(os.path.abspath(route), os.path.join(BUILD_HERE, route))
        elif route.startswith('http://') or route.startswith('https://'):
            download_from_url(route, os.path.join(BUILD_HERE, os.path.basename(route)))
        else:
            os.makedirs(os.path.join(BUILD_HERE, route), exist_ok=True)
            print('Copying tree {}'.format(route))
            shutil.rmtree(os.path.join(BUILD_HERE, route))
            shutil.copytree(os.path.abspath(route), os.path.join(BUILD_HERE, route))

    for root, _, file_list in os.walk(SRC_PROJECT_FOLDER):
        for file_item in file_list:
            if root.find('__pycache__') >= 0:
                continue
            src = os.path.join(root, file_item)
            dst = os.path.join(BUILD_HERE, os.path.relpath(root), file_item)
            
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            if (file_item.split('.')[-1] != "py"):
                print('Copying {}'.format(src))
                shutil.copyfile(src, dst)
            else:
                print('Encrypting {}'.format(file_item))
                with open(src, 'r', encoding='utf-8') as py:
                    with open(dst.replace('.py', EXT), 'wb+') as mb:
                        mb.write(rc4_encrypt(py.read(), KEY))
                        # mb.write(py.read().encode())

    # getting venv dependencies
    deplist = list()
    if not DEPS_FROM_REQUIREMENTS:
        for root, dirs, __ in os.walk(os.path.join(CWD, 'venv', 'Lib', 'site-packages')):
            for dir in dirs:
                if dir.endswith('.dist-info'):
                    dep = dir.replace('.dist-info','')
                    dep_version = dep.split('-')[-1]
                    dep_name = dep.replace('-{}'.format(dep_version), '')
                    if dep_name in DEV_DEPS:
                        continue
                    deplist.append('{}=={}'.format(dep_name, dep_version))
            break
    else:
        with open("./requirements.txt", "r", encoding='utf-8') as file:
            for line in file:
                deplist.append(line.strip())

    print('This dependencies were found:\n\r', *[dep+'\n\r' for dep in deplist])
    print('installing... (it may take a while)')
    # for i, dep in enumerate(deplist):
    #     progressBar(i+1, len(deplist))
    #     pip_install(PYTHON_FOLDER, dep)
    pip_install(PYTHON_FOLDER, ' '.join(deplist))
    print('')
        
        
    print('All requirements has been installed. Clearing a folder')
    for root, dirs, __ in os.walk(PYTHON_FOLDER):
        for dir in dirs:
            if dir.endswith('.dist-info'):
                print('Removing', dir)
                shutil.rmtree(os.path.join(root, dir))
        break

    with open(os.path.join(BUILD_HERE, '.depfile'), 'w+') as f:
        for dep in deplist:
            f.write(dep+'\r')
        f.close()  


    # getting appversion

    mainfile = open(os.path.join(SRC_PROJECT_FOLDER, '__init__.py'), 'r', encoding='utf-8').read()
    
    appversion = re.search(r'__version__\s*=\s*\(\s*(\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*\d+)\s*\)', mainfile)
    if appversion is None:
        print("Build finished, but I can't find __version__ in your main __init__. ")
        print("Make sure it exists, and it's a tuple containng at least two integers")
        exit()
    
    appversion = [v.strip() for v in appversion.group(1).split(',')]

    app_zip_name = f'{config["builder"].get("dist_name",PROJECT_NAME).lower().replace(" ", "_")}_v{".".join(map(str, appversion))}.zip'
    zipdir(os.path.join(DIST_HERE,app_zip_name), BUILD_HERE)

    print('Build finished!')

    



