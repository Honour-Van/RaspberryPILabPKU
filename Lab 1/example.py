age = input('Enter your age:\n')
age = int(age)
if age >= 18:
    print('You are an adult')
elif age >= 6:
    print('You are a teenager')
else:
    print("You are a kid")