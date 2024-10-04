import csv

with open('graphs/temp.csv', mode ='r') as file: # modes for open method: r = read only, w = write (edit), a = append (add to end)
       # 'b': Binary mode. Used for reading or writing binary files (e.g., images). This can be combined with other modes, like 'rb' for reading binary.
       # 'x': Exclusive creation. Opens the file for writing but fails if the file already exists.
       csvFile = csv.DictReader(file)
       for lines in csvFile:
            print(lines)