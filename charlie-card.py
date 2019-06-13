#!/usr/bin/python

import os, sys, getopt, datetime

# Write val to the charlie card text file
# Val must be a float
def write_to_file(val,info):
   f = open('charlie_card.txt','w')
   f.write(str(val) + os.linesep)
   f.write(info)
   f.close

# Print the possible arguments
def print_info():
   print('-h : help')
   print('-r : remove a fare')
   print('-a : # add specified value')
   print('-d : Diplay current balance')

def get_data():
   # Get the charlie card value from the text file
   f = open('charlie_card.txt','r')
   balance = float(f.readline())
   info = f.readline()
   f.close()
   return balance,info

def print_balance(balance):
   print("Balance: {}".format(balance))

def add_leading_zero(val):
    if val < 10:
        val = str("0{}".format(val))
    return val

def get_date_time():
    now = datetime.datetime.now()

    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute
    second = now.second

    if hour > 12:
       hour = hour - 12
       label = "PM"
    elif hour == 12:
       label = "PM"
    else:
       label = "AM"

    hour = add_leading_zero(hour)
    minute = add_leading_zero(minute)
    month = add_leading_zero(month)
    day = add_leading_zero(day)
    second = add_leading_zero(second)

    date_time = str("{}/{}/{} | {}:{}:{} {}".format(now.year,month,day,hour,minute,second,label))
    #print(date_time)
    return date_time

def create_log_entry(date_time,action):
    f = open('charlie_log.txt','a')
    f.write(os.linesep)
    f.write(date_time + ', ' + action)

def summarize_log():
    f = open('charlie_log.txt','r')
    while 1:
        line = f.readline()
        if line == '':
            break
        else:
            print(line)

def main(argv):
    # Current charlie card fare
    fare = 2.25

    # Get current data and time
    date_time = get_date_time()

    # Get the charlie cards balance from the text file
    balance,info = get_data()
    print("Last accessed -- {}".format(date_time))

    # Try to get the command line arguments
    try:
        opts, args = getopt.getopt(argv,"hra:de:s")

    except getopt.GetoptError:
        print_info()
        sys.exit(2)

        # If no arguments are passed, print help
    if len(argv) == 0:
        print_info()
        action = 'error: no arguments'

    # Take in the arguments
    for opt, arg in opts:
        if opt in ("-h"):
            print_info()
            sys.exit()
            action = 'h'

        # Leaving the opt in sytanx in case long arguments are added later
        elif opt in ("-r"):
            if balance < 2.25:
                print("Insufficient Balance!")
                action = 'error: insufficient balance'
            else:
                balance = balance - 2.25
                write_to_file(balance,date_time)
                print_balance(balance)
                action = 'r'

        elif opt in ("-a"):
            try:
                val = float(arg)
                balance = balance + float(arg)
                write_to_file(balance,date_time)
                print_balance(balance)
                action = 'a' + ' ' + arg
            except:
                print("Float not passed")#, file=sys.stderr)
                action = 'error: incorrect type'

        elif opt in ("-d"):
            print_balance(balance)
            action = 'd'

        elif opt in ("-e"):
            write_to_file(float(arg),info)
            action = 'e' + '' + arg

        elif opt in ("-s"):
            summarize_log()
            action = 's'

    create_log_entry(date_time, action)

if __name__ == "__main__":
   main(sys.argv[1:])
