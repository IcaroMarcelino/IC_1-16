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

	return bd

centroides = []
for i in range(1, 1001):
	centroides = centroides + lerBase("Resultados/Clustering_01/Centroides/Centroides_B" + str(i) + ".csv")

centroides.sort()

with open("Total_centroides.csv", 'a') as csvfile:
	writer = csv.writer(csvfile, delimiter=';', lineterminator='\n')
	writer.writerows(centroides)
	csvfile.close()