
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
        if isinstance(value, dict) and not isinstance(value, _NestedDict):
            value = _NestedDict(value, _parent=self, _key=key, _root=self._root, _skip_save=self._skip_save)
        dict.__setitem__(self, key, value)
        if not self._skip_save:
            self._save_root()
    
    def get(self, key, default=None):
        """Get a value by key, returning default if key is not present"""
        if key in self:
            return self[key]
        return default
    
    def set(self, key, value):
        """Set a value for the given key"""
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

class FuckReplitDB:
    def __init__(self, filename="database.json"):
        self.filename = filename
        self.lock = threading.RLock()
        self.store = None  # Initialize store attribute
        self._loading = True  # Flag to prevent saving during loading
        self._load()
        self._loading = False  # Reset flag after loading is complete
        
    def _load(self):
        with self.lock:
            if os.path.exists(self.filename):
                try:
                    with open(self.filename, 'rb') as f:
                        data = orjson.loads(f.read())
                        self.store = self._to_nested(data)
                except (orjson.JSONDecodeError, FileNotFoundError):
                    # Handle corrupt or missing JSON
                    self.store = _NestedDict(_root=self, _skip_save=True)
            else:
                self.store = _NestedDict(_root=self, _skip_save=True)
            
            # After loading is complete, allow future saves
            if self.store is not None:
                self._enable_saves_recursively(self.store)
                
    def _enable_saves_recursively(self, nested_dict):
        """Enable saving on the loaded structure after initialization"""
        if isinstance(nested_dict, _NestedDict):
            nested_dict._skip_save = False
            for value in nested_dict.values():
                if isinstance(value, _NestedDict):
                    self._enable_saves_recursively(value)
                
    def _save(self):
        if self._loading:
            return  # Skip saving during loading process
            
        with self.lock:
            if self.store is None:
                return  # Avoid saving if store isn't initialized
                
            dir_name = os.path.dirname(self.filename)
            if dir_name and not os.path.exists(dir_name):
                os.makedirs(dir_name)
                
            with tempfile.NamedTemporaryFile('wb', dir=dir_name or '.', delete=False) as tmp_file:
                # orjson.dumps returns bytes, not string
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
        result = _NestedDict(_root=self, _skip_save=True)  # Skip saves during initialization
        for k, v in d.items():
            result[k] = self._to_nested(v) if isinstance(v, dict) else v
        return result

    def get(self, key, default=None):
        """Get a value by key, returning default if key is not present"""
        with self.lock:
            if self.store is None:
                return default
            if key in self.store:
                return self.store[key]
            return default
    
    def set(self, key, value):
        """Set a value for the given key"""
        with self.lock:
            if self.store is None:
                self.store = _NestedDict(_root=self)
            self.store[key] = value
            self._save()
            return value
        
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



        
