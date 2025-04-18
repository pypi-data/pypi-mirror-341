class _ModuleWrapper:
    def __init__(self, sdk, module):
        for key in dir(module):
            fn = getattr(module, key)
            if callable(fn) and not key.startswith("_"):
                setattr(self, key, fn.__get__(sdk))