import re

s = input("Enter your phone number without gaps please:")

mail = re.match(r'^\(\d{3}\)\d{3}-\d{3}$', s)

if mail:
    print('You entered good phone number')
else:
    print('You entered wrong phone number')
