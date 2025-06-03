import sympy as sp
import os
import sys

if not os.path.exists("/etc/os-release"):
    sys.exit(1)

Requerimientos = {"C_l": 0.0000000001, "S_R": 20/0.00001 , "VDD": 5, "fmin": 7, "Vic": 4}
Parametros = {"Vtn": 0.6696, "lamda_d4" : 0.005, "lamda_d2" : 0.004} 
variables = {}


def resolve(formula, *dicts):
    valores = {}
    for d in dicts:
        valores.update(d)

    lhs, rhs = formula.split('=')
    lhs = lhs.strip()
    rhs = rhs.strip()
    symbols_dict = {var: sp.Symbol(var) for var in valores.keys()}
    
    expr = sp.sympify(rhs, locals=symbols_dict)
    
    result = expr.evalf(subs=valores)
    
    variables[lhs] = result
    
    return lhs, result

# Ejecutar la función
variable, resultado = resolve("I_5 = C_l * S_R", Requerimientos)
variable, resultado = resolve("P_diss = C_l * S_R * VDD", Requerimientos)
variable, resultado = resolve("R_3db = 1 / (2 * pi * fmin)", Requerimientos)
variable, resultado = resolve("V_sg3 = VDD - Vic + Vtn", Requerimientos,Parametros)
variable, resultado = resolve("R_out = 2 / ", Requerimientos,Parametros)



print(variables)