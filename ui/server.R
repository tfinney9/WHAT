#
#
# UI Backend for WHAT
#
#

library(shiny)
library(shinyjs)
library(scatterD3)

#dev Paths
#runPath<-"/home/tanner/src/WHAT/backend/logWindProfile.py"

#deploy Paths
runPath<-"/home/ubuntu/hd2/src/WHAT/backend/logWindProfile.py"

shinyServer(function(input,output,session){
  
  observeEvent(input$exec,
               {
                 gArgs=paste("\"",input$wind_speed,"\" \"",input$spd_units,"\" \"",input$surface,"\" \"",input$height,"\" \"",input$canopy,"\" \"",input$hght_units,"\"",sep="")
                 print(gArgs)
                 runFile<-system2(command=runPath,args=gArgs,stdout=TRUE)
                 print(runFile)
                 outDat<-strsplit(runFile,":|: ")
                 output$adjustedSpeed<-renderPrint(outDat[[1]][1])
                 
                 point_x<-as.double(outDat[[1]][5])
                 point_y<-as.double(outDat[[1]][7])
                 
                 plotData<-read.csv(file=trimws(outDat[[1]][3]),check.names=FALSE)
                 # plotData<-read.csv(file=trimws("/home/tanner/src/WHAT/backend/data/plots/pDat.csv"),check.names=FALSE)
                #  output$logWindPlot<-renderPlot({
                #    plot(plotData,type="l",col="blue",lwd=2)
                #    grid()
                #    title("Wind Profile")
                #    points(point_x,point_y,col="red",type="p",lwd=5)
                # })
                 output$logWindPlot<-renderScatterD3({
                   scatterD3(
                     x = plotData[[1]],
                     y = plotData[[2]],
                     xlab=colnames(plotData)[1],
                     ylab=colnames(plotData)[2],
                     col_var=plotData[[3]],
                     col_lab="Info",
                     legend_width = 0
                   )
                 })
                 
                 
               })
  
})
