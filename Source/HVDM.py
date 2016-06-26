#####################################################################################
# Icaro Marcelino Miranda - 06/2016
# 
# Metrica de distancia HVDM - Distancia entre valores simbolicos.
# 
# 	Para a utilizacao desse algoritmo e necessario um arquivo para cada variavel
# da base, contendo o numero de ocorrencias para cada nivel para todos os casos
# da variavel de saida.
# 
# Exemplo de uso:
# 	
# 	# Le as ocorrencias para a classe de saida. (Veja pasta de Inputs)
# 	atributos = lerAtributos()
# 	
# 	indice_ponto1 = 0
# 	indice_ponto2 = 100
# 	
# 	distancia = HVDM(atributos, base_de_dados, indice_ponto1, indice_ponto2)
#
#####################################################################################

class Atributos:
	def __init__(self, nome_arquivo):
		self.info, self.niveis = self.lerInfo(nome_arquivo)
		self.dp = 0

	def lerInfo(self, nome_arquivo):
		arq = open(nome_arquivo, 'r').readlines()

		i = 0
		niveis = []
		for linha in arq:
			arq[i] = linha.split("|")

			ncol = len(arq[i])-1

			arq[i][ncol] = arq[i][ncol].split("\n")
			arq[i][ncol] = arq[i][ncol][0]

			niveis.append(arq[i][0])

			i += 1
		
		return arq, niveis

	def getInfo(self):
		return self.info

	def setDP(self, dp):
		self.dp = dp

	def freqRelativaSaida(self, x, c):
		if x in self.niveis:
			indice = self.niveis.index(x)
			elem = self.info[indice]
			
			return int(elem[c])/int(elem[1])
		
		return 0

	def VDM(self, x, y):
		vdm = 0

		for c in list(range(2, 5)):
			vdm += ((self.freqRelativaSaida(x,c))-(self.freqRelativaSaida(y,c)))**2

		return vdm

	def distanciaHVDM(self, x, y):
		if x == y:
			self.distancia = 0
			return 0

		if (x == "NA") | (y == "NA"):
			self.distancia = 1
			return 1

		# if (type(x) == type(.5)) | (type(x) == type(1)) & \
		# 	(type(y) == type(.5)) | (type(y) == type(1)):

		# 	self.distancia = (abs(x-y)/(4*self.dp))
		# 	return (abs(x-y)/(4*self.dp))

		else:
			self.distancia = self.VDM(x,y)
			return self.VDM(x,y)

	def setXY(self, x, y):
		self.x = x
		self.y = y

	def calcularDistancia(self):
		self.distancia = self.distanciaHVDM(self.x, self.y)
		return self.distancia

	def getDistancia(self):
		return self.distancia

	def desvioPadrao(valores):
		soma = 0

		for valor in valores:
			soma += valor
		
		media = soma/len(valores)

		soma = 0
		for valor in valores:
			soma += (valor - media)**2
	   
		dp = (soma/len(valores))**0.5

		return dp

def HVDM(atributos, base, x, y):
	d = 0
	i = 0

	for atributo in atributos:
		atributo.setXY(base[x][i], base[y][i])

		d += float(atributo.calcularDistancia())**2
		i += 1

	d **= 0.5
	return d

def lerAtributos():
	arquivos = ["Estado.txt","Agravo.txt","Sexo.txt","RacaCor.txt","Meses.txt","Agente.txt","Antibiotico.txt","Resistencia.txt","FaixaEtaria.txt"]


	atributos = []
	
	for arq in arquivos:
		atributos.append(Atributos("Inputs/Atributos/" + arq))

	return atributos

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