#!/usr/bin/python
import os
from database_manager import DatabaseManager

class Rom():
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
        self.size    = None
        self.crc32   = None
        self.md5     = None
        self.sha1    = None
        self.merge   = None
        self.status  = None
        self.date    = None
        self.game_id = None

    def save(self):
        if self.id == None:
            self.save_new()
        else:
            self.save_edit()

    def save_new(self):
        statement = '''INSERT INTO rom
                            (name,
                             size,
                             crc32,
                             md5,
                             sha1,
                             merge,
                             status,
                             date,
                             game_id)
                     values
                            (?,?,?,?,?,?,?,?,?)'''
        params = (self.name,
                  self.size,
                  self.crc32,
                  self.md5,
                  self.sha1,
                  self.merge,
                  self.status,
                  self.date,
                  self.game_id)
        self.id = self.database_manager.execute_statement_get_id(statement, params)

    def save_edit(self):
        statement = '''UPDATE rom SET
                             name = ?,
                             size = ?,
                             crc32 = ?,
                             md5 = ?,
                             sha1 = ?,
                             merge = ?,
                             status = ?,
                             date = ?,
                             game_id = ?
                     WHERE
                             id = ?'''
        params = (self.name,
                  self.size,
                  self.crc32,
                  self.md5,
                  self.sha1,
                  self.merge,
                  self.status,
                  self.date,
                  self.game_id,
                  self.id)
        self.id = self.database_manager.execute_statement_get_id(statement, params)

    @staticmethod
    def get_all_roms():
        statement = "SELECT * FROM rom"
        params = []
        rom_list = Rom().database_manager.execute_statement(statement, params)
        return_list = []
        for rom in rom_list:
            return_rom = Rom()
            return_rom.id = rom[0]
            return_rom.name = rom[1]
            return_rom.size = rom[2]
            return_rom.crc32 = rom[3]
            return_rom.md5 = rom[4]
            return_rom.sha1 = rom[5]
            return_rom.merge = rom[6]
            return_rom.status = rom[7]
            return_rom.date = rom[8]
            return_rom.game_id = rom[9]
            return_list.append(return_rom)
        return return_list

    def get_by_id(self):
        statement = "SELECT * FROM rom WHERE id = ?"
        params = (self.id,)
        rom = self.database_manager.execute_statement(statement, params)[0]
        self.id = rom[0]
        self.name = rom[1]
        self.size = rom[2]
        self.crc32 = rom[3]
        self.md5 = rom[4]
        self.sha1 = rom[5]
        self.merge = rom[6]
        self.status = rom[7]
        self.date = rom[8]
        self.game_id = rom[9]
