import json

class data():
    def __init__(self):
        self.date = ''
        self.val = 0

vals = []
def main():
    for i in range(0,5):
        d = data()
        vals.append(d)
    print(vals)

if __name__ == "__main__":
   main()
