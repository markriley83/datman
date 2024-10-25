#!/usr/bin/python
import os, sys, argparse, magic, re
from lxml import etree
from database_manager import DatabaseManager
from rebuild_location import RebuildLocation
from datfile_root import DatfileRoot
from datfile import Datfile
from game import Game
from rom import Rom
from hash import Hash

class DatfileScan():

    def __init__(self):
        self.hash = Hash()

    def connect_database(self, profile=os.path.join(os.path.expanduser("~"), ".datman")):
        self.database = DatabaseManager.Instance()
        self.database.connect(profile)

    def disconnect_database(self):
        self.database.close()
        self.database = None

    def scan(self):
        rebuild_location = RebuildLocation()
        rebuild_location.path = self.file_root
        rebuild_location.get_by_path()
        if rebuild_location.id == None:
            rebuild_location.save()
            self.database.write_db()
        datfile_root = DatfileRoot()
        datfile_root.path = self.datfile_root
        datfile_root.rebuild_location_ref = rebuild_location.id
        datfile_root.get_by_path()
        if datfile_root.id == None:
            datfile_root.save()
            self.database.write_db()
        for root, dirnames, filenames in os.walk(datfile_root.path):
            for filename in filenames:
                print("scanning %s" % filename)
                if magic.from_file(os.path.join(root, filename), mime=True).decode("utf-8") == "application/xml":
                    print("MIME type: application/xml")
                    self.scanxml(root, filename, datfile_root)
                else:
                    print("file is not XML. Checking other file types.")
                    with open(os.path.join(root, filename), 'r') as fh:
                        first_line = fh.readline()
                        if re.search("clrmamepro", first_line):
                            print("We have a clrmamepro datfile")
                            #self.scanclrmamepro(fh)
                        else:
                            print("Unknown file type.")

    def scanxml(self, filepath, filename, datfile_root):
        system = None
        context = etree.iterparse(os.path.join(filepath, filename), events=('end',))
        try:
            for event, elem in context:
                if elem.tag == 'header':
                    system = self.build_system(event, elem, filepath, filename, datfile_root)
                    if system == -1:
                        return
                if elem.tag == 'game':
                    game = self.build_game(event, elem, system)
        except etree.XMLSyntaxError:
            print(context)

    def scanclrmamepro(self, fh):
        system = Datfile()
        game = None
        rom = None
        for line in fh:
            if line.strip() == ')':
                if not game:
                    print("Save a System")
                else:
                    print("Save a Game")
                    game = None
                continue
            if line.strip() == '':
                continue
            if re.search("^game", line.strip()):
                game = Game()
                continue
            elif  re.search("^rom", line.strip()):
                rom = Rom()
                print("Save a Rom")
                rom = None
                continue
            key, value = line.strip().split(" ", 1)
            if not game:
                if key == 'name':
                    print("Name: %s" % value[1:-1])
                elif key == 'description':
                    print("Desc: %s" % value[1:-1])
                elif key == 'category':
                    print("Ctgy: %s" % value[1:-1])
                elif key == 'version':
                    print("vrsn: %s" % value)
                elif key == 'author':
                    print("athr: %s" % value[1:-1])
            else:
                if key == 'name':
                    print("Name: %s" % value[1:-1])
                elif key == 'description':
                    print("Desc: %s" % value[1:-1])

    def build_system(self, event, elem, filepath, filename, datfile_root):
        system = Datfile()
        for child in elem.getchildren():
            if child.tag == 'name':
                print("Found system: %s" % child.text)
                system.name = child.text
            if child.tag == 'description':
                system.description = child.text
            if child.tag == 'version':
                system.version = child.text
            if child.tag == 'date':
                system.date = child.text
            if child.tag == 'author':
                system.author = child.text
            if child.tag == 'homepage':
                system.homepage = child.text
            if child.tag == 'url':
                system.url = child.text
            if child.tag == 'comment':
                system.comment = child.text
        system.datfile_root_ref = datfile_root.id
        system.filename = filename
        system.filepath = filepath.replace(datfile_root.path, '')
        with open(os.path.join(filepath, filename), 'rb') as fh:
            system.size = os.stat(os.path.join(filepath, filename)).st_size
            self.hash.file = fh
            self.hash.get_hashes()
            system.crc32 = self.hash.crc32
            system.md5 = self.hash.md5
            system.sha1 = self.hash.sha1
        system.get_by_attributes()
        if system.id == None:
            system.save()
            self.database.write_db()
            return system
        else:
            print("Datfile is already in Database.")
            return -1

    def build_game(self, event, elem, system):
        game = Game()
        print("Found game: %s" % elem.get("name"))
        game.name = elem.get("name")
        game.datfile_id = system.id
        for child in elem.getchildren():
            if child.tag == 'description':
                game.description = child.text
        game.save()
        for child in elem.getchildren():
            if child.tag == 'rom':
                rom = self.build_rom(child, game)
        return game

    def build_rom(self, elem, game):
        rom = Rom()
        print("Found rom: %s" % elem.get("name"))
        rom.name = elem.get("name")
        rom.size = elem.get("size")
        if elem.get("crc"):
            rom.crc32 = elem.get("crc")
        if elem.get("md5"):
            rom.md5 = elem.get("md5")
        if elem.get("sha1"):
            rom.sha1 = elem.get("sha1")
        rom.game_id = game.id
        rom.save()
        return rom


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Scan a directory for datfiles")
    parser.add_argument("-p", "--profile", help="Datman profile")
    parser.add_argument("-r", "--datfile-root", help="Root directory to scan")
    parser.add_argument("-f", "--file-root", help="Rebuild directory")
    args = parser.parse_args()
    if args.datfile_root:
        datfile_root = args.datfile_root
    else:
        datfile_root = os.path.join(os.path.join(os.path.expanduser("~"), "datman"), "datfiles")
    if args.file_root:
        file_root = args.file_root
    else:
        file_root = os.path.join(os.path.join(os.path.expanduser("~"), "datman"), "romdir")
    if args.profile:
        profile = args.profile
    else:
        profile = os.path.join(os.path.expanduser("~"), ".datman")
    if not os.path.exists(profile):
        print("Settings directory does not exist. Please run database_manager.py")
        sys.exit(1)
    if not os.path.exists(datfile_root):
        os.makedirs(datfile_root)
    datscan = DatfileScan()
    datscan.connect_database(profile)
    datscan.datfile_root = datfile_root
    datscan.file_root = file_root
    datscan.scan()
    datscan.disconnect_database()
