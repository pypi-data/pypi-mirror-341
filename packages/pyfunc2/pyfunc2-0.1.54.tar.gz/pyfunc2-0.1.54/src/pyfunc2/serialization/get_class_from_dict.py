# Stub file for get_class_from_dict
def get_class_from_dict(d):
    class Dummy:
        pass
    obj = Dummy()
    obj.__dict__.update(d)
    return obj
