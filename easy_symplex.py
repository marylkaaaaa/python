from pulp import *

x1 = pulp.LpVariable("x1", lowBound=0)
x2 = pulp.LpVariable("x2", lowBound=0)

problem = pulp.LpProblem('Задача',pulp.LpMaximize)

problem += 4*x1 +6*x2 #Функция цели
problem += 90*x1+ 5*x2 <= 10000 #органичение 1
problem +=x2 ==3*x1 #органичение 1

problem.solve()  #Solve the given Lp problem.

print ("Результат:")
for variable in problem.variables():         # Returns a list of the problem variables
    print (variable.name, "=", variable.varValue)

print ("Значение функции:")
print (value(problem.objective))        #Returns the value of the variable/expression x, or x if it is a number
