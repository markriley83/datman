#!/usr/bin/python
import os
from database_manager import DatabaseManager

class DatfileRoot():
    database_manager = None

    def __init__(self):
        self.clear()
        self.database_manager = DatabaseManager.Instance()

    def set_profile(self, profile=os.path.join(os.path.expanduser("~"), ".datman")):
        print("Profile Location: %s" % profile)
        self.database_manager.connect(profile)

    def clear(self):
        self.id                   = None
        self.path                 = None
        self.rebuild_location_ref = None

    def save(self):
        if self.id == None:
            self.save_new()
        else:
            self.save_edit()

    def save_new(self):
        statement = '''INSERT INTO datfile_root
                            (path,
                             rebuild_location_ref)
                     values
                            (?,?)'''
        params = (self.path,
                  self.rebuild_location_ref)
        self.id = self.database_manager.execute_statement_get_id(statement, params)

    def save_edit(self):
        statement = '''UPDATE datfile_root SET
                             path = ?,
                             rebuild_location_ref = ?
                     WHERE
                             id = ?'''
        params = (self.path,
                  self.rebuild_location_ref,
                  self.id)
        self.id = self.database_manager.execute_statement_get_id(statement, params)

    def get_by_id(self):
        statement = "SELECT * FROM datfile_root WHERE id = ?"
        params = (self.id,)
        datfile_root = self.database_manager.execute_statement(statement, params)[0]
        self.id = datfile_root[0]
        self.path = datfile_root[1]
        self.rebuild_location_ref = datfile_root[2]

    def get_by_path(self):
        statement = "SELECT * FROM datfile_root WHERE path = ?"
        params = (self.path,)
        datfile_root = self.database_manager.execute_statement(statement, params)
        if len(datfile_root) > 0:
            self.id = datfile_root[0][0]
            self.path = datfile_root[0][1]
            self.rebuild_location_ref = datfile_root[2]
