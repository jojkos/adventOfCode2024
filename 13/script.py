import re
from sympy import symbols, Eq, solve

with open("input.txt", "r") as file:
        # read all lines, remove new line character
        input = [line.strip() for line in file.readlines()]

equations = []
aCost = 3
bCost = 1

i = 0

# regex that will parse numbers from this string Button A: X+94, Y+34
matchButtons = re.compile(r"Button [A-Z]: X([+-]\d+), Y([+-]\d+)")
# regex taht will parse numbers in this string Prize: X=8400, Y=5400
matchPrice = re.compile(r"Prize: X=(\d+), Y=(\d+)")

i = 0

for line in input:    
    if i % 3 == 0:
        a = None
        b = None
        price = None

    if not line:
          continue
    
    if i % 3 != 2:
        match = matchButtons.match(line)
        x = int(match.groups()[0])
        y = int(match.groups()[1])

        if not a:
            a = (x, y)
        else:
            b = (x, y)
    else:
         match = matchPrice.match(line)
         x = int(match.groups()[0])
         y = int(match.groups()[1])
         price = (x, y)

         equations.append({
                "a": a,
                "b": b,
                "price": price
         })
    i+= 1

# print(equations)
cost = 0

for equation in equations:
    # Define the variables
    x, y = symbols('x y')

    priceX  = equation["price"][0] + 10000000000000
    priceY = equation["price"][1] + 10000000000000

    # Define the equations
    eq1 = Eq(equation["a"][0] * x + equation["b"][0] * y, priceX)
    eq2 = Eq(equation["a"][1] * x + equation["b"][1] * y, priceY)

    # Solve the system of equations
    solution = solve((eq1, eq2), (x, y))
    
    # get x and y value from the solution
    x = solution[x]
    y = solution[y]
    isSolution = x.is_integer
    
    # print(x, y)

    if isSolution:
         cost += aCost * x + bCost * y

print(cost)


    