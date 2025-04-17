

import orjson
import os
import threading
from typing import Dict, Any, Iterator

class NestedDict:
    def __init__(self, parent, key_path):
        self.parent = parent
        self.key_path = key_path
    
    def __getitem__(self, key):
        new_path = self.key_path + [key]
        
        with self.parent.lock:
            try:
                with open(self.parent.filename, 'rb') as f:
                    data = orjson.loads(f.read())
                
                current = data
                for k in self.key_path:
                    current = current[k]
                
                value = current[key]
                if isinstance(value, dict):
                    return NestedDict(self.parent, new_path)
                return value
            except (KeyError, ValueError, FileNotFoundError):
                raise KeyError(key)
    
    def __setitem__(self, key, value):
        new_path = self.key_path + [key]
        
        with self.parent.lock:
            try:
                with open(self.parent.filename, 'rb') as f:
                    data = orjson.loads(f.read())
            except (ValueError, FileNotFoundError):
                data = {}
            
            current = data
            for k in self.key_path:
                if k not in current:
                    current[k] = {}
                current = current[k]
            
            current[key] = value
            
            with open(self.parent.filename, 'wb') as f:
                f.write(orjson.dumps(data, option=orjson.OPT_INDENT_2))
    
    def __contains__(self, key):
        with self.parent.lock:
            try:
                with open(self.parent.filename, 'rb') as f:
                    data = orjson.loads(f.read())
                
                current = data
                for k in self.key_path:
                    current = current[k]
                
                return key in current
            except (KeyError, ValueError, FileNotFoundError):
                return False
                
    def __delitem__(self, key):
        with self.parent.lock:
            try:
                with open(self.parent.filename, 'rb') as f:
                    data = orjson.loads(f.read())
                
                current = data
                for k in self.key_path:
                    current = current[k]
                
                if key in current:
                    del current[key]
                    
                    with open(self.parent.filename, 'wb') as f:
                        f.write(orjson.dumps(data, option=orjson.OPT_INDENT_2))
                else:
                    raise KeyError(key)
            except (KeyError, ValueError, FileNotFoundError):
                raise KeyError(key)

class FuckReplitDB:
    def __init__(self, filename):
        self.filename = filename
        self.lock = threading.Lock()
        
        if not os.path.exists(filename):
            with open(filename, 'wb') as f:
                f.write(orjson.dumps({}))
    
    def get(self, key, default=None):
        with self.lock:
            try:
                with open(self.filename, 'rb') as f:
                    data = orjson.loads(f.read())
                return data.get(key, default)
            except (ValueError, FileNotFoundError):
                return default
    
    def set(self, key, value):
        with self.lock:
            try:
                with open(self.filename, 'rb') as f:
                    data = orjson.loads(f.read())
            except (ValueError, FileNotFoundError):
                data = {}
            
            data[key] = value
            
            with open(self.filename, 'wb') as f:
                f.write(orjson.dumps(data, option=orjson.OPT_INDENT_2))
    
    def delete(self, key):
        with self.lock:
            try:
                with open(self.filename, 'rb') as f:
                    data = orjson.loads(f.read())
                
                if key in data:
                    del data[key]
                    
                    with open(self.filename, 'wb') as f:
                        f.write(orjson.dumps(data, option=orjson.OPT_INDENT_2))
            except (ValueError, FileNotFoundError):
                pass
    
    def items(self):
        with self.lock:
            try:
                with open(self.filename, 'rb') as f:
                    data = orjson.loads(f.read())
                return data.items()
            except (ValueError, FileNotFoundError):
                return {}
    
    def keys(self):
        with self.lock:
            try:
                with open(self.filename, 'rb') as f:
                    data = orjson.loads(f.read())
                return data.keys()
            except (ValueError, FileNotFoundError):
                return []
    
    def __contains__(self, key):
        with self.lock:
            try:
                with open(self.filename, 'rb') as f:
                    data = orjson.loads(f.read())
                return key in data
            except (ValueError, FileNotFoundError):
                return False
    
    def __getitem__(self, key):
        with self.lock:
            try:
                with open(self.filename, 'rb') as f:
                    data = orjson.loads(f.read())
                
                value = data[key]
                if isinstance(value, dict):
                    return NestedDict(self, [key])
                return value
            except (KeyError, ValueError, FileNotFoundError):
                raise KeyError(key)
    
    def __setitem__(self, key, value):
        self.set(key, value)
        
    def __delitem__(self, key):
        with self.lock:
            try:
                with open(self.filename, 'rb') as f:
                    data = orjson.loads(f.read())
                
                if key in data:
                    del data[key]
                    
                    with open(self.filename, 'wb') as f:
                        f.write(orjson.dumps(data, option=orjson.OPT_INDENT_2))
                else:
                    raise KeyError(key)
            except (ValueError, FileNotFoundError):
                raise KeyError(key)
    
    def __iter__(self) -> Iterator:
        with self.lock:
            try:
                with open(self.filename, 'rb') as f:
                    data = orjson.loads(f.read())
                return iter(data)
            except (ValueError, FileNotFoundError):
                return iter([])
                
                
                


                
