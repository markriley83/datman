#!/usr/bin/python
import os
from database_manager import DatabaseManager

class ArchivedFile():
    database_manager = None

    def __init__(self):
        self.clear()
        self.database_manager = DatabaseManager.Instance()

    def set_profile(self, profile=os.path.join(os.path.expanduser("~"), ".datman")):
        print("Profile Location: %s" % profile)
        self.database_manager.connect(profile)

    def clear(self):
        self.id           = None
        self.file_id      = None
        self.container_id = None

    def save(self):
        if self.id == None:
            self.save_new()
        else:
            self.save_edit()

    def save_new(self):
        statement = '''INSERT INTO archived_file
                            (file_id,
                             container_id)
                     values
                            (?,?)'''
        params = (self.file_id,
                  self.container_id)
        self.id = self.database_manager.execute_statement_get_id(statement, params)

    def save_edit(self):
        statement = '''UPDATE archived_file SET
                             file_id = ?,
                             container_id = ?
                     WHERE
                             id = ?'''
        params = (self.file_id,
                  self.container_id,
                  self.id)
        self.id = self.database_manager.execute_statement_get_id(statement, params)

    def get_by_id(self):
        statement = "SELECT * FROM archived_file WHERE id = ?"
        params = (self.id,)
        archived_file = self.database_manager.execute_statement(statement, params)
        if len(archived_file) > 0:
            self.id = archived_file[0][0]
            self.file_id = archived_file[0][1]
            self.container_id = archived_file[0][2]
            return True
        else:
            return False

    def get_by_file_id(self):
        statement = "SELECT * FROM archived_file WHERE file_id = ?"
        params = (self.file_id,)
        archived_file = self.database_manager.execute_statement(statement, params)
        if len(archived_file) > 0:
            self.id = archived_file[0][0]
            self.file_id = archived_file[0][1]
            self.container_id = archived_file[0][2]
            return True
        else:
            return False
