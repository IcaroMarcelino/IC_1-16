#################################################################
# Icaro Marcelino Miranda - 06/2016
# 
# 	Script para gerar um arquivo de atributos para cada variavel 
# da base indicando o numero de ocorrencia dos niveis para os
# casos da classe de saida
# 
#################################################################

frequencias <- function(bd){
  for(i in 1:ncol(bd)){
    x = as.data.frame(table(bd[,i]))
    
    i0 = which(bd[,8] == "I")
    r = which(bd[,8] == "R")
    s = which(bd[,8] == "S")
    
    x1 = which(bd[,i] == x[1,1])
    
    i1 = intersect(x1, i0)
    r1 = intersect(x1, r)
    s1 = intersect(x1, s)

    nome = paste(as.character(x[1,1]))
    
    if(nome == ""){ nome = "NA"}
    
     write(paste(nome, as.character(x[1,2]), as.character(length(i1)), as.character(length(r1)), as.character(length(s1)), sep = "|"), file = paste(getwd(), "/Inputs/Atributos/", as.character(colnames(bd)[i]), ".txt", sep = ""), append = FALSE)
    
    for(j in 2:nrow(x)){
     x1 = which(bd[,i] == x[j,1])
      
     i1 = intersect(x1, i0)
     r1 = intersect(x1, r)
     s1 = intersect(x1, s)

     nome = paste(as.character(x[j,1]))
                  
     if(nome == ""){ nome = "NA"}
     
     write(paste(nome, as.character(x[j,2]), as.character(length(i1)), as.character(length(r1)), as.character(length(s1)), sep = "|"), file = paste(getwd(), "/Inputs/Atributos/", as.character(colnames(bd)[i]), ".txt", sep = ""), append = TRUE)
    }
  }
}

