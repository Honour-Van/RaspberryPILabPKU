from pyswip import Prolog, registerForeign # 导入模块

features = {}
def verify(t):
    if t in features:
        if features[t] == 'yes':
            return 1
        elif features[t] == 'no':
            return 0
    choice = input("Is it true? {}(y/n):".format(t))
    if choice == 'y':
        features[t] = 'yes'
        return 1
    elif choice == 'n':
        features[t] = 'no'
        return 0

verify.arity = 1
registerForeign(verify)
prolog = Prolog()
prolog.consult('animal.pl') # 导入 Prolog 的代码（规则库）
for result in prolog.query('hypothesize(X)'):
    print('It is', result["X"])