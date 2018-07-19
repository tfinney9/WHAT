#
#
# UI for WHAT
#
#

library(shiny)
library(shinyjs)
library(shinythemes)
library(scatterD3)



#Deploy Paths
vegPath<-"/home/ubuntu/hd2/src/WHAT/backend/data/surface_types.csv"

#Dev Paths
if(Sys.getenv("USER")[1]=="tanner")
{
  vegPath<-"/home/tanner/src/WHAT/backend/data/surface_types.csv"
}
vegData<-read.csv(file=vegPath)



shinyUI(fluidPage(theme=shinytheme("cosmo"),
  titlePanel("WHAT"),
  h3("Wind Height Adjustment Tool"),
  hr(),
  fluidRow(
    column(8,
           wellPanel(
             fluidRow(
           column(4,
           numericInput("wind_speed",label="Enter Wind Speed",value=10,min=0,max=1000)
                  ),
           column(4,
                  selectizeInput("spd_units",label="Wind Speed Units",choices=list("miles per hour (mph)"="mph",
                                                                                   "meters per second (mps)"="mps",
                                                                                   "kilometers per hour (kph)"="kph",
                                                                                   "chains per hour"="cph",
                                                                                   "furlongs per fortnight"="fpf"))
                  ),
           column(4,
                  numericInput("init_hgt",label="Wind Speed Height",value=5,min=0,max=1000)
                  )
           ),
           hr(),
           fluidRow(
           column(8,
           selectInput("surface","Select Surface/Vegetation",
                       c(Choose='',vegData[1]),selectize=TRUE,selected="evergreen needle-leaf trees")
           ),
           column(4,
                  numericInput("canopy",label="Enter Canopy Height",value=0,min=0,max=10000)
                  )
           ),
           hr(),
           fluidRow(
           column(8,
           numericInput("height",label="Enter Output Wind Height",value=100,min=0,max=1000)
           ),
           column(4,
                  selectizeInput("hght_units","Height Units",choices=list("feet (ft)"="ft",
                                                                          "meters (m)"="m",
                                                                          "chain",
                                                                          "furlong"))
                  )
           ),
           br()
          ),
          actionButton("exec",label="Calculate Wind Height!",class="btn-primary"),
          br(),
          hr(),
          verbatimTextOutput("adjustedSpeed")

         ),
      column(4,
             # plotOutput("logWindPlot")
             h4("Wind Profile"),
             scatterD3Output("logWindPlot")
        
      )
    
  )
  
                  )
        )
