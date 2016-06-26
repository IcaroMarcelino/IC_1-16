#####################################################################################
# Icaro Marcelino Miranda - 06/2016
# 
# Mineracao de regras de associacao temporais usando Algoritmos Geneticos
# 
# Codificacao do cromossomo:
# Cada cromossomo possui 16 genes, 1 para cada variavel
# Cada gene possui a seguinte estrutura:
#  ______________________
# | w | AC | v | t0 | t1 |
# 
#   w (float) -> peso que sera comparado a um limiar, para decisao se a condicao 
#   episodica representada pelo gene fara parte da regra.
#
#   AC (bool) -> flag que indica se a condicao representada pelo gene fara parte do
#   antecedente (AC = 0) ou consequente (AC = 1) da regra.
#   
#   v -> representa a variavel ou o intervalo da variavel
#   
#   t0 e t1 -> limites inferior e superior do intervalo de tempo, e ajustado pelo GA
#   
#####################################################################################

import time
from deap import base
from deap import creator
from deap import tools
import random
import csv

def getIntervaloTempo(nome_arquivo, variavel):
	arq = open(nome_arquivo, 'r').readlines()

	i = 0
	for linha in arq:
		a = linha.split('|')

		a[2] = a[2].split('\n')
		a[2].remove("")

		if(a[0] == variavel):
			return [a[1], a[2][0]]

		i += 1

	return [0,0]    

def gerarCromossomoAleatorio(bd):
	random.shuffle(bd)
	observacao = random.choice(bd)
	bd.remove(observacao)
	cromossomo = []

	# arquivos = ["Estado.txt","Agravo.txt","Sexo.txt","Meses.txt","Agente.txt","Antibiotico.txt","Resistencia.txt","FaixaEtaria.txt"]
	arquivos = ["Estado.txt","Agravo.txt","Sexo.txt","RacaCor.txt","Meses.txt","Agente.txt","Antibiotico.txt","Resistencia.txt","FaixaEtaria.txt"]

	i = 0
	cont = 0
	cont1 = 0
	cont2 = 0
	cont3 = 0

	for variavel in observacao:
		if i != 4:
			w  = random.random()
			AC = random.choice([0,1])

			if AC == 1:
				cont += 1
				if w < 0.5:
					cont2 += 1
				else:
					cont3 += 1
			else:
				cont1 += 1
				if w < 0.5:
					cont2 += 1
				else:
					cont3 += 1

			if cont >= len(bd[0])-2:
				AC = 0

			if cont1 >= len(bd[0])-2:
				AC = 1

			if cont2 >= cont/2:
				w = random.uniform(.51,1)

			if cont3 >= cont1/2:
				w = random.uniform(.51,1)

			v  = variavel
			t  = getIntervaloTempo("Inputs/Intervalos/" + "Intervalo_" + arquivos[i], variavel)

			cromossomo.append([w, AC, v, t])
		i += 1

	return cromossomo

def probVariaveisEpisodios():
	arquivos = list(range(50,113))
	arquivos = arquivos + [48]

	sup = []

	for arquivo in arquivos:
		v = open("Inputs/Suporte/" + "supp_" + str(arquivo) + ".txt", 'r').readlines()
		v1 = [[]]

		i = 0
		for linha in v:
			v[i] = linha.split('|')

			temp = v[i][len(v[i])-1].split('\n')
			v[i].remove(v[i][len(v[i])-1])
			temp.remove('')

			v[i] = v[i] + temp

			
			for variavel in v[i]:
				v1[i].append(variavel.split(','))

			v1.append([])
			i += 1

		sup.append(v1)

	return sup

def getEpisodeset():
	arquivos = list(range(50,113))
	arquivos = [48] + arquivos

	episodeset = []

	for arquivo in arquivos:
		v = open("Inputs/Episodeset/" + str(arquivo) + ".txt", 'r').readlines()

		i = 0
		for linha in v:
			v[i] = linha.split('|')

			temp = v[i][len(v[i])-1].split('\n')
			v[i].remove(v[i][len(v[i])-1])
			temp.remove('')

			v[i] = v[i] + temp

			i += 1

		episodeset.append(v)
	return episodeset

