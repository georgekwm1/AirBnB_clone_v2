#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
import json


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls:
            if isinstance(cls, str):
                cls = eval(cls)
            instances = {}
            for key, value in self.__objects.items():
                if isinstance(value, cls):
                    instances[key] = value
            return instances
        return self.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        class_name = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[class_name] = obj

    def save(self):
        """Saves storage dictionary to file"""
        with open(self.__file_path, "w") as file:
            my_dict = self.__objects
            my_dict = {key: my_dict[key].to_dict() for key in my_dict.keys()}
            json.dump(my_dict, file)

    def reload(self):
        """Deserializes the JSON file to __objects (only if the file exists)"""
        try:
            with open(self.__file_path, 'r') as file:
                data = json.load(file)
            for obj in data.values():
                class_name = obj["__class__"]
                self.new(eval(class_name)(**obj))
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """delete obj from __objects"""
        if (obj):
            className = f"{obj.__class__.__name__}.{obj.id}"
            try:
                del self.__objects[className]
            except KeyError:
                pass
                
    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()
