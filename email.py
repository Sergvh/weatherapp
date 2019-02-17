import re

s = input("Enter your email please:")

mail = re.match(r'^([A-Za-z0-9_-]+\.)*[A-Za-z0-9_-]+@[a-z0-9_-]+(\.[a-z0-9_-]+)'
                r'*\.[a-z]{2,6}$', s)

if mail:
    print('You entered good email')
else:
    print('You entered wrong email')
