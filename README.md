# pySearchPassDB
Write data to the database and search for a password by email on this database.
## How to use
Search for passwords by email.
```
python pySearchPassDB.py -s example@example.com
python pySearchPassDB.py --search example@example.com
```
Add fields to the database from files. The lines in the file must be in the format email:password. Specifies the path to the folder where these files are with passwords. All files and subdirectories are parsed.
```
python pySearchPassDB.py -a "path/to/dir"
python pySearchPassDB.py --add "path/to/dir"
```
Show count fileds of db.
```
python pySearchPassDB.py -c
python pySearchPassDB.py --count
```
Clear all db fields.
```
python pySearchPassDB.py --clear
```