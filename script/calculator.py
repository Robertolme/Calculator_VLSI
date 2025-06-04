import sympy as sp
import os
import sys

if not os.path.exists("/etc/os-release"):
    sys.exit(1)

#Requerimientos = {"C_l": 0.0000000001, "S_R": 20/0.00001 , "VDD": 5, "fmin": 7, "Vic_max": 4, "Vic_min": 2, "Avd" : 100}
#Parametros = {"Vtn": 0.6696, "lamda_d4" : 0.05, "lamda_d2" : 0.04, "Kp" : 49.9685e-6, "Kn" : 108.0460e-6, "V_tp" : 0.9214347} 
#variables = {}

Requerimientos = {"C_l": 10e-12, "S_R": 20/1e-6 , "VDD": 5, "fmin": 100e3, "Vic_max": 4, "Vic_min": 2, "Avd" : 100}
Parametros = {"Vtn": 0.6696, "lamda_d4" : 0.05, "lamda_d2" : 0.04, "Kp" : 49.9685e-6, "Kn" : 108.0460e-6, "V_tp" : 0.9214347} 
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
#variable, resultado = resolve("R_out = 2 / ", Requerimientos,Parametros)
variable, resultado = resolve("W_L_3_4 = I_5/( Kp *(V_sg3 - V_tp)^2 )", Requerimientos,Parametros,variables)
variable, resultado = resolve("W_L_1_2 = ((Avd * (lamda_d4 + lamda_d2) * sqrt(I_5/2) )^2) / (2 * Kn) ", Requerimientos,Parametros,variables)
variable, resultado = resolve("V_DS5_sat = Vic_min - (sqrt(I_5 / (Kn * W_L_1_2 )) ) - Vtn", Requerimientos,Parametros,variables)
variable, resultado = resolve("W_L_5 = (2 * I_5 / ( Kn * (V_DS5_sat)^2) )", Requerimientos,Parametros,variables)


print(variables)