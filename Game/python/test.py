import pyglet
import sympy
x2 = sympy.symbols("x2", integer=True)
print(sympy.solve(sympy.Eq((x2 - 3)**2 + (-2 * x2 - 2)**2, 4), x2))