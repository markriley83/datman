#!/usr/bin/python
import os
from database_manager import DatabaseManager

class BiosSet():
    database_manager = None

    def __init__(self):
        self.clear()
        self.database_manager = DatabaseManager.Instance()

    def set_profile(self, profile=os.path.join(os.path.expanduser("~"), ".datman")):
        print("Profile Location: %s" % profile)
        self.database_manager.connect(profile)

    def clear(self):
        self.id          = None
        self.name        = None
        self.description = None
        self.default     = None
        self.game_id     = None

    def save(self):
        if self.id == None:
            self.save_new()
        else:
            self.save_edit()

    def save_new(self):
        statement = '''INSERT INTO bios_set
                            (name,
                             description,
                             default,
                             game_id)
                     values
                            (?,?,?,?)'''
        params = (self.name,
                  self.description,
                  self.default,
                  self.game_id)
        self.id = self.database_manager.execute_statement_get_id(statement, params)

    def save_edit(self):
        statement = '''UPDATE bios_set SET
                             name = ?,
                             description = ?,
                             default = ?,
                             game_id = ?
                     WHERE
                             id = ?'''
        params = (self.name,
                  self.description,
                  self.default,
                  self.game_id,
                  self.id)
        self.id = self.database_manager.execute_statement_get_id(statement, params)

    def get_by_id(self):
        statement = "SELECT * FROM bios_set WHERE id = ?"
        params = (self.id,)
        bios_set = self.database_manager.execute_statement(statement, params)[0]
        self.id = bios_set[0]
        self.name = bios_set[1]
        self.description = bios_set[2]
        self.default = bios_set[3]
        self.game_id = bios_set[4]
