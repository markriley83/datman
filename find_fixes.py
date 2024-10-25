#!/usr/bin/python
import os, argparse
from database_manager import DatabaseManager
from file import File
from rom import Rom
from match import Match

class FindFixes():

    def connect_database(self, profile=os.path.join(os.path.expanduser("~"), ".datman")):
        self.database = DatabaseManager.Instance()
        self.database.connect(profile)

    def disconnect_database(self):
        self.database.close()
        self.database = None

    def find_fixes(self):
        roms = Rom.get_all_roms()
        for rom in roms:
            file = File()
            file.size = rom.size
            file.crc32 = rom.crc32
            file.md5 = rom.md5
            file.sha1 = rom.sha1
            file_list = file.get_list_by_available_attributes()
            for found_file in file_list:
                print("Found %s in %s" % (rom.name, found_file.filename))
                match = Match()
                match.file_id = found_file.id
                match.rom_id = rom.id
                match.get_by_files()
                if match.id == None:
                    match.save()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Find fixes in the database")
    parser.add_argument("-p", "--profile", help="Datman profile")
    args = parser.parse_args()
    if args.profile:
        profile = args.profile
    else:
        profile = os.path.join(os.path.expanduser("~"), ".datman")
    if not os.path.exists(profile):
        print("Settings directory does not exist. Please run database_manager.py")
        sys.exit(1)
    find_fixes = FindFixes()
    find_fixes.connect_database(profile)
    find_fixes.find_fixes()
    find_fixes.disconnect_database()
