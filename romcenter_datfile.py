#!/usr/bin/python
import os
from database_manager import DatabaseManager

class RomcenterDatfile():
    database_manager = None

    def __init__(self):
        self.clear()
        self.database_manager = DatabaseManager.Instance()

    def set_profile(self, profile=os.path.join(os.path.expanduser("~"), ".datman")):
        print("Profile Location: %s" % profile)
        self.database_manager.connect(profile)

    def clear(self):
        self.datfile_id       = None
        self.plugin           = None
        self.rom_mode         = None
        self.bios_mode        = None
        self.sample_mode      = None
        self.lock_rom_mode    = None
        self.lock_bios_mode   = None
        self.lock_sample_mode = None

    def save(self):
        if self.id == None:
            self.save_new()
        else:
            self.save_edit()

    def save_new(self):
        statement = '''INSERT INTO romcenter_datfile
                            (datfile_id,
                             plugin,
                             rom_mode,
                             bios_mode,
                             sample_mode,
                             lock_rom_mode,
                             lock_bios_mode,
                             lock_sample_mode)
                     values
                            (?,?,?,?,?,?,?,?)'''
        params = (self.datfile_id,
                  self.plugin,
                  self.rom_mode,
                  self.bios_mode,
                  self.sample_mode,
                  self.lock_rom_mode,
                  self.lock_bios_mode,
                  self.lock_sample_mode)
        self.id = self.database_manager.execute_statement_get_id(statement, params)

    def save_edit(self):
        statement = '''UPDATE romcenter_datfile SET
                             plugin = ?,
                             rom_mode = ?,
                             bios_mode = ?,
                             sample_mode = ?
                             lock_rom_mode = ?,
                             lock_bios_mode = ?,
                             lock_sample_mode = ?
                     WHERE
                             datfile_id = ?'''
        params = (sself.plugin,
                  self.rom_mode,
                  self.bios_mode,
                  self.sample_mode,
                  self.lock_rom_mode,
                  self.lock_bios_mode,
                  self.lock_sample_mode,
                  self.datfile_id)
        self.id = self.database_manager.execute_statement_get_id(statement, params)

    def get_by_id(self):
        statement = "SELECT * FROM romcenter_datfile WHERE datfile_id = ?"
        params = (self.datfile_id,)
        romcenter_datfile = self.database_manager.execute_statement(statement, params)[0]
        self.datfile_id = romcenter_datfile[0]
        self.plugin = romcenter_datfile[1]
        self.rom_mode = romcenter_datfile[2]
        self.bios_mode = romcenter_datfile[3]
        self.sample_mode = romcenter_datfile[4]
        self.lock_rom_mode = romcenter_datfile[2]
        self.lock_bios_mode = romcenter_datfile[3]
        self.lock_sample_mode = romcenter_datfile[4]
