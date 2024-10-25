#!/usr/bin/python
import os
from database_manager import DatabaseManager

class ClrmameproDatfile():
    database_manager = None

    def __init__(self):
        self.clear()
        self.database_manager = DatabaseManager.Instance()

    def set_profile(self, profile=os.path.join(os.path.expanduser("~"), ".datman")):
        print("Profile Location: %s" % profile)
        self.database_manager.connect(profile)

    def clear(self):
        self.datfile_id    = None
        self.header        = None
        self.force_merging = None
        self.force_no_dump = None
        self.force_packing = None

    def save(self):
        if self.id == None:
            self.save_new()
        else:
            self.save_edit()

    def save_new(self):
        statement = '''INSERT INTO clrmamepro_datfile
                            (datfile_id,
                             header,
                             force_merging,
                             force_no_dump,
                             force_packing)
                     values
                            (?,?,?,?,?)'''
        params = (self.datfile_id,
                  self.header,
                  self.force_merging,
                  self.force_no_dump,
                  self.force_packing)
        self.id = self.database_manager.execute_statement_get_id(statement, params)

    def save_edit(self):
        statement = '''UPDATE clrmamepro_datfile SET
                             header = ?,
                             force_merging = ?,
                             force_no_dump = ?,
                             force_packing = ?
                     WHERE
                             datfile_id = ?'''
        params = (self.force_packing,
                  self.header,
                  self.force_merging,
                  self.force_no_dump,
                  self.datfile_id)
        self.id = self.database_manager.execute_statement_get_id(statement, params)

    def get_by_id(self):
        statement = "SELECT * FROM clrmamepro_datfile WHERE datfile_id = ?"
        params = (self.datfile_id,)
        clrmamepro_datfile = self.database_manager.execute_statement(statement, params)[0]
        self.datfile_id = clrmamepro_datfile[0]
        self.header = clrmamepro_datfile[1]
        self.force_merging = clrmamepro_datfile[2]
        self.force_no_dump = clrmamepro_datfile[3]
        self.force_packing = clrmamepro_datfile[4]
