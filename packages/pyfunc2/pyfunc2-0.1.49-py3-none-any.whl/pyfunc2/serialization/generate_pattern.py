import re

def generate_pattern(text_pattern):
    var_list = re.findall('\{([^"]*)\}', text_pattern)
    #print(var_list)
    var_dict = {}
    for var in var_list:
        #regexp = text_pattern.replace(var, '[^"]*')
        regexp = text_pattern.replace(var, '\w+')
        #regexp = regexp.replace(' ', '\s')
        regexp = regexp.replace('{', '(')
        regexp = regexp.replace('}', ')')
        #print(regexp)

        var_dict[var] = r"{}".format(regexp)

    #print(var_dict)

    return var_dict
    # return r"({})\sclass".format(class_name)