#!/usr/bin/python
import argparse, os
from gi.repository import Gtk
from database_manager import DatabaseManager
from file_scan import FileScan
from datfile_scan import DatfileScan
from find_fixes import FindFixes
from fix_roms import FixRoms

class Datman:
    settings_dir = None
    database_file = None
    file_root = None
    datfile_base = None
    build_root = None

    def __init__(self):
        self.glade = "datman.glade"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.glade)
        self.main_window = self.builder.get_object("mainWindow")
        self.update_dats_button = self.builder.get_object("updateDats")
        self.scan_roms_button = self.builder.get_object("scanRoms")
        self.find_fixes_button = self.builder.get_object("findFixes")
        self.fix_roms_button = self.builder.get_object("fixRoms")
        self.do_all_button = self.builder.get_object("doAll")
        if self.main_window:
            self.main_window.connect("destroy", Gtk.main_quit)
        if self.update_dats_button:
            self.update_dats_button.connect("clicked", self.update_dats)
        if self.scan_roms_button:
            self.scan_roms_button.connect("clicked", self.scan_roms)
        if self.find_fixes_button:
            self.find_fixes_button.connect("clicked", self.find_fixes)
        if self.fix_roms_button:
            self.fix_roms_button.connect("clicked", self.fix_roms)
        if self.do_all_button:
            self.do_all_button.connect("clicked", self.do_all)
        self.main_window.show()


    def update_dats(self, widget, data=None):
        datscan = DatfileScan()
        datscan.connect_database(self.profile)
        datscan.datfile_root = self.datfile_root
        datscan.file_root = self.build_root
        datscan.scan()
        datscan.disconnect_database()

    def scan_roms(self, widget, data=None):
        filescan = FileScan()
        filescan.connect_database(self.profile)
        filescan.file_root = file_root
        filescan.scan()
        filescan.disconnect_database()

    def find_fixes(self, widget, data=None):
        find_fixes = FindFixes()
        find_fixes.connect_database(self.profile)
        find_fixes.find_fixes()
        find_fixes.disconnect_database()

    def fix_roms(self, widget, data=None):
        fix_roms = FixRoms()
        fix_roms = FixRoms()
        fix_roms.connect_database(self.profile)
        fix_roms.fix_roms()
        fix_roms.disconnect_database()

    def do_all(self, widget, data=None):
        self.update_dats(widget, data)
        self.scan_roms(widget, data)
        self.find_fixes(widget, data)
        self.fix_roms(widget, data)

    def setup_environment(self):
        if not os.path.exists(self.profile):
            database = DatabaseManager.Instance()
            database.connect(self.profile)
            database.setup_database()
            database.close()

    def run(self):
        self.setup_environment()
        Gtk.main()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Set up database for datman")
    parser.add_argument("-p", "--profile", help="Datman profile")
    parser.add_argument("-r", "--datfile-root", help="Root directory to scan for datfiles")
    parser.add_argument("-f", "--file-root", help="Root directory to scan for roms")
    parser.add_argument("-b", "--build-root", help="Root directory to rebuild to")
    args = parser.parse_args()
    if args.profile:
        profile = args.profile
    else:
        profile = os.path.join(os.path.expanduser("~"), ".datman")
    if args.datfile_root:
        datfile_root = args.datfile_root
    else:
        datfile_root = os.path.join(os.path.join(os.path.expanduser("~"), "datman"), "datfiles")
    if args.file_root:
        file_root = args.file_root
    else:
        file_root = os.path.join(os.path.join(os.path.expanduser("~"), "datman"), "to_sort")
    if args.build_root:
        build_root = args.build_root
    else:
        build_root = os.path.join(os.path.join(os.path.expanduser("~"), "datman"), "romdir")
    datman = Datman()
    datman.profile = profile
    datman.file_root = file_root
    datman.datfile_root = datfile_root
    datman.build_root = build_root
    datman.run()
