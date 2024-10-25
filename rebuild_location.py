#!/usr/bin/python
import os
from database_manager import DatabaseManager

class RebuildLocation():
    database_manager = None

    def __init__(self):
        self.clear()
        self.database_manager = DatabaseManager.Instance()

    def set_profile(self, profile=os.path.join(os.path.expanduser("~"), ".datman")):
        print("Profile Location: %s" % profile)
        self.database_manager.connect(profile)

    def clear(self):
        self.id   = None
        self.path = None

    def save(self):
        if self.id == None:
            self.save_new()
        else:
            self.save_edit()

    def save_new(self):
        statement = '''INSERT INTO rebuild_location
                            (path)
                     values
                            (?)'''
        params = (self.path,)
        self.id = self.database_manager.execute_statement_get_id(statement, params)

    def save_edit(self):
        statement = '''UPDATE rebuild_location SET
                             path = ?
                     WHERE
                             id = ?'''
        params = (self.path,
                  self.id)
        self.id = self.database_manager.execute_statement_get_id(statement, params)

    def get_by_id(self):
        statement = "SELECT * FROM rebuild_location WHERE id = ?"
        params = (self.id,)
        rebuild_location = self.database_manager.execute_statement(statement, params)[0]
        self.id = rebuild_location[0]
        self.path = rebuild_location[1]

    def get_by_path(self):
        statement = "SELECT * FROM rebuild_location WHERE path = ?"
        params = (self.path,)
        rebuild_location = self.database_manager.execute_statement(statement, params)
        if len(rebuild_location) > 0:
            self.id = rebuild_location[0][0]
            self.path = rebuild_location[0][1]
