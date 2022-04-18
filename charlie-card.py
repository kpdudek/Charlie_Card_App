#!/usr/bin/env python3

import os,sys,getopt,datetime,json
from math import floor

class CharlieCardManager():

    def __init__(self):
        self.fare = 2.40
        self.balance = None
        self.date_time = None
        self.last_trip = None
        self.new_entry = None
        self.charlie_card_data = None
        self.load_data()

    def log(self,message):
        '''
            Write a message to the log file
        '''
        fp = open('charlie_card.log','a')
        date_time = datetime.datetime.now()
        line = f"[{date_time}] {message}\n"
        fp.write(line)
        print(message)
        fp.close()

    def print_info(self):
        '''
            Print all possible arguments and provide a short description.
        '''
        print('This script manages your charlie card data. The following actions can be taken:')
        print('-h     : Print usage')
        print('-r     : Remove a fare')
        print('-a {#} : Add specified value')
        print('-e {#} : Edit the current balance')
        print('-p     : Diplay current balance')
        print('-s     : Diplay usage statistics')
        print('-t     : Diplay number of remaining trips')

    def load_data(self):
        '''
            Load the Charlie Card data from the database.
        '''
        self.date_time = datetime.datetime.now()
        fp = open('charlie_card.json','r')
        self.charlie_card_data = json.load(fp)
        trip_dates = list(self.charlie_card_data.keys())
        self.balance = self.charlie_card_data[trip_dates[-1]]['balance']
        self.last_trip = datetime.datetime.strptime(trip_dates[-1], "%Y-%m-%d %H:%M:%S.%f")
        fp.close()

    def save_data(self):
        '''
            Write the current Charlie Card data to the database.
        '''
        if self.new_entry is not None:
            fp = open('charlie_card.json','w')
            self.charlie_card_data.update(self.new_entry)
            json.dump(self.charlie_card_data,fp)
            fp.close()

    def print_balance(self):
        '''
            Print the Charlie Card's balance.
        '''
        if self.balance == None:
            self.load_data()
        self.log("Current balance: %.2f"%(self.balance))
        self.log(f"Last Trip: {str(self.last_trip.date())}")

    def remove_fare(self):
        '''
            Remove a trip fare from the Charlie Card's balance.
        '''
        if self.balance < self.fare:
            self.log('Insufficient balance for trip!')
            self.print_balance()
        else:
            self.log(f"Trip fare removed.")
            print(f"Last Trip: {str(self.last_trip.date())}")
            print("Old balance: %.2f"%(self.balance))
            self.balance -= self.fare
            self.new_entry = {str(self.date_time): {"balance": self.balance}}
            print("New balance: %.2f"%(self.balance))
            self.trips_left()
    
    def add_to_balance(self,value):
        self.balance += value
        self.log(f"Added to balance: {value}")
        self.new_entry = {str(self.date_time): {"balance": self.balance}}
        self.print_balance()

    def edit_balance(self,new_balance):
        self.log(f"Set balance to: {new_balance}")
        self.balance = new_balance
        self.new_entry = {str(self.date_time): {"balance": self.balance}}
        self.print_balance()

    def trips_left(self):
        trips = floor(self.balance/self.fare)
        self.log(f"Trips remaining: {trips}")
    
    def statistics(self):
        self.log("Analyzing charlie card usage...")
        self.print_balance()

#################################################
##                  MAIN                       ##
#################################################
def main(argv):
    ccm = CharlieCardManager()

    # Try to get the command line arguments
    try:
        opts, args = getopt.getopt(argv,"hra:pe:st")
    except getopt.GetoptError:
        ccm.print_info()
        sys.exit(2)

    if len(argv) == 0:
        ccm.print_info()
        return
    
    # Take in the arguments. Accepted arguments are:
    # -h     : Print usage
    # -r     : Remove a fare
    # -a {#} : Add specified value
    # -e {#} : Edit the current balance
    # -p     : Diplay current balance
    # -s     : Diplay usage statistics
    # -t     : Diplay number of remaining trips
    for opt, arg in opts:
        if opt in ("-h"):
            ccm.print_info()
            sys.exit()

        elif opt in ("-r"):
            ccm.remove_fare()

        elif opt in ("-a"):
            try:
                val = float(arg)
                ccm.add_to_balance(val)
            except:
                print('Value entered is not a valid dollar amount!')

        elif opt in ("-e"):
            try:
                new_balance = float(arg)
            except:
                print('Value entered is not a valid dollar amount!')
            ccm.edit_balance(new_balance)
        
        elif opt in ("-p"):
            ccm.print_balance()

        elif opt in ("-s"):
            ccm.statistics()

        elif opt in ("-t"):
            ccm.trips_left()
            ccm.print_balance()

    ccm.save_data()

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    finally:
        pass
