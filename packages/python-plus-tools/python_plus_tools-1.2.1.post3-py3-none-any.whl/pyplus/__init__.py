'''
The python Plus - Pyplus
================
the python's plus library.\n
'''

from site import getsitepackages
from toml import load,dump
from pathlib import Path
import os

global_config_path = Path(os.getenv("appdata"),"xystudio", "pyplus", "config.toml")
local_config_path = Path(".xystudio", "pyplus", "config.toml").resolve()
global_config = {}
local_config = {}
union_config = {}

os.makedirs(global_config_path.parent, exist_ok=True)

if not global_config_path.exists():
    global_config_path.touch()
else:
    with open(global_config_path, 'r', encoding="utf-8") as f:
        global_config = load(f)

_temp = True
try:
    if global_config["library"].get("autoCreateLocalConfig", "true") == "false":
        _temp = False
except KeyError:
    pass

if _temp:
    os.makedirs(local_config_path.parent, exist_ok=True)
    if not(local_config_path.exists()):
        local_config_path.touch()

try:
    with open(local_config_path, 'r', encoding="utf-8") as f:
        local_config = load(f)
except FileNotFoundError:
    pass

_temp = True
try:
    print(global_config,global_config["library"]["firstUsedConfig"])
    if global_config["library"].get("firstUsedConfig", "local") == "global":
        _temp = False
except KeyError:
    pass

if _temp:
    union_config = global_config | local_config
else:
    union_config = local_config | global_config

try:
    with open(local_config_path, 'r', encoding="utf-8") as f:
        local_config = load(f)
except FileNotFoundError:
    pass

_temp = True
try:
    if union_config["library"].get("showDeprecationWarning", "true") == "false":
        _temp = False
except KeyError:
    pass

from . import science ,tools

if _temp:
    print(f"{tools.colors.Fore.MAGENTA}{tools.colors.Style.BRIGHT}note:write 'pyplus.config('library.showDeprecationWarning', 'false')' and run code again to close this warning.")

__all__=[
    "science" ,"tools",
    "VERSION","UPDATE_DOC", "UPDATE_TIME", "PRE_VERSION", "PRE_UPDATE_DOC", "PRE_UPDATE_TIME",
    "ALL", "NEW", "WILL", 
    "get_update", "get_version_update_time", "get_version", "get_pre_version", "get_news_update_time", "get_new", "get_all", "get_will", "get_pre_update", "get_pre_version_update_time", "get_pre_news_update_time", "get_pre_new", "get_pre_all", 
    "config"
]

with open(getsitepackages()[1]+"\\pyplus\\update.toml", "r", encoding="utf-8") as f:
    updates = load(f)

LOCAL = "local"
GLOBAL = "global"

ALL = "all"
NEW = "news"
WILL = "will"

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

try:
    first_used_config = global_config["library"].get("firstUsedConfig", "local")
except KeyError:
    first_used_config = "local"

def config(config_name:str, value:object, config_type = first_used_config):
    global local_config,global_config

    config_name = config_name

    if config_type == LOCAL:
        os.makedirs(local_config_path.parent, exist_ok=True)
        if not(local_config_path.exists()):
            local_config_path.touch()

        config_split = config_name.split(".")
        config_char_1 = config_split[0]
        try:
            config_char_2 = config_split[1]
            local_config[config_char_1] = {config_char_2:value}
        except IndexError:
            local_config[config_char_1] = value

        with open(local_config_path, "w", encoding="utf-8") as f:
            dump(local_config, f)
    elif config_type == GLOBAL:
        config_split = config_name.split(".")
        config_char_1 = config_split[0]
        try:
            config_char_2 = config_split[1]
            global_config[config_char_1] = {config_char_2:value}
        except IndexError:
            global_config[config_char_1] = value
        with open(global_config_path, "w", encoding="utf-8") as f:
            dump(global_config, f)
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
            return union_config[config_char_1]
    except KeyError:
        return None

__version__ = get_version("main")