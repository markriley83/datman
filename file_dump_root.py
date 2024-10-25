#!/usr/bin/python
import os
from database_manager import DatabaseManager

class FileDumpRoot():
    database_manager = None

    def __init__(self):
        self.clear()
        self.database_manager = DatabaseManager.Instance()

    def set_profile(self, profile=os.path.join(os.path.expanduser("~"), ".datman")):
        print("Profile Location: %s" % profile)
        self.database_manager.connect(profile)

    def clear(self):
        self.id       = None
        self.path     = None
        self.priority = None

    def save(self):
        if self.id == None:
            self.save_new()
        else:
            self.save_edit()

    def save_new(self):
        statement = '''INSERT INTO file_dump_root
                            (path,
                             priority)
                     values
                            (?,?)'''
        params = (self.path,
                  self.priority)
        self.id = self.database_manager.execute_statement_get_id(statement, params)

    def save_edit(self):
        statement = '''UPDATE file_dump_root SET
                             path = ?,
                             priority = ?
                     WHERE
                             id = ?'''
        params = (self.path,
                  self.priority,
                  self.id)
        self.id = self.database_manager.execute_statement_get_id(statement, params)

    def get_by_id(self):
        statement = "SELECT * FROM file_dump_root WHERE id = ?"
        params = (self.id,)
        file_dump_root = self.database_manager.execute_statement(statement, params)[0]
        self.id = file_dump_root[0]
        self.path = file_dump_root[1]
        self.priority = file_dump_root[2]

    def get_by_path(self):
        statement = "SELECT * FROM file_dump_root WHERE path = ?"
        params = (self.path,)
        file_dump_root = self.database_manager.execute_statement(statement, params)
        if len(file_dump_root) > 0:
            self.id = file_dump_root[0][0]
            self.path = file_dump_root[0][1]
            self.priority = file_dump_root[0][2]
