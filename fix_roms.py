#!/usr/bin/python
import os, argparse, zipfile, shutil
from database_manager import DatabaseManager
from match import Match
from rom import Rom
from file import File
from archived_file import ArchivedFile
from file_dump_root import FileDumpRoot
from game import Game
from datfile import Datfile
from datfile_root import DatfileRoot
from rebuild_location import RebuildLocation
from tempfile import NamedTemporaryFile, TemporaryFile
from StringIO import StringIO

class FixRoms():

    def connect_database(self, profile=os.path.join(os.path.expanduser("~"), ".datman")):
        self.database = DatabaseManager.Instance()
        self.database.connect(profile)

    def disconnect_database(self):
        self.database.close()
        self.database = None

    def fix_roms(self):
        matches = Match.get_all_matches()
        for match in matches:
            rom = Rom()
            rom.id = match.rom_id
            rom.get_by_id()
            file = File()
            file.id = match.file_id
            file.get_by_id()
            file_dump_root = FileDumpRoot()
            file_dump_root.id = file.file_dump_root_ref
            file_dump_root.get_by_id()
            game = Game()
            game.id = rom.game_id
            game.get_by_id()
            datfile = Datfile()
            datfile.id = game.datfile_id
            datfile.get_by_id()
            datfile_root = DatfileRoot()
            datfile_root.id = datfile.datfile_root_ref
            datfile_root.get_by_id()
            rebuild_location = RebuildLocation()
            rebuild_location.id = datfile_root.rebuild_location_ref
            rebuild_location.get_by_id()

            systemdir = rebuild_location.path + datfile.filepath
            systemdir = os.path.join(systemdir, datfile.name)

            fixname = "%s.zip" % (os.path.join(systemdir, game.name))
            if not os.path.exists(systemdir):
                os.makedirs(systemdir)
            print("Fixing %s - %s. Adding %s" % (datfile.name, game.name, rom.name))
            fixfile = zipfile.ZipFile(fixname, 'a')
            if not rom.name in fixfile.namelist():
                print("fix that file")
                archived_file = ArchivedFile()
                archived_file.file_id = file.id
                is_archive = archived_file.get_by_file_id()
                if is_archive:
                    print("File is in an archive, lets get it out")
                    container = File()
                    container.id = archived_file.container_id
                    container.get_by_id()
                    sortzip = zipfile.ZipFile(os.path.join(file_dump_root.path + container.filepath, container.filename))
                    fixfile.writestr(rom.name, sortzip.read(file.filename))
                else:
                    print("File is out in the open. Fix")
                    fixfile.write(os.path.join(file_dump_root.path + file.filepath, file.filename), rom.name)
            else:
                print("That rom is already there")
            fixfile.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Fix roms based on matches found.")
    parser.add_argument("-p", "--profile", help="Datman profile")
    args = parser.parse_args()
    if args.profile:
        profile = args.profile
    else:
        profile = os.path.join(os.path.expanduser("~"), ".datman")
    if not os.path.exists(profile):
        print("Settings directory does not exist. Please run database_manager.py")
        sys.exit(1)
    fix_roms = FixRoms()
    fix_roms.connect_database(profile)
    fix_roms.fix_roms()
    fix_roms.disconnect_database()
