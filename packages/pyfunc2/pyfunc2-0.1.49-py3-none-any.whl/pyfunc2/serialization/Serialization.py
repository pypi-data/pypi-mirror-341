import json
import numpy as np


class Serialization:
    object_class = {}  # class variable shared by all instances
    object_json = {}  # json variable shared by all instances
    dictionary = ""
    sentence = ""

    def __init__(self, object_class):
        self.object_class = object_class

    def fromObject(self):
        return True

    def fromClass(self):
        return True


    def getSerializedSentence(self, full=False):
        # Deserialize the JSON back to a dictionary
        dictionary = json.loads(self.object_json)
        value_list = np.array(dictionary.values())
        attr_list = np.array(dictionary.keys())
        attr_sentence = ""
        value_sentence = ""
        key_value_sentence = ""
        for k, v in dictionary.items():
            # k is the key
            # v is the value
            if attr_sentence: attr_sentence = attr_sentence + ", "
            attr_sentence = attr_sentence + str(k)
            if value_sentence: value_sentence = value_sentence + ", "
            value_sentence = value_sentence + str(v)

        class_name = type(self.object_class).__name__
        # class_name = self.object_json.__class__.__name__
        object_methods_params = {}

        # Convert the dictionary back to a human-readable sentence
        # self.sentence = f"The [{class_name}] Class can do {object_methods} and each command can {object_methods_params} and give data {attr_sentence} with a values {value_sentence}"
        # self.sentence = f"The {class_name} class can do: {object_methods} and use data names: {attr_sentence} & this object has values: {key_value_sentence}"
        # self.sentence = f"The {class_name} class can do: {object_methods} and use data names: {attr_sentence}."
        object_methods = self.getSerializedSentenceFunctions()
        self.sentence = ""
        if full: self.sentence = f"The {class_name} class "
        self.sentence = self.sentence + f"can {object_methods} "

        # self.sentence = human_readable_sentence(dictionary)
        return self.sentence


    def getSerializedJSON(self):
        # Convert the book to a dictionary
        object_dict = self.object_class.__dict__

        # Serialize the book to a JSON string
        self.object_json = json.dumps(object_dict)

        return self.object_json

    def getSerializedFunctions(self):
        # object_methods = [method_name for method_name in dir(self.object_class) if callable(getattr(self.object_class, method_name))]
        # Extract list of existing methods in python class based on object instance
        object_methods = [method for method in dir(self.object_class) if
                          callable(getattr(self.object_class, method)) and not method.startswith("__")]

        return object_methods

    def getSerializedSentenceFunctions(self, end = "", separator = ", "):
        key_value_sentence = ""
        for value in self.getSerializedFunctions():
            if key_value_sentence: key_value_sentence = key_value_sentence + separator
            key_value_sentence = key_value_sentence + str(value) + ""

        key_value_sentence = key_value_sentence + end

        return key_value_sentence

    def getSerializedDataSentence(self, full=False, end = ";", separator = ", "):
        # Deserialize the JSON back to a dictionary
        dictionary = json.loads(self.object_json)
        attr_sentence = ""
        for key, value in dictionary.items():
            if attr_sentence: attr_sentence = attr_sentence + separator
            attr_sentence = attr_sentence + str(key)

        attr_sentence = attr_sentence + end
        class_name = type(self.object_class).__name__

        # Convert the dictionary back to a human-readable sentence
        self.sentence = ""
        if full: self.sentence = f"The {class_name} class "
        self.sentence = self.sentence + f"use data names: {attr_sentence}"

        return self.sentence

    def getSerializedInstanceSentence(self, full=False, end = " ", separator = "; "):
        # Deserialize the JSON back to a dictionary
        dictionary = json.loads(self.object_json)
        key_value_sentence = ""
        for key, value in dictionary.items():
            if key_value_sentence: key_value_sentence = key_value_sentence + separator
            key_value_sentence = key_value_sentence + str(key) + ": " + str(value) + ""

        key_value_sentence = key_value_sentence + end
        class_name = type(self.object_class).__name__

        # Convert the dictionary back to a human-readable sentence
        self.sentence = ""
        if full: self.sentence = f"The {class_name} class instance "
        self.sentence = self.sentence + f"has values: {key_value_sentence}"

        return self.sentence

    def getSerializedMethodSentence(self, full=False, end = ";", separator = " "):
        class_name = type(self.object_class).__name__
        # Convert the dictionary back to a human-readable sentence
        object_methods = self.getSerializedSentenceFunctions("", separator)
        self.sentence = ""
        if full: self.sentence = f"The {class_name} class "
        self.sentence = self.sentence + f"can {object_methods}" + end

        return self.sentence


    def getSerializedData(self):
        # Deserialize the JSON back to a dictionary
        dictionary = json.loads(self.object_json)

        return dictionary