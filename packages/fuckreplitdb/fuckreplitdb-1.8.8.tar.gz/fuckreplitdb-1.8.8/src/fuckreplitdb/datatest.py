
import time
import threading
from __init__ import FuckReplitDB

# Define the filename for the database
filename = "test_db.json"

# Create an instance of FuckReplitDB
db = FuckReplitDB(filename)

# Test basic set and get operations
print("Setting key 'name' to 'Alice'...")
db.set('name', 'Alice')

print("Getting 'name'...")
print(db.get('name'))  # Expected output: Alice

# Test nested data with NestedDict
print("\nSetting nested data...")
db['user'] = {'first_name': 'John', 'last_name': 'Doe'}

print("Getting nested data 'user.first_name'...")
print(db['user']['first_name'])  # Expected output: John

# Test adding a nested dictionary and retrieving its items
print("\nAdding more nested data...")
db['user']['address'] = {'street': '123 Elm St', 'city': 'Somewhere'}
print("Getting nested data 'user.address'...")
print(db['user']['address'])  # Expected output: {'street': '123 Elm St', 'city': 'Somewhere'}

# Test checking if a nested key exists
print("\nChecking if 'user' exists...")
print('user' in db)  # Expected output: True

print("Checking if 'user.address' exists...")
print('address' in db['user'])  # Expected output: True

# Test deleting nested data
print("\nDeleting 'user.address'...")
del db['user']['address']

print("Checking if 'user.address' exists after deletion...")
print('address' in db['user'])  # Expected output: False

# Test iterating over nested keys and items
print("\nIterating over top-level keys...")
for key in db.keys():
    print(key)  # Expected output: 'name' and 'user'

print("Iterating over nested 'user' keys...")
for key in db['user'].keys():
    print(key)  # Expected output: 'first_name', 'last_name'

# Test updating nested data
print("\nUpdating 'user.first_name'...")
db['user']['first_name'] = 'Jane'

print("Getting updated 'user.first_name'...")
print(db['user']['first_name'])  # Expected output: Jane

# Test writing and reading different data types in nested data
print("\nSetting different types of nested data...")
db['user']['age'] = 30
db['user']['is_active'] = True
db['user']['preferences'] = {'theme': 'dark', 'notifications': True}

print("Getting different types of nested data...")
print(db['user']['age'])  # Expected output: 30
print(db['user']['is_active'])  # Expected output: True
print(db['user']['preferences'])  # Expected output: {'theme': 'dark', 'notifications': True}

# Test non-existent nested key access
print("\nTrying to get a non-existent nested key 'user.hobbies'...")
try:
    print(db['user']['hobbies'])
except KeyError:
    print("KeyError: 'hobbies'")

# Test concurrent access (simulate a simple multi-threaded environment with nested data)
def concurrent_set_nested():
    for i in range(10):
        db['nested_key'][f'concurrent_key_{i}'] = f'value_{i}'
        print(f"Set nested_key.concurrent_key_{i} to value_{i}")

def concurrent_get_nested():
    for i in range(10):
        print(f"Got nested_key.concurrent_key_{i}: {db['nested_key'].get(f'concurrent_key_{i}')}")
        
# Create threads for concurrent set and get of nested data
thread_1 = threading.Thread(target=concurrent_set_nested)
thread_2 = threading.Thread(target=concurrent_get_nested)

thread_1.start()
thread_2.start()

# Wait for both threads to complete
thread_1.join()
thread_2.join()

# Test deleting an entire nested key (e.g., 'user')
print("\nDeleting 'user'...")
del db['user']
print("Trying to access 'user' after deletion...")
try:
    print(db['user'])
except KeyError:
    print("KeyError: 'user'")

# Test setting a key that is a dictionary within a dictionary
print("\nSetting nested dictionaries...")
db['settings'] = {'theme': 'light', 'notifications': {'email': True, 'sms': False}}

print("Getting nested 'settings.theme'...")
print(db['settings']['theme'])  # Expected output: light

print("Getting nested 'settings.notifications.email'...")
print(db['settings']['notifications']['email'])  # Expected output: True

# Test deep nesting
print("\nSetting deep nested data...")
db['nested'] = {'level_1': {'level_2': {'level_3': 'deep_value'}}}

print("Getting deep nested data 'nested.level_1.level_2.level_3'...")
print(db['nested']['level_1']['level_2']['level_3'])  # Expected output: deep_value

# Test iterating over nested data
print("\nIterating over nested 'settings.notifications' keys...")
for key in db['settings']['notifications'].keys():
    print(key)  # Expected output: 'email', 'sms'

print("\nAll tests completed.")


