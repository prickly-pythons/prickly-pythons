# Python program For
# Birthday Reminder Application
 
import time
import os
import pdb
import pandas as pd
import subprocess

root = '/Users/Karen/code/birthdays/'

birthdayFile = root+'list_of_dates'
taken_care_of_file = root+'taken_care_of_list'

# Weeks to look ahead in time:
weeks           =   3

def checkTodaysBirthdays():
    # Load permanent list of birthdays and names
    list_of_dates       =   pd.read_table(birthdayFile, skiprows=2, sep='\t', names=['dates','names'], engine='python')
    months              =   [int(_.split(' ')[0]) for _ in list_of_dates['dates']]
    days                =   [int(_.split(' ')[1]) for _ in list_of_dates['dates']]
    names               =   list_of_dates['names'].values
    month_today         =   int(time.strftime('%m'))
    day_today           =   int(time.strftime('%d'))

    # Load list of birthdays taken care off:
    taken_care_of_list  =   pd.read_table(taken_care_of_file+'.txt', names=['names'], engine='python')['names'].values

    # Go through permanent list
    notifications       =   0
    for month,day,name in zip(months,days,names):

        if name not in taken_care_of_list:

            if month == month_today:
                if day == day_today:
                    notify(keep=True,title="There's a birthday today!",subtitle=name,message='date: %s-%s' % (month,day),name=name)
                    remove_from_taken_care_off_list(name)
                    notifications       +=   0

                if 0 < day - day_today < weeks*7.:
                    notify(keep=True,title="Birthday in the near future!",subtitle='Get ready for... '+name+'!',message='date: %s-%s' % (month,day),name=name)
                    notifications       +=   0

            # Check for birthdays hiding in next month
            if month != month_today:
                if month == month_today+1:
                    if 30-day_today + day < weeks*7.:
                        notify(keep=True,title="Birthday in the near future!",subtitle='Get ready for... '+name+'!',message='date: %s-%s' % (month,day),name=name)
                        notifications       +=   0

    if notifications > 0:
        notify(keep=False,title="No Birthdays in the near future!",subtitle='keep working',message='... and keep it hot')

def notify(keep=False,title='',subtitle='',message='',name=''):

    if keep: 
        create_notify_script(title, subtitle, message)
        os.system('chmod 777 '+root+'notify_script.sh')
        result = subprocess.Popen([''+root+'notify_script.sh'], shell=True, stdout=subprocess.PIPE)
        out = result.communicate()
        if 'Noworries' in out[0] or 'Taken' in out[0]:
            # Taking this name out of this years list
            add_to_taken_care_off_list(name)
        # else: Will remind again tomorrow

    if not keep: 
        os.system('terminal-notifier -title "%s" -subtitle "%s" -message "%s"' % (title,subtitle,message))

def create_notify_script(title, subtitle, message):
    # Installed Alerter program from https://github.com/vjeantet/alerter

    script_out          =    open(root+'notify_script.sh','w')
    script_out.write('ANSWER="$('+root+'alerter -title "%s" -subtitle "%s" -message "%s" -actions "Taken care of","Need to get gift","No worries")"' % (title,subtitle,message) )
    script_out.write('\ncase $ANSWER in')
    script_out.write('\n    "@CLOSED") echo "You clicked on the default alert close button" ;;')
    script_out.write('\n    "@CONTENTCLICKED") echo "You clicked the alert content !" ;;')
    script_out.write('\n    "@ACTIONCLICKED") echo "You clicked the alert default action button" ;;')
    script_out.write('\n    "Taken care off") echo "Action Taken" ;;')
    script_out.write('\n    "Need to get gift") echo "Action Need" ;;')
    script_out.write('\n    "No worries") echo "Action Noworries" ;;')
    script_out.write('\n    **) echo "? --> $ANSWER" ;;')
    script_out.write('\nesac')
    
    script_out.close()

def add_to_taken_care_off_list(name):

    os.system('cp '+taken_care_of_file+'.txt '+taken_care_of_file+'_temp'+'.txt')
    script_in           =    open(taken_care_of_file+'_temp'+'.txt','r')
    script_out          =    open(taken_care_of_file+'.txt','w')

    # Copy last version of this file
    for line in script_in:
        script_out.write(line)

    # Add new names
    script_out.write(name+'\n')

    script_in.close()
    script_out.close()
    os.system('rm '+taken_care_of_file+'_temp'+'.txt')

def remove_from_taken_care_off_list(name):

    os.system('cp '+taken_care_of_file+'.txt '+taken_care_of_file+'_temp'+'.txt')
    script_in           =    open(taken_care_of_file+'_temp'+'.txt','r')
    script_out          =    open(taken_care_of_file+'.txt','w')

    # Copy last version of this file
    for line in script_in:
        if line != name+'\n': script_out.write(line)

    script_in.close()
    script_out.close()
    os.system('rm '+taken_care_of_file+'_temp'+'.txt')

# To run as shell script
if __name__ == '__main__':
    checkTodaysBirthdays()


    