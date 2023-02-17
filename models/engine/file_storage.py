#!/usr/bin/python3
'''
    Define the class FileStorage system
'''
import json
import models


class FileStorage:
    '''
        Serializes instances to JSON file && deserializes to JSON file.
    '''
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        '''
            Return--> dictionary
        '''
        n_dict = {}
        if cls is None:
            return self.__objects

        if cls != "":
            for x, v in self.__objects.items():
                if cls == x.split(".")[0]:
                    n_dict[x] = v
            return n_dict
        else:
            return self.__objects

    def new(self, obj):
        '''
            Set in __objects the obj with key <obj class name>.id
            Aguments:
                obj : An instance object.
        '''
        key = str(obj.__class__.__name__) + "." + str(obj.id)
        value_dict = obj
        FileStorage.__objects[key] = value_dict

    def save(self):
        '''
            Serializes __objects attr to JSON file.
        '''
        objs_d = {}
        for key, val in FileStorage.__objects.items():
            objs_d[key] = val.to_dict()

        with open(FileStorage.__file_path, mode='w', encoding="UTF8") as fd:
            json.dump(objs_d, fd)

    def reload(self):
        '''
            Deserializes the JSON file to __objects.
        '''
        try:
            with open(FileStorage.__file_path, encoding="UTF8") as fd:
                FileStorage.__objects = json.load(fd)
            for key, val in FileStorage.__objects.items():
                class_name = val["__class__"]
                class_name = models.classes[class_name]
                FileStorage.__objects[key] = class_name(**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        '''
        Deletes an obj
        '''
        if obj is not None:
            key = str(obj.__class__.__name__) + "." + str(obj.id)
            FileStorage.__objects.pop(key, None)
            self.save()

    def close(self):
        '''
        Deserialize JSON file to objects
        '''
        self.reload()

    def get(self, cls, id):
        '''
            Retrieve an obj w/class name and id
        '''
        result = None

        try:
            for v in self.__objects.values():
                if v.id == id:
                    result = v
        except BaseException:
            pass

        return result

    def count(self, cls=None):
        '''
            Count--> number of  objects in FileStorage
        '''
        cls_cntr = 0

        if cls is not None:
            for x in self.__objects.keys():
                if cls in x:
                    cls_cntr += 1
        else:
            cls_cntr = len(self.__objects)
        return cls_cntr
