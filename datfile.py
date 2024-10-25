#!/usr/bin/python
import os
from database_manager import DatabaseManager

class Datfile():
    database_manager = None

    def __init__(self):
        self.clear()
        self.database_manager = DatabaseManager.Instance()

    def set_profile(self, profile=os.path.join(os.path.expanduser("~"), ".datman")):
        print("Profile Location: %s" % profile)
        self.database_manager.connect(profile)

    def clear(self):
        self.id               = None
        self.datfile_root_ref = None
        self.filepath         = None
        self.filename         = None
        self.size             = None
        self.crc32            = None
        self.md5              = None
        self.sha1             = None
        self.name             = None
        self.description      = None
        self.category         = None
        self.version          = None
        self.date             = None
        self.author           = None
        self.homepage         = None
        self.url              = None
        self.comment          = None

    def save(self):
        if self.id == None:
            self.save_new()
        else:
            self.save_edit()

    def save_new(self):
        statement = '''INSERT INTO datfile
                            (datfile_root_ref,
                             filepath,
                             filename,
                             size,
                             crc32,
                             md5,
                             sha1,
                             name,
                             description,
                             category,
                             version,
                             date,
                             author,
                             homepage,
                             url,
                             comment)
                     values
                            (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
        params = (self.datfile_root_ref,
                  self.filepath,
                  self.filename,
                  self.size,
                  self.crc32,
                  self.md5,
                  self.sha1,
                  self.name,
                  self.description,
                  self.category,
                  self.version,
                  self.date,
                  self.author,
                  self.homepage,
                  self.url,
                  self.comment)
        self.id = self.database_manager.execute_statement_get_id(statement, params)

    def save_edit(self):
        statement = '''UPDATE datfile SET
                             datfile_root_ref = ?,
                             filepath = ?,
                             filename = ?,
                             size = ?,
                             crc32 = ?,
                             md5 = ?,
                             sha1 = ?,
                             name = ?,
                             description = ?,
                             category = ?,
                             version = ?,
                             date = ?,
                             author = ?,
                             homepage = ?,
                             url = ?,
                             comment = ?
                     WHERE
                             id = ?'''
        params = (self.datfile_root_ref,
                  self.filepath,
                  self.filename,
                  self.size,
                  self.crc32,
                  self.md5,
                  self.sha1,
                  self.name,
                  self.description,
                  self.category,
                  self.version,
                  self.date,
                  self.author,
                  self.homepage,
                  self.url,
                  self.comment,
                  self.id)
        self.id = self.database_manager.execute_statement_get_id(statement, params)

    def get_by_id(self):
        statement = "SELECT * FROM datfile WHERE id = ?"
        params = (self.id,)
        datfile = self.database_manager.execute_statement(statement, params)[0]
        self.id = datfile[0]
        self.datfile_root_ref = datfile[1]
        self.filepath = datfile[2]
        self.filename = datfile[3]
        self.size = datfile[4]
        self.crc32 = datfile[5]
        self.md5 = datfile[6]
        self.sha1 = datfile[7]
        self.name = datfile[8]
        self.description = datfile[9]
        self.category = datfile[10]
        self.version = datfile[11]
        self.date = datfile[12]
        self.author = datfile[13]
        self.homepage = datfile[14]
        self.url = datfile[15]
        self.comment = datfile[16]

    def get_by_attributes(self):
        statement = '''SELECT * FROM datfile WHERE
                             filename = ? AND
                             size = ? AND
                             crc32 = ? AND
                             md5 = ? AND
                             sha1 = ?'''
        params = (self.filename, self.size, self.crc32, self.md5, self.sha1)
        datfile = self.database_manager.execute_statement(statement, params)
        if len(datfile) > 0:
            self.id = datfile[0][0]
            self.datfile_root_ref = datfile[0][1]
            self.filepath = datfile[0][2]
            self.filename = datfile[0][3]
            self.size = datfile[0][4]
            self.crc32 = datfile[0][5]
            self.md5 = datfile[0][6]
            self.sha1 = datfile[0][7]
            self.name = datfile[0][8]
            self.description = datfile[0][9]
            self.category = datfile[0][10]
            self.version = datfile[0][11]
            self.date = datfile[0][12]
            self.author = datfile[0][13]
            self.homepage = datfile[0][14]
            self.url = datfile[0][15]
            self.comment = datfile[0][16]
