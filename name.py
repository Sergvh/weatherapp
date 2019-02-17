import re

s = input("Enter your name please:")

name = re.search(r'\b[A-Z]\w+\b', s)

print('Hello ' + name.group(0))
