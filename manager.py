from locker import Locker

pw_manager = Locker()
data = pw_manager.read()

obj = {
    'Google': {
        'SECRET': 'mynamejeff',
        'HINT': 'His name is jeff'
    },
    'Reddit': {
        'SECRET': 'iambatman',
        'HINT': 'He is batman'
    }
}

pw_manager.write(obj)