def getOcorrenciasVariaveis():
	arquivos = ["Estado.txt","Agravo.txt","Sexo.txt","RacaCor.txt","Meses.txt","Agente.txt","Antibiotico.txt","Resistencia.txt","FaixaEtaria.txt"]
	# arquivos = ["Estado.txt","Agravo.txt","Sexo.txt","Meses.txt","Agente.txt","Antibiotico.txt","Resistencia.txt","FaixaEtaria.txt"]
	
	sup = []

	for arquivo in arquivos:
		v = open("Inputs/Ocorrencias/" + arquivo, 'r').readlines()

		i = 0
		for linha in v:
			v[i] = linha.split('|')

			temp = v[i][len(v[i])-1].split('\n')
			v[i].remove(v[i][len(v[i])-1])
			temp.remove('')

			v[i] = v[i] + temp

			v[i][1] = v[i][1].split(',')

			i += 1

		sup.append(v)

	return sup

def supp(x, ocorrencias, tam):
	soma = 0
	
	intervalos = {}

	if len(x) > 0:
		for elemento in x:
			for variavel in ocorrencias:
				for item in variavel:
					if (elemento[0] == item[0]) & (elemento[0] != []):
						temp = set(item[1])

						if len(intervalos) == 0:
							intervalos = set(item[1])
							break
						else:
							intervalos = intervalos.intersection(temp)
							break

	if len(intervalos) == 0:
		return -1

	return len(intervalos)/tam

def fenotipo(cromossomo):
	antecedente = []
	consequente = []

	if(len(cromossomo[0]) == 1):
		cromossomo = [cromossomo]

	for gene in cromossomo[0]:

		w = gene[0]
		AC = gene[1]
		v = gene[2]
		t = gene[3]

		if w > .5:
			if AC == 1:
				antecedente.append([v, t])
			else:
				consequente.append([v, t])

	return [antecedente, consequente]

def printFenotipo(fenotipo):
	ant = []
	con = []

	ant = "Se ("
	for antecedente in fenotipo[0]:
		ant = ant + " " + str(antecedente)
	ant = ant + ")"

	con = "Entao ("
	for consequente in fenotipo[1]:
		con = con + " " + str(consequente)
	con = con + ")"

	print(ant)
	print(con)
	print("\n")

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

	return bd

def fitness(cromossomo, ocorrencias, tam):
	regra = fenotipo(cromossomo)

	antecedente = regra[0]
	consequente = regra[1]

	if antecedente == []:
		return 0, 0

	if consequente == []:
		return 0, 0

	suppXuY = supp(antecedente + consequente, ocorrencias, tam)
	suppX = supp(antecedente, ocorrencias, tam)
	conf = suppXuY/suppX

	if suppXuY == -1:
		return 0, 0
	if suppX == -1:
		return 0, 0

	if conf >= 1:
		return 0, 0

	return suppXuY, conf

