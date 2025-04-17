# Stub file for get_class_from_str
def get_class_from_str(s):
    class Dummy:
        pass
    obj = Dummy()
    obj.__dict__["value"] = s
    return obj
