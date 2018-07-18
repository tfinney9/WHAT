#
#
# UI Backend for WHAT
#
#

library(shiny)
library(shinyjs)
library(leaflet)

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
                 output$adjustedSpeed<-renderPrint(runFile)
               })
  
})
