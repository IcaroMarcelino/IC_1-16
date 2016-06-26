escreveArqNames <- function(info, nome){
  write("", file = nome, append = FALSE)
  i = 1
  n = ncol(info)
  while(i<=n){
    write(paste(as.character(colnames(info[i])), ":"), file = nome, append = TRUE)
    write(as.character(sort(unique(info[[i]]))), file = nome, ncolumns = 1+length(levels(info[[i]])), append = TRUE, sep=",")
    write(".\n", file = nome, append = TRUE)
    i=i+1
  }
}
