#!/usr/bin/python3
""" Console Module """

from models.base_model import BaseModel
from models.__init__ import storage
from models.amenity import Amenity
from models.review import Review
from models.place import Place
from models.state import State
from models.user import User
from models.city import City
import cmd


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) '

    classes = [
               'BaseModel', 'User', 'Place', 'State',
               'City', 'Amenity', 'Review'
    ]

    def do_quit(self, command):
        """ Method to exit the HBNB console"""
        return True

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        print()
        return True

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass

    def do_create(self, args):
        """ Create an object of any class"""
        if not args:
            print("** class name missing **")
            return
        args = args.split()
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        new_instance = eval(args[0])()

        for parameter in args[1:]:
            name, value = parameter.split("=")
            test = value
            if test[0] == '"':
                value = value.strip('"').replace('_', ' ')

            else:
                if test[0] == '-':
                    test = test.lstrip('-')
                if ('.' in test) and (test.replace('.', '', 1).isdigit()):
                    value = float(value)
                else:
                    value = int(value)

            new_instance.__dict__[name] = value
        new_instance.save()
        print(new_instance.id)

    def help_create(self):
        """ Help information for the create method """
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def do_show(self, args):
        """Prints the string representation of an instance"""

        if not args:
            print("** class name missing **")

        else:
            args = args.split()
            if args[0] not in self.classes:
                print("** class doesn't exist **")

            elif len(args) < 2:
                print("** instance id missing **")

            elif f"{args[0]}.{args[1]}" not in storage.all().keys():
                print("** no instance found **")

            else:
                key = f"{args[0]}.{args[1]}"
                print(storage.all()[key])

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """Deletes an instance based on the class name and id"""

        if not args:
            print("** class name missing **")

        else:
            args = args.split()

            if args[0] not in self.classes:
                print("** class doesn't exist **")

            elif len(args) < 2:
                print("** instance id missing **")

            elif f"{args[0]}.{args[1]}" not in storage.all().keys():
                print("** no instance found **")

            else:
                key = f"{args[0]}.{args[1]}"
                del storage.all()[key]
                storage.save()

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """ Shows all objects, or all objects of a class"""
        if not args:
            myList = [str(value) for value in storage.all().values()]
        else:
            myCls = args.split()[0]
            if myCls not in self.classes:
                print("** class doesn't exist **")
            else:
                myList = [str(value) for value in storage.all(myCls).values()]
        print(myList)

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_update(self, args):
        """Updates an instance based on the class name and id"""

        myDict = storage.all()
        if not args:
            print("** class name missing **")

        else:
            args = args.split()
            if args[0] not in self.classes:
                print("** class doesn't exist **")

            elif len(args) == 1:
                print("** instance id missing **")

            else:
                key = f"{args[0]}.{args[1]}"
                if key not in myDict.keys():
                    print(key)
                    print("** no instance found **")

                else:
                    if len(args) == 2:
                        print("** attribute name missing **")

                    elif len(args) == 3:
                        print("** value missing **")

                    else:
                        myInstance = myDict[key]
                        myValue = args[3]
                        if myValue[0] == '"' and myValue[-1] == '"':
                            myValue = myValue.strip('"')
                        elif myValue.isdigit():
                            myValue = int(myValue)
                        elif myValue[0] == "-":
                            if myValue.replace("-", "").isdigit():
                                myValue = int(myValue)
                        else:
                            try:
                                myValue = float(mVvalue)
                            except ValueError:
                                pass
                        setattr(myInstance , args[2], myValue)
                        myInstance.save()

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
