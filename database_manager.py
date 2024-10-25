#!/usr/bin/python
import sqlite3, os, argparse
from singleton import Singleton

@Singleton
class DatabaseManager():
    cursor = None
    conn = None

    def connect(self, profile=os.path.join(os.path.expanduser("~"), ".datman")):
        print("Profile Location: %s" % profile)
        self.conn = sqlite3.connect(profile)
        self.cursor = self.conn.cursor()

    def write_db(self):
        self.conn.commit()

    def close(self):
        self.write_db()
        self.conn.close()

    def setup_database(self):
        print("Creating database tables from file.")
        with open('database.sql', 'r') as fh:
            sql = fh.read()
            self.cursor.executescript(sql)
        self.write_db()
        print("Database table creation complete.")

    def execute_statement_get_id(self, statement, params):
        self.cursor.execute(statement, params)
        return self.cursor.lastrowid

    def execute_statement(self, statement, params):
        self.cursor.execute(statement, params)
        return self.cursor.fetchall()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Set up profile for datman")
    parser.add_argument("-p", "--profile", help="Datman profile")
    args = parser.parse_args()
    if args.profile:
        profile = args.profile
    else:
        profile = os.path.join(os.path.expanduser("~"), ".datman")
    if not os.path.exists(profile):
        database = DatabaseManager.Instance()
        database.connect(profile)
        database.setup_database()
        database.close()
    else:
        print("Profile already exists")
