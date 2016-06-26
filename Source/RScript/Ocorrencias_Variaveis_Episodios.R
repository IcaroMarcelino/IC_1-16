ocorrencias_variaveis <- function(bd){
  for(i in 1:ncol(bd)){
    c = as.data.frame(table(bd[,i]))[1]
    app = FALSE
    for(j in 1:nrow(c)){
      n = which(bd[,i] == c[j,])
      
      b = bd[n,]
      
      inter = as.data.frame(table(b[,5]))
      
      intervalos = paste(as.character(inter$Var1[1]), as.character(inter$Freq[1]), sep = ',') 
      
      for(k in 2:length(b)){
        intervalos = paste(intervalos, paste(as.character(inter$Var1[k]), as.character(inter$Freq[k]), sep = ',') , sep = "|")
      }

      write(paste(as.character(c[j,]), as.character(intervalos), sep = "|"), file = paste(getwd(), "/Inputs/Suporte/", as.character(colnames(bd)[i]), ".txt", sep = ""), append = app)
      
      app = TRUE
    }
  }
}