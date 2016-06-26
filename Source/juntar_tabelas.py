import csv

def lerBase(nome_arquivo):
	bd = open(nome_arquivo, 'r').readlines()

	i = 0
	for linha in bd:
		bd[i] = linha.split(';')

		ncol = len(bd[i])-1

		bd[i][ncol] = bd[i][ncol].split("\n")
		bd[i][ncol] = bd[i][ncol][0]

		i += 1

	bd.pop(0)
	bd.pop(0)

	return bd

regras = []
for i in list(range(300,351)):
	regras = regras + lerBase("Resultados/Regras_01/Tabelas/Conf_Max/Tabela_Melhores_Regras_" + str(i) +  ".csv")

regras = map(list, set(map(tuple, regras)))
regras = list(regras)
regras.sort()

tabela = [["Antecedentes", " ", " ", " ", " ", " ", " ", " ", "Consequentes", " ", " ", " ", " ", " ", " ", " ", "Suporte", "Confianca"]]
tabela.append(["Estado", "Agravo", "Sexo", "RacaCor", "Agente", "Antibiotico", "Resistencia", "FaixaEtaria", "Estado", "Agravo", "Sexo", "RacaCor", "Agente", "Antibiotico", "Resistencia", "FaixaEtaria"])

tabela = tabela + regras
with open("Resultados/TOTAL_REGRAS_CONFMAX.csv", 'w') as csvfile:
	writer = csv.writer(csvfile, delimiter=';', lineterminator='\n')
	writer.writerows(tabela)
	csvfile.close()
