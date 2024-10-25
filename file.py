#!/usr/bin/python
import os
from database_manager import DatabaseManager

class File():
    database_manager = None

    def __init__(self):
        self.clear()
        self.database_manager = DatabaseManager.Instance()

    def set_profile(self, profile=os.path.join(os.path.expanduser("~"), ".datman")):
        print("Profile Location: %s" % profile)
        self.database_manager.connect(profile)

    def clear(self):
        self.id                 = None
        self.file_dump_root_ref = None
        self.filepath           = None
        self.filename           = None
        self.is_container       = None
        self.size               = None
        self.crc32              = None
        self.md5                = None
        self.sha1               = None

    def save(self):
        if self.id == None:
            self.save_new()
        else:
            self.save_edit()

    def save_new(self):
        statement = '''INSERT INTO file
                            (file_dump_root_ref,
                             filepath,
                             filename,
                             is_container,
                             size,
                             crc32,
                             md5,
                             sha1)
                     values
                            (?,?,?,?,?,?,?,?)'''
        params = (self.file_dump_root_ref,
                  self.filepath,
                  self.filename,
                  self.is_container,
                  self.size,
                  self.crc32,
                  self.md5,
                  self.sha1)
        self.id = self.database_manager.execute_statement_get_id(statement, params)

    def save_edit(self):
        statement = '''UPDATE file SET
                             file_dump_root_ref = ?,
                             filepath = ?,
                             filename = ?,
                             is_container = ?,
                             size = ?,
                             crc32 = ?,
                             md5 = ?,
                             sha1 = ?
                     WHERE
                             id = ?'''
        params = (self.file_dump_root_ref,
                  self.filepath,
                  self.filename,
                  self.is_container,
                  self.size,
                  self.crc32,
                  self.md5,
                  self.sha1,
                  self.id)
        self.id = self.database_manager.execute_statement_get_id(statement, params)

    def get_by_id(self):
        statement = "SELECT * FROM file WHERE id = ?"
        params = (self.id,)
        file = self.database_manager.execute_statement(statement, params)[0]
        self.id = file[0]
        self.file_dump_root_ref = file[1]
        self.filepath = file[2]
        self.filename = file[3]
        self.is_container = file[4]
        self.size = file[5]
        self.crc32 = file[6]
        self.md5 = file[7]
        self.sha1 = file[8]

    def get_by_visible(self):
        statement = '''SELECT * FROM file WHERE
                             file_dump_root_ref = ? AND
                             filepath = ? AND
                             filename = ? AND
                             size = ?'''
        params = (self.file_dump_root_ref, self.filepath, self.filename, self.size)
        file = self.database_manager.execute_statement(statement, params)
        if len(file) > 0:
            self.id = file[0][0]
            self.file_dump_root_ref = file[0][1]
            self.filepath = file[0][2]
            self.filename = file[0][3]
            self.is_container = file[0][4]
            self.size = file[0][5]
            self.crc32 = file[0][6]
            self.md5 = file[0][7]
            self.sha1 = file[0][8]

    def get_list_by_available_attributes(self):
        statement = "SELECT * FROM file WHERE "
        params = []
        if not self.size == None:
            statement += "size = ? AND "
            params.append(self.size)
        if not self.crc32 == None:
            statement += "crc32 = ? AND "
            params.append(self.crc32.upper())
        if not self.md5 == None:
            statement += "md5 = ? AND "
            params.append(self.md5.upper())
        if not self.sha1 == None:
            statement += "sha1 = ? AND "
            params.append(self.sha1.upper())
        statement += "1=1"
        files = self.database_manager.execute_statement(statement, params)
        return_list = []
        for file in files:
            return_file = File()
            return_file.id = file[0]
            return_file.file_dump_root_ref = file[1]
            return_file.filepath = file[2]
            return_file.filename = file[3]
            return_file.is_container = file[4]
            return_file.size = file[5]
            return_file.crc32 = file[6]
            return_file.md5 = file[7]
            return_file.sha1 = file[8]
            return_list.append(return_file)
        return return_list
