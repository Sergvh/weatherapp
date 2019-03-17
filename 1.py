def get_number():
    try:
        return int(input('Enter number:'))
    except ValueError:
        print('Bad number!!')
    finally:
        return int(input('Enter number:'))

get_number()
