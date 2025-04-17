# Stub file for get_class_from_json
def get_class_from_json(j):
    class Dummy:
        pass
    obj = Dummy()
    if isinstance(j, dict):
        obj.__dict__.update(j)
    return obj
