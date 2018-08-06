#
#
# UI for WHAT
#
#

library(shiny)
library(shinyjs)
library(shinythemes)
library(scatterD3)
library(shinyBS)
library(shinycssloaders)


#Deploy Paths
# vegPath<-"/home/ubuntu/hd2/src/WHAT/backend/data/surface_types.csv"
vegPath<-"/home/ubuntu/hd2/src/WHAT/backend/data/canopy_types.csv"


#Dev Paths
if(Sys.getenv("USER")[1]=="tanner")
{
  # vegPath<-"/home/tanner/src/WHAT/backend/data/surface_types.csv"
  vegPath<-"/home/tanner/src/WHAT/backend/data/canopy_types.csv"
}
vegData<-read.csv(file=vegPath)



shinyUI(fluidPage(theme=shinytheme("cosmo"),
  useShinyjs(),
  titlePanel("WHAT"),
  h3("Wind Height Adjustment Tool"),
  hr(),
  fluidRow(
    column(8,
           wellPanel(
             fluidRow(
           column(6,
           numericInput("wind_speed",label="Wind Speed",value=10,min=0,max=1000),
           bsTooltip("wind_speed","Input Known Wind Speed",placement="bottom",trigger="hover")
                  ),
           # column(4,
           #        selectizeInput("spd_units",label="Wind Speed Units",choices=list("miles per hour (mph)"="mph",
           #                                                                         "meters per second (mps)"="mps",
           #                                                                         "kilometers per hour (kph)"="kph",
           #                                                                         "chains per hour"="cph",
           #                                                                         "furlongs per fortnight"="fpf"))
           #        ),
           column(6,
                  numericInput("init_hgt",label="Wind Speed Height (Above Ground Level)",value=120,min=0,max=1000),
                  bsTooltip("init_hgt","Input Height Above Ground Level",placement = "bottom",trigger="hover")
                  )
           ),
           hr(),
           fluidRow(
           column(4,
           selectInput("surface","Surface/Vegetation",
                       c(Choose='',vegData[1]),selectize=TRUE,selected="Aspen")
           ),
           column(4,
                  numericInput("canopy",label="Vegetation Height",value=100,min=0,max=10000),
                  bsTooltip("canopy","Specify the above ground height of the vegetation", placement="bottom",trigger="hover")
                  ),
           column(4,
                  numericInput("canopy_ratio",label="Canopy Ratio",value=0.7,min=0,max=1,step=0.1),
                  bsTooltip("canopy_ratio","Specify the ratio of canopy to stem for the selected vegetation", placement="bottom",trigger="hover")
                  )
           ),
           hr(),
           fluidRow(
           column(6,
           numericInput("height",label="Enter Output Wind Height (Above Ground Level)",value=10,min=0,max=1000),
           bsTooltip("height","Height Above Ground Level",placement = "bottom",trigger="hover")
           )
           # column(4,
           #        selectizeInput("hght_units","Height Units",choices=list("feet (ft)"="ft",
           #                                                                "meters (m)"="m",
           #                                                                "chain",
           #                                                                "furlong"))
           #        )
           ),
           hr(),
           fluidRow(
             column(4,
                    # checkboxInput("simpleCanopy","Enable Simple Canopy Model",value=TRUE)
                    radioButtons("selModel","Select Model",choices=list("Massman","Albini","Both"),
                                 selected="Massman",inline=TRUE)),
                    column(4,
                           selectizeInput("spd_units",label="Wind Speed Units",choices=list("miles per hour (mph)"="mph",
                                                                                            "meters per second (mps)"="mps",
                                                                                            "kilometers per hour (kph)"="kph",
                                                                                            "chains per hour"="cph",
                                                                                            "furlongs per fortnight"="fpf"))
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
          actionButton("exec",label="Calculate Wind Speed!",class="btn-primary"),
          br(),
          hr(),
          verbatimTextOutput("crapInputs"),
          # withSpinner(
          # verbatimTextOutput("adjustedSpeed")
          htmlOutput("adjustedSpeed")
          # )
          # uiOutput("renderVtext")

         ),
      column(4,
             # plotOutput("logWindPlot")
             h4("Wind Profile"),
             # uiOutput("renderScat")
             withSpinner(
             scatterD3Output("logWindPlot"),type=4
             )
        
            )
    ) #end fluidrow
  ) #end fluidpage
) #End shinyui
