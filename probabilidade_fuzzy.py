# -*- coding: utf-8 -*-
import numpy as np
import skfuzzy as fuzz

from skfuzzy import control as ctr 

venda= ctr.Antecedent(np.arange(0,1.01,0.01),"venda")

preco=ctr.Antecedent(np.arange(100000,1001000,1000),"preco")

qualidade=ctr.Consequent( np.arange(0,101,1), "qualidade")


#venda
venda["baixa"]=fuzz.trimf(venda.universe,[0,0.25,0.5])
venda["media"]=fuzz.trimf(venda.universe,[0.25,0.5,0.75])
venda["alta"]=fuzz.trimf(venda.universe,[0.5,0.75,1])
#preco
preco["baixo"]=fuzz.trimf(preco.universe,[100000, 200000,300000])
preco["medio"]=fuzz.trimf(preco.universe,[250000, 500000, 700000])
preco["alto"]=fuzz.trimf(preco.universe,[600000, 800000, 1000000])
#qualidade
qualidade['ruim'] = fuzz.trapmf(qualidade.universe, [0, 25, 45,60])
qualidade['mediana'] = fuzz.trapmf(qualidade.universe, [40, 50, 70,80])
qualidade['boa'] = fuzz.trapmf(qualidade.universe, [75, 80,95,100])



# regra 1 - se probabilidade venda é baixa, então qualidade é ruim
regra1 = ctr.Rule(venda['baixa'], qualidade['ruim'])
# regra 2 - se probabilidade venda é médio ou o preço é médio, então qualidade é mediana
regra2 = ctr.Rule(venda['media'] | preco['medio'], qualidade['mediana'])
# regra 3 - se probabilidade venda é alta e o preço é alto, então qualidade é boa
regra3 = ctr.Rule(venda['alta'] & preco['alto'], qualidade['boa'])
# regra 4 - se probabilidade venda é médio ou o preço é baixo, então qualidade é mediana
regra4 = ctr.Rule(venda['media'] | preco['baixo'], qualidade['mediana'])
# regra 5 - se probabilidade venda é baixa e o preço é alto, então qualidade é mediana
regra5 = ctr.Rule(venda['baixa'] & preco['alto'], qualidade['mediana'])
imovel_ctrl = ctr.ControlSystem([regra1, regra2, regra3, regra4, regra5])
engine = ctr.ControlSystemSimulation(imovel_ctrl)

# passa as predições dos modelos para suas respectivas variáveis de entrada
engine.input['venda'] =int(input("probabilidade de venda(%): "))/100
engine.input['preco'] = int(input("preço do imóvel: "))

engine.compute()

print(engine.output['qualidade'])
qualidade.view(sim=engine)
