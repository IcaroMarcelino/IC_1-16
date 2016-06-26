#################################################################
# Icaro Marcelino Miranda - 06/2016
# 
# 	Script para gerar um arquivo para cada variavel da base
# indicando o primeiro e o ultimo instante que os niveis ocorrem
# 
#################################################################

intervalosObservacoes <- function(bd){
  for(i in 1:ncol(bd)){
    c = as.data.frame(table(bd[,i]))[1]
    app = FALSE
    for(j in 1:nrow(c)){
      n = which(bd[,i] == c[j,])
      
      b = bd[n,]
      
      max = b[which.max(b[,5]),5]
      min = b[which.min(b[,5]),5]
      
      write(paste(as.character(c[j,]), as.character(min), as.character(max), sep = "|"), file = paste(getwd(), "/Inputs/Intervalos/Intervalo_", as.character(colnames(bd)[i]), ".txt", sep = ""), append = app)
      
      app = TRUE
    }
  }
}