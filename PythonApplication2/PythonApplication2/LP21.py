import pulp

Model = pulp.LpProblem('The Problem', pulp.LpMaximize)

Types = ['Tropic', 'Sea', 'Orleans', 'Grand']

x = pulp.LpVariable.dict('x_%s', Types, lowBound = 10, cat=pulp.LpInteger) # Minimum 10 Types of House

Profit = dict(zip(Types, [40000, 45000, 60000, 80000]))
Lot = dict(zip(Types, [0.20, 0.27, 0.25, 0.35]))
Stories = dict(zip(Types, [1, 1, 2, 2]))
Bedrooms = dict(zip(Types, [2, 3, 3, 4]))

Model += sum([Profit[i] * x[i] for i in Types]) # For Maximize
Model += sum([Lot[i] * x[i] for i in Types]) <= 20
Model += x['Sea'] + x['Orleans'] + x['Grand'] >= 50
Model += x['Tropic'] + x['Sea'] >= 40

Model .solve()

for Type in Types:
    print('Dla typu: %s powinno się wybudować: %s budynków'%(Type, x[Type].value()))
print('Profit: ' + str(sum([Profit[i] * x[i].value() for i in Types])))
print('Area: ' + str(sum([Lot[i] * x[i].value() for i in Types])))
