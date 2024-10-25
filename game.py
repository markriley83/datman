#!/usr/bin/python
import os
from database_manager import DatabaseManager

class Game():
    database_manager = None

    def __init__(self):
        self.clear()
        self.database_manager = DatabaseManager.Instance()

    def set_profile(self, profile=os.path.join(os.path.expanduser("~"), ".datman")):
        print("Profile Location: %s" % profile)
        self.database_manager.connect(profile)

    def clear(self):
        self.id           = None
        self.comment      = None
        self.description  = None
        self.year         = None
        self.manufacturer = None
        self.name         = None
        self.source_file  = None
        self.is_bios      = None
        self.clone_of     = None
        self.sample_of    = None
        self.board        = None
        self.rebuild_to   = None
        self.datfile_id   = None

    def save(self):
        if self.id == None:
            self.save_new()
        else:
            self.save_edit()

    def save_new(self):
        statement = '''INSERT INTO game
                            (comment,
                             description,
                             year,
                             manufacturer,
                             name,
                             source_file,
                             is_bios,
                             clone_of,
                             sample_of,
                             board,
                             rebuild_to,
                             datfile_id)
                     values
                            (?,?,?,?,?,?,?,?,?,?,?,?)'''
        params = (self.comment,
                  self.description,
                  self.year,
                  self.manufacturer,
                  self.name,
                  self.source_file,
                  self.is_bios,
                  self.clone_of,
                  self.sample_of,
                  self.board,
                  self.rebuild_to,
                  self.datfile_id)
        self.id = self.database_manager.execute_statement_get_id(statement, params)

    def save_edit(self):
        statement = '''UPDATE game SET
                             comment = ?,
                             description = ?,
                             year = ?,
                             manufacturer = ?,
                             name = ?,
                             source_file = ?,
                             is_bios = ?,
                             clone_of = ?,
                             sample_of = ?,
                             board = ?,
                             rebuild_to = ?,
                             datfile_id = ?
                     WHERE
                             id = ?'''
        params = (self.comment,
                  self.description,
                  self.year,
                  self.manufacturer,
                  self.name,
                  self.source_file,
                  self.is_bios,
                  self.clone_of,
                  self.sample_of,
                  self.board,
                  self.rebuild_to,
                  self.datfile_id,
                  self.id)
        self.id = self.database_manager.execute_statement_get_id(statement, params)

    def get_by_id(self):
        statement = "SELECT * FROM game WHERE id = ?"
        params = (self.id,)
        game = self.database_manager.execute_statement(statement, params)[0]
        self.id = game[0]
        self.comment = game[1]
        self.description = game[2]
        self.year = game[3]
        self.manufacturer = game[4]
        self.name = game[5]
        self.source_file = game[6]
        self.is_bios = game[7]
        self.clone_of = game[8]
        self.sample_of = game[9]
        self.board = game[10]
        self.rebuild_to = game[11]
        self.datfile_id = game[12]
