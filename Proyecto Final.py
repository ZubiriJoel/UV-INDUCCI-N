# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 14:48:46 2020

@author: Pon nombre aqui
"""

import numpy as np;
import pandas as pd;


#Lee el base de datos
datos = pd.read_csv('synergy_logistics_database.csv',delimiter=',')
print(datos.columns)


#1)---------------------------------------------------------------------------

#Acumulacion de total_value agrupado por direccion, origen, destino, medio
rutas = datos.groupby(
            ['direction',
             'origin',
             'destination',
             'transport_mode']).agg({'total_value':np.sum})

rutasE = datos[datos['direction'] == 'Exports'].groupby(
            ['direction',
             'origin',
             'destination',
             'transport_mode']).agg({'total_value':np.sum})

rutasI = datos[datos['direction'] == 'Imports'].groupby(
            ['direction',
             'origin',
             'destination',
             'transport_mode']).agg({'total_value':np.sum})


#Rutas mas demandadas en general
print(rutas.nlargest(10,'total_value'))

#Rutas de exportacion mas demandadas
print(rutasE.nlargest(10,'total_value'))

#Rutas de importacion mas demandadas
print(rutasI.nlargest(10,'total_value'))

'''
Diria que no conviene utilizar esta estrategia ya que no hay equilibrio si 
tomamos los 10 mas demanadas en general, ya que solo uno es de importe
'''

#2)---------------------------------------------------------------------------

#Acumulacion nada mas sobre el medio
medios = datos.groupby(['transport_mode']).agg({'total_value':np.sum})

#Los medios mas utilizados en general
print(medios.nlargest(10,'total_value'))

'''
Los 3 mas utilizados son Sea, Rail y Air; 
y el medio de transporte que se podria reducir sin impactar ganancias es Road
'''

#3)---------------------------------------------------------------------------

#Agregar el porcentaje que representa el valor
datos['porcentaje'] = datos['total_value']/datos['total_value'].sum()

#Sumar porcentajes y valor por pais
paises = datos.groupby(['origin']).agg({'total_value':np.sum,'porcentaje':np.sum})

#Los ordenamos de mayor a menor y hacemos una suma cumulativa
paises_acum = paises.nlargest(100,'porcentaje').cumsum()

print(paises_acum)

'''
Los paises que aportan el 80% son China, USA, Japan, France, South Korea, Germany, Russia, Canada, Italia
'''