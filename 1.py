try:
    selected_index = int(input('Please select location: '))
except IndexError:
    print('The number you entered is too large!')
    exit(0)
except ValueError:
    print('You must enter an integer number!')
    raise SystemExit()

print('Hello')