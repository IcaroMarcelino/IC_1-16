antibioticos <- function(bd, arq){
  micro = levels(bd[,9])
  antif = as.data.frame(table(bd[,11]))
  antif = antif[order(antif[,2], decreasing = TRUE),]
  
  anti = as.character(antif$Var1)
  
  m = 0
  a = 0
  inter = 0
  linha = NULL
  
  mat = matrix(nrow = 1, ncol = length(micro)+1)
  
  mat[1,1] = "Antibiotico/Agente"
  
  for(t in 1:length(micro)){
    mat[1,t+1] = as.character(micro[t])
  }
  
  write.table(mat, file = arq, append = FALSE, quote = FALSE, row.names = FALSE, col.names = FALSE, sep = ";")

  for(i in 1:length(anti)){
    a = which(bd[,11] == anti[i])
    mat = matrix(nrow = 1, ncol = length(micro)+1)
    mat[1,1] = as.character(anti[i])
    
   for(j in 1:length(micro)){
    m = which(bd[,9] == micro[j])
    inter = intersect(a,m)
    
    linha = c(linha, inter)
    
    if(length(inter) > 0){
      mat[1,j+1] = "X"
    }
    else{
      mat[1,j+1] = ""
    }
  }
   write.table(mat, file = arq, append = TRUE, quote = FALSE, row.names = FALSE, col.names = FALSE, sep = ";")
 }
}
