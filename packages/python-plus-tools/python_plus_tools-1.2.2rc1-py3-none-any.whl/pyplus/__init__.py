'''
The python Plus - Pyplus
================
the python's plus library.\n
'''

from os import makedirs, getenv
from pathlib import Path
from site import getsitepackages

from . import tools, science
from toml import load,dump

global_config_path = Path(getenv("appdata"),"xystudio", "pyplus", "config.toml")
local_config_path = Path(".xystudio", "pyplus", "config.toml").absolute()
global_config = {}
local_config = {}
union_config = {}

LOCAL = "local"
GLOBAL = "global"

ALL = "all"
NEW = "news"
WILL = "will"

makedirs(global_config_path.parent, exist_ok=True)

if not global_config_path.exists():
    global_config_path.touch()
else:
    with open(global_config_path, 'r', encoding="utf-8") as f:
        global_config = load(f)

if global_config["library"].get("library", {"autoCreateLocalConfig" : True})["autoCreateLocalConfig"]:
    makedirs(local_config_path.parent, exist_ok=True)
    if not(local_config_path.exists()):
        local_config_path.touch()

try:
    with open(local_config_path, 'r', encoding="utf-8") as f:
        local_config = load(f)
except FileNotFoundError:
    pass

first_used_config = global_config.get("library", {"firstUsedConfig" : "local"})['firstUsedConfig']

if first_used_config == "local":
    union_config = global_config | local_config
else:
    union_config = local_config | global_config

if union_config.get("library", {"showDeprecationWarning":True})['showDeprecationWarning']:
    from warnings import warn
    print(f"{tools.colors.Fore.MAGENTA}{tools.colors.Style.BRIGHT}note:write 'pyplus.config('library.showDeprecationWarning', 'false')' and run code again to close this warning.")

__all__=[
    "science" ,"tools",
    "VERSION","UPDATE_DOC", "UPDATE_TIME", "PRE_VERSION", "PRE_UPDATE_DOC", "PRE_UPDATE_TIME",
    "ALL", "NEW", "WILL", 
    "get_update", "get_version_update_time", "get_version", "get_pre_version", "get_news_update_time", "get_new", "get_all", "get_will", "get_pre_update", "get_pre_version_update_time", "get_pre_news_update_time", "get_pre_new", "get_pre_all", 
    "config"
]

with open(getsitepackages()[1]+"\\pyplus\\config\\update.toml", "r", encoding="utf-8") as f:
    updates = load(f)

def get_update(namespace:str, version: str): 
    '''get the version update doc.'''
    try:
        open_dict = updates['release'][namespace]['update_info']
    except KeyError:
        raise ValueError('This namespace not found.')

    if version == ALL: 
        out_obj = open_dict
    elif version == NEW: 
        out_obj = open_dict.get(updates['release'][namespace]['version'], "This version is not found. Maybe it is not recorded.")
    elif version == WILL: 
        out_obj = open_dict.get(WILL, "This version is not found. Maybe it is not recorded.")
    else: 
        out_obj = open_dict.get(str(version), "This version is not found. Maybe it is not recorded.")
    
    print(out_obj)
    return out_obj

def get_version_update_time(namespace:str, version: str): 
    '''Get the version update time.'''
    try:
        open_dict = updates['release'][namespace]['update_time']
    except KeyError:
        raise ValueError('This namespace not found.')

    if version == ALL: 
        out_obj = open_dict
    elif version == NEW: 
        out_obj = open_dict.get(updates['release'][namespace]['version'], "This version is not found. Maybe it is not recorded.")
    elif version == WILL: 
        raise ValueError('`get_version_update_time` cannot get will update time.')
    else: 
        out_obj = open_dict.get(str(version), "This version is not found. Maybe it is not recorded.")
    
    print(out_obj)
    return out_obj

def get_will(namespace:str): 
    '''Get the will update doc.'''
    return get_update(namespace, WILL)

