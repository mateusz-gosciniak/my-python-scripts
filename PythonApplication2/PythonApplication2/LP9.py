import pulp

''' Describe
LP9. (Based on [Ec79]) Kronkhauser, Golden, and Smith, a public accounting firm, has received a request to audit
the estate of a prominent individual who is being considered for appointment to a sensitive governmental
position
'''

Model = pulp.LpProblem('Find the auditing team', pulp.LpMaximize) # The managing partner would like to assemble an auditing team that has maximum total auditing experience.

# Constraints
MaxWeight = 1000 #  The auditing team will travel by a private business jet that has a passenger-load capacity of 1000 pounds.
MaxSeniors = 2 # At the same time, he does not want misunderstandings within the team, so he wants to have at most two senior staff members on the team (as team’s headperson and his deputy).

# Data From Table
Team = ['Linda Nelson', 'Susan Mayo', 'Karen Dubronsky', 'George Oswald', 'William Masterton', 'Andrew Goldman', 'Donald Crowder', 'Josh Zushinsky', 'Ronald Kramer']
Weight = dict(zip(Team, [105, 120, 140, 145, 170, 181, 210, 215, 230]))
Years = dict(zip(Team, [1.2, 5.8, 6.5, 3.2, 14, 0.5, 2, 10, 4.6]))
Senior = dict(zip(Team, [0, 0, 1, 0, 1, 0, 0, 1, 0])) # 0 means No, 1 means Yes

x = pulp.LpVariable.dict('x_%s', Team, 0, 1, pulp.LpInteger) # You can not take a clone of this person. Each person can only be taken to the team once.

Model += sum([Years[i] * x[i] for i in Team]) # The managing partner would like to assemble an auditing team that has maximum total auditing experience. 
Model += sum([Weight[i] * x[i] for i in Team]) <= MaxWeight
Model += sum([Senior[i] * x[i] for i in Team]) <= MaxSeniors

Model .solve()

for Person in Team:
    if x[Person].value() > 0:
        print('Mr/Ms %s is in the Team'%(Person))
    else:
        print('Mr/Ms %s isnt in the Team'%(Person))

print('Years of Expierence: ' + str(sum([Years[i] * x[i].value() for i in Team])))
print('Whole Weight: ' + str(sum([Weight[i] * x[i].value() for i in Team])))
print('Seniors in Team: ' + str(sum([Senior[i] * x[i].value() for i in Team])))

''' Output
Mr/Ms Linda Nelson is in the Team
Mr/Ms Susan Mayo is in the Team
Mr/Ms Karen Dubronsky isnt in the Team
Mr/Ms George Oswald is in the Team
Mr/Ms William Masterton is in the Team
Mr/Ms Andrew Goldman isnt in the Team
Mr/Ms Donald Crowder isnt in the Team
Mr/Ms Josh Zushinsky is in the Team
Mr/Ms Ronald Kramer is in the Team
Years of Expierence: 38.800000000000004 
Whole Weight: 985.0
Seniors in Team: 2.0
'''
