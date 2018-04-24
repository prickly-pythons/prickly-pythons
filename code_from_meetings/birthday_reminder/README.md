# Birthday Reminder

Creates a notification box in the top right corner of the screen with the following options if someone has a birthday today (or one that is coming up within the next 3 weeks):
- close (ignore)
- Taken care of
- Need to get gift
- No worries

## Responsible
Karen Olsen, last edits: April 24 2018

## Requirements
Mac OS (tested on 10.13.1)
Python v 2.7.14 or above

## How to use:
Edit the "root" variable in birthday_reminder.py to where this folder is located on your laptop:
```
root = '/Users/Karen/code/birthdays/'
```
Edit the following line in the birthday_script shell script to fit where python is located and "root":
```
/Users/Karen/anaconda2/bin/python2 /Users/Karen/code/birthdays/birthday_reminder.py
```
Run on command line with:
```
./birthday_script
```

## Updates that might be added:
- Class structure to make it easier to edit/add/delete birthdays.
- Setting up ad launch daemon with [LaunchControl](http://www.soma-zone.com/LaunchControl/) to execute the shell script everyday at a certain time.
