import csv
import networkx as nx
import matplotlib.pyplot as plt

with open('graphs/temp.csv', mode ='r') as file: # modes for open method: r = read only, w = write (edit), a = append (add to end)
       # 'b': Binary mode. Used for reading or writing binary files (e.g., images). This can be combined with other modes, like 'rb' for reading binary.
       # 'x': Exclusive creation. Opens the file for writing but fails if the file already exists.
          csv_reader = csv.DictReader(file)
          print(next(csv_reader)) # prints the next row in the csv reader. the reader iterates thru like an io stream

#another way to store file name
file = open('graphs/temp.csv', mode='r')

# Remember to close the file when you're done
file.close()