def get_version(namespace:str):
    '''Get the version.'''
    return updates['release'][namespace]['version']

def get_pre_version():
    '''Get the pre version.'''
    return updates['pre-release']['version']

def get_news_update_time(namespace:str): 
    '''Get the new update time.'''
    return get_version_update_time(namespace, NEW)

def get_new(namespace:str): 
    '''Get the new update doc.'''
    return get_update(namespace, NEW)

def get_all(namespace:str): 
    '''Get the all update doc.'''
    return get_update(namespace, ALL)

def get_will(namespace:str): 
    '''Get the will update doc.'''
    return get_update(namespace, WILL)

def get_pre_update(version: str): 
    '''Get the pre-release version update doc.'''
    try:
        open_dict = updates['pre-release']['update_info']
    except KeyError:
        raise ValueError('This namespace not found.')

    if version == ALL: 
        out_obj = open_dict
    elif version == NEW: 
        out_obj = open_dict.get(updates['pre-release']['version'], "This version is not found. Maybe it is not recorded.")
    elif version == WILL: 
        out_obj = open_dict.get(WILL, "This version is not found. Maybe it is not recorded.")
    else: 
        out_obj = open_dict.get(str(version), "This version is not found. Maybe it is not recorded.")

    print(out_obj)
    return out_obj

def get_pre_version_update_time(version: str): 
    '''Get the pre-release version update time.'''
    try:
        open_dict = updates['pre-release']['update_time']
    except KeyError:
        raise ValueError('This namespace not found.')

    if version == NEW: 
        out_obj = open_dict
    elif version == NEW: 
        out_obj = open_dict.get(updates['pre-release']['version'], "This version is not found. Maybe it is not recorded.")
    elif version == WILL: 
        raise ValueError('`get_version_update_time` cannot get will update time.')
    else: 
        out_obj = open_dict.get(str(version), "This version is not found. Maybe it is not recorded.")
    print(out_obj)
    return out_obj

def get_pre_news_update_time(): 
    '''Get the new update time.'''
    return get_pre_version_update_time(NEW)

def get_pre_new(): 
    '''Get the new pre-release update doc.'''
    return get_pre_update(NEW)

def get_pre_all(): 
    '''Get the all pre-release update doc.'''
    return get_pre_update(ALL)

def open_doc(doc_name:str):
    raise NotImplementedError("Document is not completed.")

def config(config_name:str, value:object, config_type = first_used_config, not_reset_config:bool = True):
    global local_config,global_config

    config_name = config_name

    if config_type == LOCAL:
        makedirs(local_config_path.parent, exist_ok=True)
        if not(local_config_path.exists()):
            local_config_path.touch()

        config_split = config_name.split(".", 1)
        config_char_1 = config_split[0]
        try:
            config_char_2 = config_split[1]
        except IndexError:
            raise ValueError("config name must use 'a.b'.")

        with open(local_config_path, "w+", encoding="utf-8") as f:
            config = load(f) | {config_char_1 : {config_char_2 : value}}
            dump(config, f)
    elif config_type == GLOBAL:
        config_split = config_name.split(".")
        config_char_1 = config_split[0]
        try:
            config_char_2 = config_split[1]
        except IndexError:
            raise ValueError("config name must use 'a.b'.")

        with open(global_config_path, "w+", encoding="utf-8") as f:
            config = load(f) | {config_char_1 : {config_char_2 : value}}
            dump(config, f)
    else:
        raise ValueError("This config type not found.")

def get_config(config_name:str):
    try:
        config_split = config_name.split(".")
        config_char_1 = config_split[0]
        try:
            config_char_2 = config_split[1]
            return union_config[config_char_1][config_char_2]
        except IndexError:
            raise ValueError("config name must use two texts, example : 'a.b'.")
    except KeyError:
        return None

__version__ = get_version("main")

del getsitepackages, Path, getenv