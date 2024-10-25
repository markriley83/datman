#!/usr/bin/python
import os
from database_manager import DatabaseManager

class Disk():
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
        self.md5     = None
        self.sha1    = None
        self.merge   = None
        self.status  = None
        self.game_id = None

    def save(self):
        if self.id == None:
            self.save_new()
        else:
            self.save_edit()

    def save_new(self):
        statement = '''INSERT INTO disk
                            (name,
                             md5,
                             sha1,
                             merge,
                             status,
                             game_id)
                     values
                            (?,?,?,?,?,?)'''
        params = (self.name,
                  self.md5,
                  self.sha1,
                  self.merge,
                  self.status,
                  self.game_id)
        self.id = self.database_manager.execute_statement_get_id(statement, params)

    def save_edit(self):
        statement = '''UPDATE disk SET
                             name = ?,
                             md5 = ?,
                             sha1 = ?,
                             merge = ?,
                             status = ?,
                             game_id = ?
                     WHERE
                             id = ?'''
        params = (self.name,
                  self.md5,
                  self.sha1,
                  self.merge,
                  self.status,
                  self.game_id,
                  self.id)
        self.id = self.database_manager.execute_statement_get_id(statement, params)

    def get_by_id(self):
        statement = "SELECT * FROM disk WHERE id = ?"
        params = (self.id,)
        disk = self.database_manager.execute_statement(statement, params)[0]
        self.id = disk[0]
        self.crc32 = disk[1]
        self.md5 = disk[2]
        self.sha1 = disk[3]
        self.merge = disk[4]
        self.status = disk[5]
        self.game_id = disk[6]
