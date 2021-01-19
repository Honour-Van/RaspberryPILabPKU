import random


def srp():
    user = 0
    wtimes = 0
    ltimes = 0
    ttimes = 0
    while True:
        user = input("Please input: Scissors(0), Rock(1), Paper(2), Quit(3)\n")
        if len(user) > 1:
            print('too long')
            continue
        elif user.isdigit():
            user = int(user)
            if user > 3:
                print('num out of range')
                continue
        else:
            print('input not num')
            continue
        if user == 3:
            break
        computer = random.randint(0, 2)
        if (user == 0 and computer == 2) or (user == 1 and computer == 0) \
                or (user == 2 and computer == 1):
            print('YOU WIN!')
            wtimes = wtimes + 1
        elif computer == user:
            print("IT'S A TIE!")
            ttimes = ttimes + 1
        else:
            print('YOU LOSE!')
            ltimes = ltimes + 1
        print("________________________")
        print(wtimes, ltimes, ttimes)
        print("________________________")


def srp2():
    user = 0
    count = [0, 0, 0]
    wtimes = 0
    ltimes = 0
    ttimes = 0
    while True:
        user = input("Please input: Scissors(0), Rock(1), Paper(2), Quit(3)\n")
        if len(user) > 1:
            print('too long')
            continue
        elif user.isdigit():
            user = int(user)
            if user > 3:
                print('num out of range')
                continue
        else:
            print('input not num')
            continue
        if user == 3:
            break

        count[user] = count[user] + 1
        sum = count[0] + count[1] + count[2]
        computer = random.randint(0, sum)
        if computer <= count[0]:
            computer = 1
        elif computer <= count[0] + count[1]:
            computer = 2
        elif computer <= sum:
            computer = 0
        if (user == 0 and computer == 2) or (user == 1 and computer == 0) \
                or (user == 2 and computer == 1):
            print('YOU WIN!')
            wtimes = wtimes + 1
        elif computer == user:
            print("IT'S A TIE!")
            ttimes = ttimes + 1
        else:
            print('YOU LOSE!')
            ltimes = ltimes + 1
        print("________________________")
        print(count[0], count[1], count[2], sum)
        print(wtimes, ltimes, ttimes)
        print("________________________")


if __name__ == '__main__':
    srp2()
