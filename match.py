#!/usr/bin/python
import os
from database_manager import DatabaseManager

class Match():
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
        self.rom_id = None

    def save(self):
        if self.id == None:
            self.save_new()
        else:
            self.save_edit()

    def save_new(self):
        statement = '''INSERT INTO match
                            (file_id,
                             rom_id)
                     values
                            (?,?)'''
        params = (self.file_id,
                  self.rom_id)
        self.id = self.database_manager.execute_statement_get_id(statement, params)

    def save_edit(self):
        statement = '''UPDATE match SET
                             file_id = ?,
                             rom_id = ?
                     WHERE
                             id = ?'''
        params = (self.file_id,
                  self.rom_id,
                  self.id)
        self.id = self.database_manager.execute_statement_get_id(statement, params)

    @staticmethod
    def get_all_matches():
        statement = "SELECT * FROM match"
        params = []
        match_list = Match().database_manager.execute_statement(statement, params)
        return_list = []
        for match in match_list:
            return_match = Match()
            return_match.id = match[0]
            return_match.file_id = match[1]
            return_match.rom_id = match[2]
            return_list.append(return_match)
        return return_list

    def get_by_id(self):
        statement = "SELECT * FROM match WHERE id = ?"
        params = (self.id,)
        match = self.database_manager.execute_statement(statement, params)[0]
        self.id = match[0]
        self.file_id = match[1]
        self.rom_id = match[2]

    def get_by_files(self):
        statement = "SELECT * FROM match WHERE file_id = ? AND rom_id = ?"
        params = (self.file_id, self.rom_id)
        match = self.database_manager.execute_statement(statement, params)
        if len(match) > 0:
            self.id = match[0][0]
            self.file_id = match[0][1]
            self.rom_id = match[0][1]