def ga_temporal(ngen, npop, pbcx, pbmt, exec):
	print("\n\n---- Incio GA Regras de Associacao (", str(exec), ") ----")
	start_time = time.time()
	saida = open("Regras/Regras_Fitness_" + str(exec) +  ".txt", 'w')

	bd = lerBase("Inputs/bd_mortais.csv")
	epset = getEpisodeset()
	ocorrencias = getOcorrenciasVariaveis()

	toolbox = base.Toolbox()

	creator.create("Fitness", base.Fitness, weights = (-1.0,1.0))
	creator.create("Individuo", list, fitness = creator.Fitness)

	toolbox.register("inicializarCromossomo", gerarCromossomoAleatorio, bd)
	toolbox.register("individuo", tools.initRepeat, creator.Individuo, toolbox.inicializarCromossomo, 1)
	toolbox.register("cruzamento", tools.cxUniform, indpb = .15)

	toolbox.register("populacao", tools.initRepeat, list, toolbox.individuo)

	toolbox.register("avaliar", fitness, ocorrencias = ocorrencias, tam = len(bd))
	toolbox.register("selecao", tools.selTournament, tournsize = 5)

	pop = toolbox.populacao(n = npop)

	# t = time.time()
	# print("Avaliando a populacao inicial... ")
	fitnesses = list(map(toolbox.avaliar, pop))
	for ind, fit in zip(pop, fitnesses):
		ind.fitness.values = fit
	
	# print("Tempo: ", int(time.time() - t))
	for g in range(ngen):
		# gen_time = time.time()
		print("\n-- Geracao %i --" % g)

		offspring = toolbox.selecao(pop, len(pop))
		offspring = list(map(toolbox.clone, offspring))

		for child1, child2 in zip(offspring[::2], offspring[1::2]):
			if random.random() < pbcx:
				toolbox.cruzamento(child1[0], child2[0])
				del child1.fitness.values
				del child2.fitness.values
				
		for mutante in offspring:
			for gene in mutante[0]:
				if random.random() < pbmt:
					gene[0] = random.random()

				if random.random() < pbmt:
					if gene[1] == 1:
						gene[1] = 0
					else:
						gene[1] = 1

		invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
		fitnesses = map(toolbox.avaliar, invalid_ind)
		for ind, fit in zip(invalid_ind, fitnesses):
			ind.fitness.values = fit

			fit1 = fitness(ind, ocorrencias, len(bd))
				
			while (fit1[0] == 0)|(fit1[1] == 0):
				ind[0] = gerarCromossomoAleatorio(bd)
				fit1 = fitness(ind, ocorrencias, len(bd))

		pop[:] = tools.selBest(offspring + tools.selBest(pop, 1), len(pop))
		# pop[:] = offspring

		fits = [ind.fitness.values[0] for ind in pop]
		fits2 = [ind.fitness.values[1] for ind in pop]
		
		length = len(pop)
		mean = sum(fits) / length
		mean2 = sum(fits2) / length
		# sum2 = sum(x*x for x in fits)
		# std = abs(sum2 / length - mean**2)**0.5

		r = tools.selBest(pop, 1)[0]
		m = fitness(r, ocorrencias, len(bd))
		
		# print("  Min: ", round(min(fits), 5)) 
		print("Melhor:  Suporte: ", round(m[0], 2), "   Confianca: ", round(m[1], 2))   
		print(str("Medio :  Suporte: " + str(round(mean, 2))) + "   Confianca: " + str(round(mean2, 2)))     # Valor medio.
		# print("  Std: ", round(std, 5))         # Desvio padrao da geracao.
		# print(" Melhor Individuo:\n", tools.selBest(pop, 1))
		# print(" Pior Individuo:\n", tools.selWorst(pop, 1))
		# print("  Melhor regra: ")
		# r = tools.selBest(pop, 1)[0]
		# m = fenotipo(r)
		# print("  Antecedente: ", m[0])
		# print("  Consequente: ", m[1])
		# print("  Suporte:   ", round(100*fitness(r, ocorrencias)[0], 2), "%")
		# print("  Confianca: ", round(100*fitness(r, ocorrencias)[1], 2), "%")
		# print("  Tempo gasto (geracao): ", int(time.time() - gen_time))
		# print("  Tempo gasto (total): ", int(time.time() - start_time))

		saida.write(str(g) + ";" + str(round(mean, 3)) + "\n")

	regras = open("Regras/Melhores_Regras_" + str(exec) +  ".txt", 'w')

	melhores = tools.selBest(pop, 10)

	for regra in melhores:
		regras.writelines(["%s, " % item  for item in fenotipo(regra)[0]])
		regras.write("\n=>\n")
		regras.writelines(["%s, " % item  for item in fenotipo(regra)[1]])
		regras.write("\nSuporte: " + str(fitness(regra, ocorrencias, len(bd))[0]))
		regras.write("\nConfianca: " + str(fitness(regra, ocorrencias, len(bd))[0]))
		regras.write("\n------------------------------------------------------------------\n\n")


	with open("Regras/Tabela_Melhores_Regras_" + str(exec) +  ".csv", 'w') as csvfile:
		tabela = [["Antecedentes", " ", " ", " ", " ", " ", " ", " ", "Consequentes", " ", " ", " ", " ", " ", " ", " ", "Suporte", "Confianca"]]
		tabela.append(["Estado", "Agravo", "Sexo", "RacaCor", "Agente", "Antibiotico", "Resistencia", "FaixaEtaria", "Estado", "Agravo", "Sexo", "RacaCor", "Agente", "Antibiotico", "Resistencia", "FaixaEtaria"])

		for regra in melhores:
			antecedentes = []
			consequentes = []

			for variavel in regra[0]:
				if(variavel[0] > .5):
					if variavel[1] == 1:
						antecedentes.append(variavel[2])
						consequentes.append(" ")

					else:
						consequentes.append(variavel[2])
						antecedentes.append(" ")
				else:
					antecedentes.append(" ")
					consequentes.append(" ")

			consequentes.append(round(100*fitness(regra, ocorrencias, len(bd))[0], 2))
			consequentes.append(round(100*fitness(regra, ocorrencias, len(bd))[1], 2))

			tabela.append(antecedentes + consequentes)

		writer = csv.writer(csvfile, delimiter=';', lineterminator='\n')
		writer.writerows(tabela)

	csvfile.close()
	regras.close()
	saida.close()

	print("--- %s segundos ---" % int(time.time() - start_time))


for i in list(range(1,51)):
	ga_temporal(50, 100, .8, .15, i)
