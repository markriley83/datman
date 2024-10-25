#!/usr/bin/python
import os
from database_manager import DatabaseManager

class Release():
    database_manager = None

    def __init__(self):
        self.clear()
        self.database_manager = DatabaseManager.Instance()

    def set_profile(self, profile=os.path.join(os.path.expanduser("~"), ".datman")):
        print("Profile Location: %s" % profile)
        self.database_manager.connect(profile)

    def clear(self):
        self.id       = None
        self.name     = None
        self.region   = None
        self.language = None
        self.date     = None
        self.default  = None
        self.game_id  = None

    def save(self):
        if self.id == None:
            self.save_new()
        else:
            self.save_edit()

    def save_new(self):
        statement = '''INSERT INTO release
                            (name,
                             region,
                             language,
                             date,
                             default,
                             game_id)
                     values
                            (?,?,?,?,?,?)'''
        params = (self.name,
                  self.region,
                  self.language,
                  self.date,
                  self.default,
                  self.game_id)
        self.id = self.database_manager.execute_statement_get_id(statement, params)

    def save_edit(self):
        statement = '''UPDATE release SET
                             name = ?,
                             region = ?,
                             language = ?,
                             date = ?,
                             default = ?,
                             game_id = ?
                     WHERE
                             id = ?'''
        params = (self.name,
                  self.region,
                  self.language,
                  self.date,
                  self.default,
                  self.game_id,
                  self.is_bios,
                  self.id)
        self.id = self.database_manager.execute_statement_get_id(statement, params)

    def get_by_id(self):
        statement = "SELECT * FROM release WHERE id = ?"
        params = (self.id,)
        release = self.database_manager.execute_statement(statement, params)[0]
        self.id = release[0]
        self.name = release[1]
        self.region = release[2]
        self.language = release[3]
        self.date = release[4]
        self.default = release[5]
        self.game_id = release[6]
