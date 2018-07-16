#
#
# UI for WHAT
#
#

library(shiny)
library(shinyjs)
library(shinythemes)


#Dev Paths
vegPath<-"/home/tanner/src/WHAT/backend/data/surface_types.csv"
vegData<-read.csv(file=vegPath)

shinyUI(fluidPage(theme=shinytheme("sandstone"),
  titlePanel("WHAT"),
  h3("Wind Height Adjustment Tool"),
  hr(),
  fluidRow(
    column(8,
           wellPanel(
             fluidRow(
           column(8,
           numericInput("wind_speed",label="Enter Wind Speed",value=10,min=0,max=1000)
                  ),
           column(4,
                  selectizeInput("spd_units",label="Wind Speed Units",choices=list("miles per hour (mph)"="mph",
                                                                                   "meters per second (mps)"="mps",
                                                                                   "kilometers per hour (kph)"="kph",
                                                                                   "chains per hour"="cph",
                                                                                   "furlongs per fortnight"="fpf"))
                  )),
           fluidRow(
           column(12,
           selectInput("surface","Select Surface/Vegetation",
                       c(Choose='',vegData[1]),selectize=TRUE,selected="evergreen needle-leaf trees")
           )),
           fluidRow(
           column(8,
           numericInput("height",label="Enter Output Wind Height",value=20,min=0,max=1000)
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
         )
    
  )
  
                  )
        )