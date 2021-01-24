#!/usr/bin/env python3

import os,sys,getopt,datetime,json
from math import floor

class CharlieCardManager():

    def __init__(self,fare):
        self.fare = fare
        self.date_time = datetime.datetime.now()
        
        self.balance = None
        self.last_trip = None

        self.load_data()

    # Print the possible arguments
    def print_info(self):
        print('This script manages your charlie card data. The following actions can be taken:')
        print('-h     : Print usage')
        print('-r     : Remove a fare')
        print('-a {#} : Add specified value')
        print('-p     : Diplay current balance')
        print('-s     : Diplay usage statistics')
        print('-t     : Diplay number of remaining trips')
        self.log("Displaying script usage")

    def load_data(self):
        '''
        Get the charlie card value from the text file
        '''
        fp = open('charlie_card.json','r')
        self.charlie_card_data = json.load(fp)
        self.balance = self.charlie_card_data['balance']
        self.last_trip = self.charlie_card_data['last_trip']
        fp.close()

    def save_data(self):
        '''
        Write current data state to a json file
        '''
        fp = open('charlie_card.json','w')
        self.charlie_card_data['balance'] = self.balance
        self.charlie_card_data['last_trip'] = str(self.last_trip)
        json.dump(self.charlie_card_data,fp)
        fp.close()

    def print_balance(self):
        '''
        Print balance of the charlie card
        '''
        if self.balance == None:
            self.load_data()
        print("Current balance: %.2f"%(self.balance))
        self.log("Checking balance")

    def remove_fare(self):
        '''
        Remove a trip fare from the current charlie card balance
        '''
        if self.balance < self.fare:
            print('Insufficient balance!')
        else:
            self.balance -= self.fare
            self.last_trip = str(self.date_time)
            print("Remaining balance: %.2f"%(self.balance))
        self.log(f"Took a trip")

    def add_to_balance(self,value):
        self.balance += value
        self.log(f"Added to balance: {value}")
        self.print_balance()

    def edit_balance(self,new_balance):
        self.balance = new_balance
        self.print_balance()

        self.log(f"Set balance to: {self.balance}")

    def trips_left(self):
        trips = floor(self.balance/self.fare)
        print(f"Trips remaining: {trips}")
        self.log('Checking trips left')

    def statistics(self):
        self.log("Analyzing charlie card usage")

    def log(self,action):
        fp = open('charlie_card.log','a')
        line = f"[{self.date_time}] {action}\n"
        fp.write(line)
        fp.close()

#################################################
##                  MAIN                       ##
#################################################
def main(argv):
    fare = 2.40
    ccm = CharlieCardManager(fare)

    # Try to get the command line arguments
    try:
        opts, args = getopt.getopt(argv,"hra:pe:st")

    except getopt.GetoptError:
        print_info()
        sys.exit(2)

    if len(argv) == 0:
        ccm.print_info()
        return
    
    # Take in the arguments
    for opt, arg in opts:
        if opt in ("-h"):
            ccm.print_info()
            sys.exit()

        # Leaving the opt in sytanx in case long arguments are added later
        elif opt in ("-r"):
            if ccm.balance < fare:
                print("Insufficient Balance!")
            else:
                ccm.remove_fare()

        elif opt in ("-a"):
            try:
                val = float(arg)
                ccm.add_to_balance(val)
            except:
                print('Value entered is not a valid dollar amount!')

        elif opt in ("-p"):
            ccm.print_balance()

        elif opt in ("-e"):
            try:
                new_balance = float(arg)
            except:
                print('Value entered is not a valid dollar amount!')
            ccm.edit_balance(new_balance)

        elif opt in ("-s"):
            ccm.statistics()

        elif opt in ("-t"):
            ccm.trips_left()

        ccm.save_data()

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    finally:
        pass
