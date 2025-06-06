#Desarrolar api
import sympy as sp
import sys
from fastapi import FastAPI
from pydantic import BaseModel

# Inicializar la app
app = FastAPI()

# Definir el esquema de los datos que se recibirán
class DatosEntrada(BaseModel):
    C_l: float
    S_R: float
    VDD: float
    fmin: float
    Vic_max: float
    Vic_min: float
    Avd:float

#Requerimientos = {"C_l": 0.0000000001, "S_R": 20/0.00001 , "VDD": 5, "fmin": 7, "Vic_max": 4, "Vic_min": 2, "Avd" : 100}
#Parametros = {"Vtn": 0.6696, "lamda_d4" : 0.05, "lamda_d2" : 0.04, "Kp" : 49.9685e-6, "Kn" : 108.0460e-6, "V_tp" : 0.9214347} 
#variables = {}

#Requerimientos = {"C_l": 10e-12, "S_R": 20/1e-6 , "VDD": 5, "fmin": 100e3, "Vic_max": 4, "Vic_min": 2, "Avd" : 100}
Parametros = {"Vtn": 0.6696, "lamda_d4" : 0.05, "lamda_d2" : 0.04, "Kp" : 49.9685e-6, "Kn" : 108.0460e-6, "V_tp" : 0.9214347} 
variables = {}

def resolve(formula, *dicts):
    valores = {}
    for d in dicts:
        valores.update(d)

    lhs, rhs = formula.split('=')
    lhs = lhs.strip()
    rhs = rhs.strip()
    
    # Crear símbolos
    symbols_dict = {var: sp.Symbol(var) for var in valores.keys()}
    expr = sp.sympify(rhs.replace("^", "**"), locals=symbols_dict)
    
    result = expr.evalf(subs=valores)
    return lhs, float(result)


@app.post("/calc")
def saludar(datos: DatosEntrada):
    Requerimientos = {
            "C_l": datos.C_l,
            "S_R": datos.S_R,
            "VDD": datos.VDD,
            "fmin": datos.fmin,
            "Vic_max": datos.Vic_max,
            "Vic_min": datos.Vic_min,
            "Avd": datos.Avd
        }

    variables = {}

    # Ejemplo de cálculos encadenados
    var, val = resolve("I_5 = C_l * S_R", Requerimientos)
    variables[var] = val

    var, val = resolve("P_diss = C_l * S_R * VDD", Requerimientos)
    variables[var] = val

    var, val = resolve("R_3db = 1 / (2 * pi * fmin * C_l)", Requerimientos)
    variables[var] = val

    var, val = resolve("V_sg3 = VDD - Vic_max + Vtn", Requerimientos | Parametros)
    variables[var] = val

    var, val = resolve("W_L_3_4 = I_5/( Kp *(V_sg3 - V_tp)^2 )", Requerimientos | Parametros | variables)
    variables[var] = val

    var, val = resolve("W_L_1_2 = ((Avd * (lamda_d4 + lamda_d2) * sqrt(I_5/2) )^2) / (2 * Kn) ", Requerimientos | Parametros |variables)
    variables[var] = val

    var, val = resolve("V_DS5_sat = Vic_min - (sqrt(I_5 / (Kn * W_L_1_2 )) ) - Vtn", Requerimientos | Parametros | variables)
    variables[var] = val

    var, val = resolve("W_L_5 = (2 * I_5 / ( Kn * (V_DS5_sat)^2) )", Requerimientos | Parametros | variables)
    variables[var] = val

    return variables


#variable, resultado = resolve("R_out = 2 / ", Requerimientos,Parametros)
