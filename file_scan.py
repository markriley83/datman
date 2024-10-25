#!/usr/bin/python
import os, sys, argparse, fnmatch, zipfile
from StringIO import StringIO
from database_manager import DatabaseManager
from hash import Hash
from file import File
from archived_file import ArchivedFile
from file_dump_root import FileDumpRoot

class FileScan():

    def __init__(self):
        self.hash = Hash()

    def connect_database(self, profile=os.path.join(os.path.expanduser("~"), ".datman")):
        self.database = DatabaseManager.Instance()
        self.database.connect(profile)

    def disconnect_database(self):
        self.database.close()
        self.database = None

    def scan(self):
        file_dump_root = FileDumpRoot()
        file_dump_root.path = self.file_root
        file_dump_root.get_by_path()
        if file_dump_root.id == None:
            file_dump_root.save()
            self.database.write_db()
        for root, dirnames, filenames in os.walk(file_dump_root.path):
            print("Scanning %s" %  file_dump_root.path)
            for filename in filenames:
                print("Found file: %s" % filename)
                self.analyse_file(root, filename, file_dump_root)

    def analyse_file(self, root, filename, file_dump_root):
        file = File()
        with open(os.path.join(root, filename), 'rb') as fh:
            file.file_dump_root_ref = file_dump_root.id
            file.filepath = root.replace(file_dump_root.path, '')
            file.filename = filename
            if (fnmatch.fnmatch(filename, '*.zip')):
                file.is_container = True
            else:
                file.is_container = False
            file.size = os.stat(os.path.join(root, filename)).st_size
            file.get_by_visible()
            if file.id == None:
                self.hash.file = fh
                self.hash.get_hashes()
                file.crc32 = self.hash.crc32
                file.md5 = self.hash.md5
                file.sha1 = self.hash.sha1
                file.save()
                if file.is_container:
                    self.scan_in_zipfile(zipfile.ZipFile(os.path.join(root, filename)), file.id, file_dump_root)

    def scan_in_zipfile(self, zipfile_handle, container_id, file_dump_root):
        for zipped_file in zipfile_handle.namelist():
            print("Found file: %s" % zipped_file)
            zfile = File()
            zfile.file_dump_root_ref = file_dump_root.id
            zfile.filepath = ""
            zfile.filename = zipped_file
            if (fnmatch.fnmatch(zipped_file, '*.zip')):
                zfile.is_container = True
            else:
                zfile.is_container = False
            zfile.size = zipfile_handle.getinfo(zipped_file).file_size
            self.hash.file = zipfile_handle.open(zipped_file)
            self.hash.get_hashes()
            zfile.crc32 = self.hash.crc32
            zfile.md5 = self.hash.md5
            zfile.sha1 = self.hash.sha1
            zfile.save()
            archived_file = ArchivedFile()
            archived_file.file_id = zfile.id
            archived_file.container_id = container_id
            archived_file.save()
            if zfile.is_container:
                self.scan_in_zipfile(zipfile.ZipFile(StringIO(zipfile_handle.read(zipped_file))), zfile.id, file_dump_root)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Scan a directory for files")
    parser.add_argument("-p", "--profile", help="Datman profile")
    parser.add_argument("-r", "--file-root", help="Root directory to scan")
    args = parser.parse_args()
    if args.file_root:
        file_root = args.file_root
    else:
        file_root = os.path.join(os.path.join(os.path.expanduser("~"), "datman"), "to_sort")
    if args.profile:
        profile = args.profile
    else:
        profile = os.path.join(os.path.expanduser("~"), ".datman")
    if not os.path.exists(profile):
        print("Settings directory does not exist. Please run database_manager.py")
        sys.exit(1)
    if not os.path.exists(file_root):
        os.makedirs(file_root)
    filescan = FileScan()
    filescan.connect_database(profile)
    filescan.file_root = file_root
    filescan.scan()
    filescan.disconnect_database()
