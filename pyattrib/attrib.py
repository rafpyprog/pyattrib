# -*- coding: utf-8 -*-

'''
Displays, sets, or removes the read-only, archive, system, and hidden
attributes assigned to files or directories. Used without parameters,
attrib displays attributes of all files in the current directory.
'''
import os
import subprocess
from subprocess import PIPE


ATTR_ARCHIVE = 'A'
ATTR_HIDDEN = 'H'
ATTR_READ_ONLY = 'R'
ATTR_SYSTEM_FILE = 'S'
ATTRIBUTES = (ATTR_ARCHIVE, ATTR_HIDDEN, ATTR_READ_ONLY, ATTR_SYSTEM_FILE)



class Attrib():
    def __init__(self, path=None, recursive=False, apply_directories=False):
        '''
        Parameters
        ----------
        path: string, defaults None
            Specifies the location and name of the directory, file, or
            set of files for which you want to display or change attributes.
            You can use wildcard characters (that is, ? and *) in the FileName
            parameter to display or change the attributes for a group of files.
        recursive: boolean, default False
            Applies attrib and any command-line options to matching files in
            the current directory and all of its subdirectories.
        apply_directories: boolean, default False
            Applies attrib and any command-line options to directories.
        '''
        self.SET = '+'
        self.REMOVE = '-'

        self.path = path

        if self.path is None:
            self.CMD = ['attrib']
        else:
            self.path = os.path.abspath(path)
            self.CMD = ['attrib', self.path]

        self.recursive = recursive
        self.apply_directories = apply_directories

    @property
    def attributes(self):
        if self.path:
            attr = self.get_attributes()
            # remove the path and line breaks
            attr = attr.replace(self.path, '').strip('\n')
            attr = attr.replace(" ", "")
            attr = list(attr.upper())
        else:
            attr = self.get_attributes()
            attr = attr.split('\n')
        return attr

    def get_attributes(self):
        attrib = subprocess.run(self.CMD, stdout=PIPE,
                                encoding='utf-8', check=True)
        assert attrib.returncode == 0
        return attrib.stdout

    def set_attributes(self, *args):
        for attr in args:  # check is attribute is valid
            if self.is_valid_attribute(attr) is False:
                raise ValueError('{} is not a valid attribute.'.format(attr))

        self.toogle_attributes(self.SET, *args)

    def clear_attributes(self, *args):
        # check is attribute is valid
        for attr in args:
            if self.is_valid_attribute(attr) is False:
                raise ValueError('{} is not a valid attribute.'.format(attr))
        self.toogle_attributes(self.REMOVE, *args)

    def toogle_attributes(self, action, *attributes):
        # check if is directory
        args = self.CMD.copy()

        for attr in attributes:
            args.insert(-1, ''.join([action, attr]))

        if self.recursive is True:
            args.append('/s')

        if self.apply_directories is True:
            args.append('/d')

        try:
            cmd = subprocess.run(args, check=True, stdout=PIPE,
                                 encoding='utf-8')
        except UnicodeError:
            cmd = subprocess.run(args, check=True, stdout=PIPE,
                                 encoding='latin-1')

        # If there's stdout and path is not empty Attrib returned a msg error.
        # Some attributes can't be set after another eg.: +a in a file with +s
        # If the path is empty or there is a path but no args,
        # Attrib cmd returns the attributes of the files inside the current
        # directory. We ignore this behavior.
        has_path = self.path != ''
        has_args = attributes != ()
        stdout_has_erros = cmd.stdout != ''

        if has_path and has_args and stdout_has_erros:
            msg = 'Cant set {} with the actual attributes {}'
            raise AttributeError(msg.format(attributes, self.attributes))

    def is_valid_attribute(self, attribute):
        is_valid = attribute.upper() in ATTRIBUTES
        return is_valid

    def clear_all(self):
        self.clear_attributes(*ATTRIBUTES)

    @property
    def is_hidden(self):
        return ATTR_HIDDEN in self.attributes

    @property
    def is_archive(self):
        return ATTR_ARCHIVE in self.attributes

    @property
    def is_read_only(self):
        return ATTR_READ_ONLY in self.attributes

    @property
    def is_system_file(self):
        return ATTR_SYSTEM_FILE in self.attributes

if __name__ == '__main__':
    a = Attrib()
    print(a.attributes)
