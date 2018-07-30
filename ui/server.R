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
                 print(outDat[[1]][1])
                 
                 # output$adjustedSpeed<-renderPrint(paste("Calculated wind speed:",outDat[[1]][1]))
                 # output$adjustedSpeed<-renderPrint(outDat[[1]][1])
                 
                 hdr<-"Calculated Wind Speed:"
                 eD<-strsplit(outDat[[1]][1],hdr) #split off the Header for organization
                 oD<-strsplit(eD[[1]][2],"Albini") #split off the albini model if it exists
                  
                 massmanStr<-paste(oD[[1]][1]) #set the massman str for organization
                 albiniStr<-paste("Albini",oD[[1]][2],sep="") #set the albini str
                 
                 output$adjustedSpeed<-renderUI({wellPanel(
                   HTML(paste(hdr,massmanStr,albiniStr,sep="<br/>")) #paste these strings with breaks, so it looks nice
                   )
                   })
                 
                 #this figures out which dataset to use depending on what is returned
                 which<-"BOTH"
                 if(outDat[[1]][2]=="X")
                 {
                   plotData<-read.csv(defaultPath,check.names=FALSE)
                   which<-"NM"
                 }
                 else
                 {
                   plotData<-read.csv(file=trimws(outDat[[1]][2]),check.names=FALSE)
                 }
                 
                 if(outDat[[1]][3]=="X")
                 {
                   aPlotData<-read.csv(defaultPath,check.names=FALSE)
                   which<-"NA"
                 }
                 else
                 {
                   aPlotData<-read.csv(file=trimws(outDat[[1]][3]),check.names=FALSE)
                 }
                 
                 #this figures out which color set to use, if one of the models is turned off
                 if(which=="BOTH")
                 {
                   colorDS<-unlist(list(aPlotData[[4]],plotData[[4]]))
                 }
                 if(which=="NA")
                 {
                   colorDS<-unlist(list(plotData[[4]]))
                 }
                 if(which=="NM")
                 {
                   colorDS<-unlist(list(aPlotData[[4]]))
                 }
                 # else
                 # {
                 #   colorDS<-unlist(list(aPlotData[[4]],plotData[[4]]))
                 # }
                 # plotData<-read.csv(file=trimws("/home/tanner/src/WHAT/backend/data/plots/pDat.csv"),check.names=FALSE)
                #  output$logWindPlot<-renderPlot({
                #    plot(plotData,type="l",col="blue",lwd=2)
                #    grid()
                #    title("Wind Profile")
                #    points(point_x,point_y,col="red",type="p",lwd=5)
                # })
                 output$logWindPlot<-renderScatterD3({
                   scatterD3(
                     x = c(aPlotData[[1]],plotData[[1]]),
                     y = c(aPlotData[[2]],plotData[[2]]),
                     xlab=colnames(plotData)[1],
                     ylab=colnames(plotData)[2],
                     #0==Input, 1==Output, 2==Massman Plot, 3 == Albini
                     col_var=colorDS,
                     colors=c("Massman"="#546E7A","Input"= "#FB8C00","Output"="#F44336","Albini"="#2196F3"),
                     # colors=c("2"="#546E7A","0"= "#FB8C00","1"="#F44336","3"="#2196F3"),
                     col_lab="Info",
                     legend_width = 0,
                     lines = data.frame(slope = c(0, Inf,0,0), 
                                        intercept = c(0, 0,input$canopy,(input$canopy*(1-input$canopy_ratio))),
                                        stroke = c("#000","#000","green","green"),
                                        stroke_width = c(1,1,2,2),
                                        stroke_dasharray = c(5,5,0,0))
                   )
                 })
                 
                 
               })
  
})
