import json

class data():
    def __init__(self):
        self.date = ''
        self.val = 0

vals = []
def main():
    for i in range(0,5):
        d = data()
        d.date = i
        d.val = i**2
        vals.append(d)
    
    for j in range(0,5):
        print((vals[j].date,vals[j].val))

if __name__ == "__main__":
   main()
