#!/usr/bin/python
import hashlib, sys, zlib, argparse

class Hash():
    file = None
    get_crc32 = True
    crc32 = None
    get_md5 = True
    md5 = None
    get_sha1 = True
    sha1 = None
    block_size = 8192

    def reset(self):
        self.file = None
        self.get_crc32 = True
        self.crc32 = None
        self.get_md5 = True
        self.md5 = None
        self.get_sha1 = True
        self.sha1 = None
        self.block_size = 8192

    def get_hashes(self):
        if self.get_crc32:
            crc32 = 0
        if self.get_md5:
            md5 = hashlib.md5()
        if self.get_sha1:
            sha1 = hashlib.sha1()
        for data in iter(lambda: self.file.read(self.block_size), b''):
            if self.get_crc32:
                crc32 = zlib.crc32(data, crc32)
            if self.get_md5:
                md5.update(data)
            if self.get_sha1:
                sha1.update(data)
        if self.get_crc32:
            self.crc32 = "%08X" % (crc32 & 0xFFFFFFFF)
        if self.get_md5:
            self.md5 = md5.hexdigest().upper()
        if self.get_sha1:
            self.sha1 = sha1.hexdigest().upper()

if __name__ == '__main__':
    hash = Hash()
    parser = argparse.ArgumentParser(description="Find the CRC32, MD5 and SHA1 from a file at once.")
    parser.add_argument("-f", "--file", help="File to be processed", required=True)
    parser.add_argument("--no-crc32", help="Do not require CRC32", action="store_true")
    parser.add_argument("--no-md5", help="Do not require MD5", action="store_true")
    parser.add_argument("--no-sha1", help="Do not require SHA1", action="store_true")
    parser.add_argument("-b", "--blocksize", help="Blocksize. Default 8192", type=int)
    args = parser.parse_args()
    if args.file:
        try:
            hash.file = open(args.file, 'rb')
        except FileNotFoundError:
            print("File not found")
            sys.exit(3)
    else:
        print("No filename supplied")
        sys.exit(1)
    if args.no_crc32:
        hash.get_crc32 = False
    if args.no_md5:
        hash.get_md5 = False
    if args.no_sha1:
        hash.get_sha1 = False
    if args.blocksize:
        hash.block_size = args.blocksize
    hash.get_hashes()
    if hash.get_crc32:
        print("CRC32: %s" % hash.crc32)
    if hash.get_md5:
        print("MD5: %s" % hash.md5)
    if hash.get_sha1:
        print("SHA1: %s" % hash.sha1)
    hash.file.close()
