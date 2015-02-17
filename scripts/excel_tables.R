
## operate with excel files 
# version 0.0.3

# in order to get easyGplot2, use this command lines
install.packages("devtools")
library(devtools)
install_github("easyGgplot2", "kassambara")

# libraries

options( java.parameters = "-Xmx4g" )

library(xlsx)
library(ggplot2)
library(easyGgplot2)

# global variables

file <- "patD"
sheet <- "Sheet1"

# read data from xlsx files
data <- read.xlsx(paste(file,".xlsx",sep=""), sheetName=sheet, header=TRUE)



######################
## package function ##
######################

pack_mode <- function(size) {
	temp_matrix <- matrix(nrow=(length(data[,1])))
	temp_matrix[,1] <-as.character(data[,1])
	for (i in 1:((round(length(data[2,])/size, digits=0))-1)) {
		for (k in ((2-size) + i*size):(1 + i*size)) {
			temp_matrix <- cbind(temp_matrix,data[,k])
		}
		temp_matrix[,1] <- as.character(data[,1])
		write.xlsx(temp_matrix, paste(file,"_",as.character(size),"t_packmode.xlsx", sep=""),  ## writes tables in the new sheet
			sheetName=paste("set",i, sep=" "),row.names=FALSE, append=TRUE)
		temp_matrix <- matrix(nrow=(length(data[,1])))
	}
}

#############################
## sliding window function ##
#############################


sw_mode <- function(size) {
	temp_matrix <- matrix(nrow=(length(data[,1])))
	temp_matrix[,1] <-as.character(data[,1])
	for (i in 2:(length(data[1,])-(size-1)))  {
		temp_matrix <- cbind(temp_matrix, data[,i:(i+(size-1))])
		write.xlsx(temp_matrix,paste(sheet,"_",as.character(size),"slmode.xlsx", sep=""), 
				sheetName=paste("set",i, sep=" "),row.names=FALSE, append=TRUE)
		temp_matrix <- matrix(nrow=(length(data[,1])))
		temp_matrix[,1] <- as.character(data[,1])
	}
}

######################
## Plotting results ##
######################

# read complexCruncher output

cmplx_data <- read.xlsx("cmplxcruncher.xlsx", sheetName="feces_genus_6slmode", header=TRUE)
x <- 1:length(cmplx_data$xW_B)

p1 <- ggplot(cmplx_data, aes(x=x, y=cmplx_data$xW_B)) + 
	geom_errorbar(aes(ymin=cmplx_data$xW_B-cmplx_data$xW_B_err, ymax=cmplx_data$xW_B+cmplx_data$xW_B_err), width=.1) + 
	geom_line() + geom_point() + 
	xlab("timeset") + ylab("wV") + ggtitle("wV variation") + # axis and plot labels   
	theme_bw() # sets background colour to white

p2 <- ggplot(cmplx_data, aes(x=x, y=cmplx_data$xW_beta)) + 
	geom_errorbar(aes(ymin=cmplx_data$xW_beta-cmplx_data$xW_beta_err, ymax=cmplx_data$xW_beta+cmplx_data$xW_beta_err), width=.1, colour="red") + 
	geom_line(colour="red") + geom_point() + 
	xlab("timeset") + ylab("w_beta") + ggtitle("w_beta variation") + # axis and plot labels   
	theme_bw() # sets background colour to white

# save plots in pdf file
pdf("feces_g_6t_swmode.pdf")
final_plot <- ggplot2.multiplot(p1,p2, cols=1)
dev.off()


#################################
##  TO DO:
##		- fix loop in packmode
##		- 


