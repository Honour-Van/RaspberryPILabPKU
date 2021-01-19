def calc():
        
    print(
    '''
    1: +
    2: -
    3: *
    4: /
    0: Exit
    Enter choice:
    '''
        )

    choice = int(input())
    if choice == 0:
        return
    op1 = float(input('Enter first operand: '))
    op2 = float(input('Enter second operand: '))

    ans = 0
    ope = 0
    if choice == 1:
        ans = op1 + op2
        ope = '+'
    elif choice == 2:
        ans = op1 - op2
        ope = '-'
    elif choice == 3:
        ans = op1 * op2
        ope = '*'
    elif choice == 4:
        ans = op1 / op2
        ope = '/'
    print(op1, ope, op2, "=", ans)

def calc2():
    print(
    '''
    1: +
    2: -
    3: *
    4: /
    0: Exit
    '''
        )
    while True:
        choice = input('Enter choice:')
        if choice[0].isdigit():
            choice = int(choice)
            if 0 <= choice <= 4:
                break
            else:
                print('choice num wrong')
        else:
            print('choice type wrong')
    if choice == 0:
        return
    while True:
        op1 = input('Enter first operand: ')
        if op1.isdigit():
            op2 = input('Enter second operand: ')
        else:
            print('Operand num1 wrong')
            continue
        if op2.isdigit():
            op1 = float(op1)
            op2 = float(op2)
            break
        else:
            print('operand num2 wrong')

    ans = 0
    ope = 0
    if choice == 1:
        ans = op1 + op2
        ope = '+'
    elif choice == 2:
        ans = op1 - op2
        ope = '-'
    elif choice == 3:
        ans = op1 * op2
        ope = '*'
    elif choice == 4:
        ans = op1 / op2
        ope = '/'
    print(op1, ope, op2, "=", ans)

if __name__ == "__main__":   
    # calc()
    calc2()