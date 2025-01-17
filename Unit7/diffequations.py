import sys
from sympy import symbols, lambdify, sympify, integrate, solve, solveset, simplify, I
from ast import literal_eval


x, y, c = symbols('x y c') 

class differential_equ:
    def __init__(self, equation):
        self.equation = equation
    def evaluate(self, x_sub, y_sub):
        return self.equation.subs([(x, x_sub), (y, y_sub)])


# functions
def slopefield(equ, x_range, y_range):
    first = differential_equ(sympify(equ))

    for i in range(*literal_eval(x_range)):
        for j in range(*literal_eval(y_range)):
            print(f"slope at ({i}, {j}) is {first.evaluate(i, j)}")

def euler_approx(equ, h, x, y, steps):
    if steps == 0:
        return y

    y_next = y + h * equ.evaluate(x, y)

    print(f"y({x:.2f}) = {y:.5f}")
    return euler_approx(equ, h, x + h, y_next, steps - 1)

def seperate_solve(f_x, g_y, point=None):
    F_x = integrate(f_x, x)
    G_y = integrate(g_y, y) + c  
    
    general_solution = solve(F_x - G_y, y)
    print("General solution(s):")
    for solution in general_solution:
        print(solution)
    
    if point:
        x_val, y_val = point
        for solution in general_solution:
            c_value = solve(solution.subs({x: x_val, y: y_val}), c)
            if c_value:
                particular_solution = solution.subs(c, c_value[0]).simplify()
                if particular_solution.has(I):  #imagine problem
                    real_part = particular_solution.as_real_imag()[0]
                    particular_solution = real_part.simplify()
                print(f"Particular solution for point {point}: {particular_solution}")
                return particular_solution
    else:
        return general_solution

# main part
if __name__ == '__main__':
    """
    Parameters:

    sys.argv[1] : operation run slopefield.py -h for help
    sys.argv[2] : diffrential equation (first order) 
    sys.argv[3] : x range for slopes processed inputed as tuple
    sys.argv[4] : y range for slopes processed inputed as tuple

    """

    if len(sys.argv) < 2:
        print("Please enter a command line argument\n Type -h for a refrence guide")
    elif sys.argv[1] == "-h":
        print("""
Welcome to Mark's helpful calculations for diff, equations
    Refrence Sheet

    -h  Provides a refrence sheet (This refrence sheet)
    -slope  Finds the slopes for a set of ranges and a diffrential equation
            Parmaters:

            equ: diffrential equation (first order) 
            x_range: x range for slopes processed inputed as tuple
            y_range: y range for slopes processed inputed as tuple  

            example: "x - (x * y)" "(-1, 3)" "(-1, 3)"    
    -euler Provides an approximate soultion to a diffrential equation by following the tangent line
            Parmaters: 

            equ: diffrential equation (first order)
            h: step size as a float
            final_x: x for y(x) that needs is to be found as a float
            intial value: x and y value inputed as a tuple

            example: "x + y" 0.1 1.5 "(1, 1)"
    -sep Provides a gereral or particular soultion if applicale to a first oder diffrerntial equation using seperation
            Parmaters:

            f_x : top funciton (in terms of x)
            g_y : bottom function (in terms of y)
            point: point used to find the particular soultion (if applicable) as a tuple

            example: "x**2" "y**2" "(0, 2)"
    """)
    elif sys.argv[1] == "-sep":
        try:
            point = literal_eval(sys.argv[4])      
        except:
            point = None
        seperate_solve(
            sympify(sys.argv[2]),
            sympify(sys.argv[3]),
            point
        )
    elif sys.argv[1] == "-slope":
        slopefield(sys.argv[2], sys.argv[3], sys.argv[4])
    elif sys.argv[1] == "-euler":
        inital_values = literal_eval(sys.argv[5])
        steps = round((float(sys.argv[4]) - inital_values[0]) / float(sys.argv[3]))
        final_value = euler_approx(
            differential_equ(sympify(sys.argv[2])),
            float(sys.argv[3]),
            inital_values[0],
            inital_values[1],
            steps
        )
        print(f"approximate value: {final_value}")
