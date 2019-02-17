import re
import sys

file_name = sys.argv[1]
fp = open(file_name)
contents = fp.read()


match = re.search(r'<title>.+</title>', contents)
if match:
    match = re.sub('<title>|</title>', '', match.group(0))
    print('Title is: '+match)
else:
    print('There is no title')