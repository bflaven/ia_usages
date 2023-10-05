def calculate(operation, x, y):
    '''
    operation - takes the string [add, sub, mul, div]
    x & y - two numbers
    ''' 
    if operation == 'Addition':
        return x+y
    
    elif operation == 'Subtraction':
        if x>y:
            return x-y
        else:
            return y-x

    elif operation == 'Multiplication':
        return x*y
    
    elif operation == 'Division':
        return x/y


