


import orjson
import os
import threading
import tempfile

class _NestedDict(dict):
    def __init__(self, *args, **kwargs):
        self._parent = kwargs.pop('_parent', None)
        self._key = kwargs.pop('_key', None)
        self._root = kwargs.pop('_root', None)
        self._skip_save = kwargs.pop('_skip_save', False)
        dict.__init__(self, *args, **kwargs)
        
    def __getitem__(self, key):
        if key not in self:
            self[key] = _NestedDict(_parent=self, _key=key, _root=self._root, _skip_save=self._skip_save)
        return dict.__getitem__(self, key)
        
    def __setitem__(self, key, value):
        key = str(key)
        if isinstance(value, dict) and not isinstance(value, _NestedDict):
            value = _NestedDict(value, _parent=self, _key=key, _root=self._root, _skip_save=self._skip_save)
        dict.__setitem__(self, key, value)
        if not self._skip_save:
            self._save_root()

    
    def get(self, key, default=None):
        if key in self:
            return self[key]
        return default
    
    def set(self, key, value):
        self[key] = value
        return value
        
    def _save_root(self):
        if self._skip_save:
            return
        if self._root is not None:
            self._root._save()
        elif self._parent is not None:
            self._parent._save_root()
            
    def to_dict(self):
        result = {}
        for k, v in self.items():
            if isinstance(v, _NestedDict):
                result[k] = v.to_dict()
            else:
                result[k] = v
        return result
        
    def keys(self):
        return dict.keys(self)
        
    def values(self):
        return dict.values(self)
        
    def items(self):
        return dict.items(self)
        
    def __iter__(self):
        return dict.__iter__(self)
        
    def __delitem__(self, key):
        dict.__delitem__(self, key)
        if not self._skip_save:
            self._save_root()


class FuckReplitDB:
    def __init__(self, filename="database.json"):
        self.filename = filename
        self.lock = threading.RLock()
        self.store = None
        self._loading = True
        self._load()
        self._loading = False
        
    def _load(self):
        with self.lock:
            if os.path.exists(self.filename):
                try:
                    with open(self.filename, 'rb') as f:
                        data = orjson.loads(f.read())
                        self.store = self._to_nested(data)
                except (orjson.JSONDecodeError, FileNotFoundError):
                    self.store = _NestedDict(_root=self, _skip_save=True)
            else:
                self.store = _NestedDict(_root=self, _skip_save=True)

            if self.store is not None:
                self._enable_saves_recursively(self.store)
                
    def _enable_saves_recursively(self, nested_dict):
        if isinstance(nested_dict, _NestedDict):
            nested_dict._skip_save = False
            for value in nested_dict.values():
                if isinstance(value, _NestedDict):
                    self._enable_saves_recursively(value)
                
    def _save(self):
        if self._loading:
            return
            
        with self.lock:
            if self.store is None:
                return
                
            dir_name = os.path.dirname(self.filename)
            if dir_name and not os.path.exists(dir_name):
                os.makedirs(dir_name)
                
            with tempfile.NamedTemporaryFile('wb', dir=dir_name or '.', delete=False) as tmp_file:
                json_bytes = orjson.dumps(
                    self.store.to_dict(),
                    option=orjson.OPT_INDENT_2 | orjson.OPT_SORT_KEYS
                )
                tmp_file.write(json_bytes)
                temp_name = tmp_file.name
            os.replace(temp_name, self.filename)
            
    def _to_nested(self, d):
        if not isinstance(d, dict):
            return d
        result = _NestedDict(_root=self, _skip_save=True)
        for k, v in d.items():
            k = str(k)
            result[k] = self._to_nested(v) if isinstance(v, dict) else v
        return result

    def get(self, key, default=None):
        with self.lock:
            if self.store is None:
                return default
            if key in self.store:
                return self.store[key]
            return default
    
    def set(self, key, value):
        with self.lock:
            if self.store is None:
                self.store = _NestedDict(_root=self)
            self.store[key] = value
            self._save()
            return value
            
    def __iter__(self):
        with self.lock:
            if self.store is None:
                return iter([])
            return iter(self.store)
        
    def __getitem__(self, key):
        with self.lock:
            if self.store is None:
                raise KeyError(f"Key '{key}' not found - database not loaded")
            return self.store[key]
            
    def __setitem__(self, key, value):
        with self.lock:
            if self.store is None:
                self.store = _NestedDict(_root=self)
            self.store[key] = value
            self._save()
            
    def __delitem__(self, key):
        with self.lock:
            if self.store is None:
                raise KeyError(f"Key '{key}' not found - database not loaded")
            del self.store[key]
            self._save()
            
    def __contains__(self, key):
        with self.lock:
            if self.store is None:
                return False
            return key in self.store
            
    def keys(self):
        with self.lock:
            if self.store is None:
                return []
            return self.store.keys()
            
    def values(self):
        with self.lock:
            if self.store is None:
                return []
            return self.store.values()
            
    def items(self):
        with self.lock:
            if self.store is None:
                return []
            return self.store.items()



        





