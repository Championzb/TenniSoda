#!/bin/bash
./manage.py syncdb
./manage.py schemamigration account --initial
./manage.py schemamigration city --initial
./manage.py schemamigration court --initial
./manage.py schemamigration game --initial
./manage.py schemamigration notification --initial
./manage.py schemamigration review --initial
./manage.py schemamigration activity --initial
./manage.py migrate friendship
./manage.py migrate account --fake
./manage.py migrate city --fake
./manage.py migrate court --fake
./manage.py migrate game --fake
./manage.py migrate notification --fake
./manage.py migrate review --fake
./manage.py migrate activity --fake
