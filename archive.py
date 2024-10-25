#!/usr/bin/python
import os
from database_manager import DatabaseManager

class Archive():
    database_manager = None

    def __init__(self):
        self.clear()
        self.database_manager = DatabaseManager.Instance()

    def set_profile(self, profile=os.path.join(os.path.expanduser("~"), ".datman")):
        print("Profile Location: %s" % profile)
        self.database_manager.connect(profile)

    def clear(self):
        self.id      = None
        self.name    = None
        self.game_id = None

    def save(self):
        if self.id == None:
            self.save_new()
        else:
            self.save_edit()

    def save_new(self):
        statement = '''INSERT INTO archive
                            (name,
                             game_id)
                     values
                            (?,?)'''
        params = (self.name,
                  self.game_id)
        self.id = self.database_manager.execute_statement_get_id(statement, params)

    def save_edit(self):
        statement = '''UPDATE archive SET
                             name = ?,
                             game_id = ?
                     WHERE
                             id = ?'''
        params = (self.name,
                  self.game_id,
                  self.id)
        self.id = self.database_manager.execute_statement_get_id(statement, params)

    def get_by_id(self):
        statement = "SELECT * FROM archive WHERE id = ?"
        params = (self.id,)
        archive = self.database_manager.execute_statement(statement, params)[0]
        self.id = archive[0]
        self.name = archive[1]
        self.game_id = archive[2]
