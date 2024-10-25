CREATE TABLE rebuild_location
  (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path TEXT
  );

CREATE TABLE datfile_root
  (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path TEXT,
    rebuild_location_ref INTEGER,
    FOREIGN KEY (rebuild_location_ref) REFERENCES rebuild_location (id)
  );

CREATE TABLE file_dump_root
  (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path TEXT,
    priority INTEGER
  );

CREATE TABLE datfile
  (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    datfile_root_ref INTEGER,
    filepath TEXT,
    filename TEXT,
    size INTEGER,
    crc32 TEXT,
    md5 TEXT,
    sha1 TEXT,
    name TEXT,
    description TEXT,
    category TEXT,
    version TEXT,
    date TEXT,
    author TEXT,
    homepage TEXT,
    url TEXT,
    comment TEXT,
    FOREIGN KEY (datfile_root_ref) REFERENCES datfile_root (id)
  );

CREATE TABLE clrmamepro_datfile
  (
    datfile_id INTEGER PRIMARY KEY,
    header TEXT,
    force_merging TEXT,
    force_no_dump TEXT,
    force_packing TEXT,
    FOREIGN KEY (datfile_id) REFERENCES datfile (id)
  );

CREATE TABLE romcenter_datfile
  (
    datfile_id INTEGER PRIMARY KEY,
    plugin TEXT,
    rom_mode TEXT,
    bios_mode TEXT,
    sample_mode TEXT,
    lock_rom_mode TEXT,
    lock_bios_mode TEXT,
    lock_sample_mode TEXT,
    FOREIGN KEY (datfile_id) REFERENCES datfile (id)
  );

CREATE TABLE game
  (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    comment TEXT,
    description TEXT,
    year TEXT,
    manufacturer TEXT,
    name TEXT,
    source_file TEXT,
    is_bios TEXT,
    clone_of TEXT,
    sample_of TEXT,
    board TEXT,
    rebuild_to TEXT,
    datfile_id INTEGER,
    FOREIGN KEY (datfile_id) REFERENCES datfile (id)
  );

CREATE TABLE release
  (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    region TEXT,
    language TEXT,
    date TEXT,
    'default' TEXT,
    game_id INTEGER,
    FOREIGN KEY (game_id) REFERENCES game (id)
  );

CREATE TABLE bios_set
  (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    description TEXT,
    'default' TEXT,
    game_id INTEGER,
    FOREIGN KEY (game_id) REFERENCES game (id)
  );

CREATE TABLE rom
  (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    size INTEGER,
    crc32 TEXT,
    md5 TEXT,
    sha1 TEXT,
    merge TEXT,
    status TEXT,
    date TEXT,
    game_id INTEGER,
    FOREIGN KEY (game_id) REFERENCES game (id)
  );

CREATE TABLE disk
  (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    md5 TEXT,
    sha1 TEXT,
    merge TEXT,
    status TEXT,
    game_id INTEGER,
    FOREIGN KEY (game_id) REFERENCES game (id)
  );

CREATE TABLE sample
  (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    game_id INTEGER,
    FOREIGN KEY (game_id) REFERENCES game (id)
  );

CREATE TABLE archive
  (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    game_id INTEGER,
    FOREIGN KEY (game_id) REFERENCES game (id)
  );

CREATE TABLE file
  (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_dump_root_ref INTEGER,
    filepath TEXT,
    filename TEXT,
    is_container INTEGER,
    size INTEGER,
    crc32 TEXT,
    md5 TEXT,
    sha1 TEXT,
    FOREIGN KEY (file_dump_root_ref) REFERENCES file_dump_root (id)
  );

CREATE TABLE archived_file
  (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id INTEGER,
    container_id INTEGER,
    FOREIGN KEY (file_id) REFERENCES file (id),
    FOREIGN KEY (container_id) REFERENCES file (id)
  );

CREATE TABLE match
  (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id INTEGER,
    rom_id INTEGER,
    FOREIGN KEY (file_id) REFERENCES file (id),
    FOREIGN KEY (rom_id) REFERENCES file (id)
  );
