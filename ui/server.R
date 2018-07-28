#
#
# UI Backend for WHAT
#
#

library(shiny)
library(shinyjs)
library(scatterD3)
library(shinyBS)
library(shinycssloaders)


#deploy Paths
runPath<-"/home/ubuntu/hd2/src/WHAT/backend/logWindProfile.py"
defaultPath<-"/home/ubuntu/hd2/src/WHAT/backend/data/default.csv"

#dev Paths
if(Sys.getenv("USER")[1]=="tanner")
{
  runPath<-"/home/tanner/src/WHAT/backend/logWindProfile.py"
  defaultPath<-"/home/tanner/src/WHAT/backend/data/default.csv"
}


shinyServer(function(input,output,session){
  useShinyjs()
  
  #Sanity Checks, everything must be filled out or it will grey out the button
  observe({
    # shinyjs::disable("selModel")
    if(is.numeric(input$wind_speed)==FALSE || is.numeric(input$init_hgt)==FALSE || is.numeric(input$canopy)==FALSE || is.numeric(input$height)==FALSE || is.numeric(input$canopy_ratio)==FALSE)
    {
      shinyjs::disable("exec")
      shinyjs::show("crapInputs")
      output$crapInputs<-renderPrint("Invalid Inputs")
    }
    if(is.numeric(input$wind_speed)==TRUE && is.numeric(input$init_hgt)==TRUE && is.numeric(input$canopy)==TRUE  && is.numeric(input$height)==TRUE && is.numeric(input$canopy_ratio)==TRUE)
    {
      # output$crapInputs<-renderPrint("")
      shinyjs::hide("crapInputs")
      shinyjs::enable("exec")
    }
    # if(is.numeric(input$init_hgt)==TRUE && is.numeric(input$init_hgt)==TRUE)
    # {
    #   if(input$canopy>input$init_hgt)
    #   {
    #     print("test")
    #     updateRadioButtons(session,"selModel",selected="Massman")
    #   }
    #   if(input$canopy<=input$init_hgt)
    #   {
    #     updateRadioButtons(session,"selModel",selected="Massman")
    #   }
    # }
  })
  
  observeEvent(input$exec,
               {
                 print(input$simpleCanopy)
                 gArgs=paste("\"",input$wind_speed,"\" \"",input$spd_units,"\" \"",input$surface,"\" \"",input$init_hgt,"\" \"",input$height,"\" \"",input$canopy,"\" \"",input$hght_units,"\" \"",input$canopy_ratio,"\" \"",input$selModel,"\"",sep="")
                 print(gArgs)
                 runFile<-system2(command=runPath,args=gArgs,stdout=TRUE)
                 print(runFile)
                 outDat<-strsplit(runFile,";")
                 # output$adjustedSpeed<-renderPrint(paste("Calculated wind speed:",outDat[[1]][1]))
                 output$adjustedSpeed<-renderPrint(outDat[[1]][1])
                 
                 # point_x<-as.double(outDat[[1]][5])
                 # point_y<-as.double(outDat[[1]][7])
                 if(outDat[[1]][2]=="X")
                 {
                   plotData<-read.csv(defaultPath,check.names=FALSE)
                 }
                 else
                 {
                   plotData<-read.csv(file=trimws(outDat[[1]][2]),check.names=FALSE)
                 }
                 
                 if(outDat[[1]][3]=="X")
                 {
                   aPlotData<-read.csv(defaultPath,check.names=FALSE)
                 }
                 else
                 {
                   aPlotData<-read.csv(file=trimws(outDat[[1]][3]),check.names=FALSE)
                 }
                 # plotData<-read.csv(file=trimws("/home/tanner/src/WHAT/backend/data/plots/pDat.csv"),check.names=FALSE)
                #  output$logWindPlot<-renderPlot({
                #    plot(plotData,type="l",col="blue",lwd=2)
                #    grid()
                #    title("Wind Profile")
                #    points(point_x,point_y,col="red",type="p",lwd=5)
                # })
                 output$logWindPlot<-renderScatterD3({
                   scatterD3(
                     x = c(plotData[[1]],aPlotData[[1]]),
                     y = c(plotData[[2]],aPlotData[[2]]),
                     xlab=colnames(plotData)[1],
                     ylab=colnames(plotData)[2],
                     col_var=c(plotData[[3]],aPlotData[[3]]),
                     # colors=c("blue","red"),
                     col_lab="Info",
                     legend_width = 0,
                     lines = data.frame(slope = c(0, Inf,0,0), 
                                        intercept = c(0, 0,input$canopy,(input$canopy*(1-input$canopy_ratio))),
                                        stroke = c("#000","#000","brown","brown"),
                                        stroke_width = c(1,1,2,2),
                                        stroke_dasharray = c(5,5,0,0))
                   )
                 })
                 
                 
               })
  
})
