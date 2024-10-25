datman
======

Free ROM manager written in Python

About
=====

There are plenty of ROM managers out there (Clrmamepro, Romulus,
ROM Vault) however these are all designed to run on Microsoft Windows.
Secondly, these all appear to be closed source, which doesn't help the
community, nor does it help with porting these across to other
platforms.

Therefore I started this project. Hopefully it will achieve one of two
goals:

 1. Encourage other ROM managers to have their source released, to
    encourage community participation in their development.

 2. Become a mature and useful tool in its own right.

Python was chosen as the language of choice. I admit, this is largely an
exercise to help me learn Python (I am more experienced with other
programming languages such as C, C++ and Java), but my understanding is
that Python should be more than capable of performing these tasks in an
appropriate manner.

Getting the Code
================

You can simply check out the code by typing the following into a
terminal:

    git clone https://github.com/eighthpence/datman.git

Contributing
============

All contributions are welcome. You are, of course, encouraged to create
a fork off the code. The following URI should link to that:

    https://github.com/eighthpence/datman/fork

You may send me pull requests using the button on:

    https://github.com/eighthpence/datman

All requests will be considered, but may not be accepted. If there is a
rejected request, I will do my best to let you know why, and how to
possibly amend your submission for acceptance.

If you need help using Git, I recommend reading through Scott Chahon's
ProGit book.

    http://git-scm.com/book

It took me about an evening to read through and I am a terrible reader.

Not all contributions are related to code. Feedback and suggestions are
helpful too, as well as artwork, moral support, compliments and donation
of resources. Monetary donations are not currently accepted.

I don't currently have a home for this project, so nowhere really to
discuss the above. Hopefully somewhere will take me in and give me a
forum for discussion (this could be seen as donating resources, as
mentioned above).

As mentioned I don't really have any reason to accept money for this
project as this is just a hobby, and there are other projects that need
it a lot more, such as cancer, AIDS, meningitis and cold fusion
research, not to mention those living in poverty.

Installation
============

Currently there is no way of installing. Just download and run. This
might change in the future.

Running
=======

This application is designed to run as a sort of toolkit. A GUI has been
included, but everything is designed to run from the command line.

For the GUI, run datman.py

    python datman.py

Options can be set. To see options, just run:

    python datman.py -h

Options are described better via the command line utilities.

The commands that can be run are:

    python database_manager.py
    python file_scan.py
    python datfile_scan.py
    python find_fixes.py
    python fix_roms.py

Doing this in this order will sort you out fine. A series of directories
should appear in your home directory (~/.datman and ~/datman). .datman
contains the database and future settings file. datman will contain user
files.

    datman/datfiles - put your datfiles here
    datman/romdir - this is where your files will be rebuilt
    datman/to_sort - put your files to be sorted here

All of the locations can be changed.

    python database_manager.py -s <settingsdir> -d <dbname>
    python file_scan.py -r <filedir> -s <settingsdir> -d <dbname>
    python datfile_scan.py -r <datdir> -s <settingsdir> \
                           -d <dbname> -f <rebuildroot>
    python find_fixes.py -s <settingsdir> -d <dbname>
    python fix_roms.py -s <settingsdir> -d <dbname>

The -h switch can be added to any command to bring up the help
descriptions.
