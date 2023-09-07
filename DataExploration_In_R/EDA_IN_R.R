# Exploratory Data Analysis

# Importing the required packages here
  library(tidyverse)
  library(GGally)
  library(data.table) 
  library(corrplot) # for correlation
  library(RColorBrewer) #for choosing colorblind colors

# Reading the csv file
  sleep_df <- read.csv("SleepStudy.csv", as.is = FALSE)

# Getting the column names
  names(sleep_df)
# Detailed about each column
  str(sleep_df)
  summary(sleep_df)

# Obtaining the colors from the colorblind friendly palette
  display.brewer.all(type="div", n=6, colorblindFriendly=TRUE)

# Choosing two colors
  figcolors_base1 <- brewer.pal(n=3, name="RdBu")
  figcolors2 <- c(figcolors_base1[1], figcolors_base1[3])
  figcolors2

# Choosing 4 colors
  figcolors_base2 <- brewer.pal(n=4, name="RdBu")
  figcolors4 <- c(figcolors_base2[1:4])
  figcolors4

# Choosing 6 colors
  figcolors_base3 <- brewer.pal(n=6, name="RdYlBu")
  figcolors6 <- c(figcolors_base3[6:1])
  figcolors6


# VISUALIZATIONS
# 1. Gender
    sleep_df$Gender[sleep_df$Gender == 1] <- "Male"
    sleep_df$Gender[sleep_df$Gender == 0] <- "Female"
    
    #   The gender column has two values - 
    #     1 - Male - 102 records
    #     0 - Female - 151 records
    
    table(sleep_df$Gender)
    
    #+ fig.width=7, fig.height=6 dpi=600
    ggplot(data = sleep_df) +
      geom_bar(aes(x=Gender, fill=Gender))+
      labs(y="No of people", title="Gender Type") +
      theme(legend.position="top", plot.title=element_text(hjust=0.5)) +
      scale_fill_manual(values = figcolors2)


# 2. ClassYear
  #  Class Year and Gender
  #   The ClassYear column has four values - 
  #     1 - First Year  - 47 records
  #     2 -             - 95 records
  #     3 -             - 54 records
  #     4 - Senior      - 57 records

    table(sleep_df$ClassYear)
    
    #    There are more students from the second year
    ggplot(data = sleep_df) +
      geom_bar(aes(x=ClassYear, fill=Gender)) +
      labs(y="No of people", title="Class Year based Gender") +
      scale_y_continuous(breaks = seq(0, 100, 10)) +
      theme(legend.position="top", plot.title=element_text(hjust=0.5)) +
      scale_fill_manual(values = figcolors2)


# 3. LarkOwl
    table(sleep_df$LarkOwl)
    
    #   Lark Neither     Owl 
    #   41     163       49 
    
    #Most of the students are neither Larks nor Owls 
    ggplot(data = sleep_df) +
      geom_bar(aes(x=LarkOwl, fill=Gender)) +
      labs(y="No of people", title="LarkOwl based on Gender Type") +
      theme(legend.position="top", plot.title=element_text(hjust=0.5)) +
      scale_fill_manual(values = figcolors2)


# 4. PoorSleepQuality - Measure of sleep quality (higher values are poorer sleep)
    table(sleep_df$PoorSleepQuality)
    summary(sleep_df$PoorSleepQuality)
    
    ggplot(data=sleep_df, aes(PoorSleepQuality)) +
      geom_bar(fill= figcolors_base3[6])    +
      scale_x_continuous(breaks = seq(0, 20, 1)) +
      labs(y="No of People", title="Poor Sleep Quality") +
      theme(plot.title=element_text(hjust=0.5) )


# 5. DepressionScore
    table(sleep_df$DepressionScore)
    summary(sleep_df$DepressionScore)
    
    depscore_breaks <- c(0,1,6,11,36)
    depscore_labels <- c("0","1-5","6-10","11-35")
    
    setDT(sleep_df)[ , depscore_groups := cut(DepressionScore, 
                                              breaks = depscore_breaks, 
                                              right = FALSE, 
                                              labels = depscore_labels)]
    # to see the distrbution of each group 
    table(sleep_df$depscore_groups)
    
    #Bar Chart of the depression score groups
    ggplot(data = sleep_df) +
      geom_bar(aes(x=depscore_groups, fill=depscore_groups)) +
      labs(y="No of people", title="Depression Score Groups") +
      scale_y_continuous(breaks = seq(0, 150, 10)) +
      theme(legend.position="top", plot.title=element_text(hjust=0.5)) +
      scale_fill_manual(values = figcolors4)


# 6. Drinks
    table(sleep_df$Drinks)
    
    drinks_score_breaks <- c(0,1,6,11,16,21,25)
    drinks_score_labels <- c("No Drinks","1-5","6-10","11-15","16-20", "21-25")
    
    setDT(sleep_df)[ , Drinks_Score_Groups := cut(Drinks, 
                                                  breaks = drinks_score_breaks, 
                                                  right = FALSE, 
                                                  labels = drinks_score_labels)]
    #Distribution of each group
    table(sleep_df$Drinks_Score_Groups)
    
    # Horizontal bar graph
    ggplot(data=sleep_df, aes(y=Drinks_Score_Groups,fill=Drinks_Score_Groups)) +
      geom_bar() +
      theme(legend.position="top", plot.title=element_text(hjust=0.5)) +
      labs(x="No of people",y="Number of alcoholic drinks per week ", 
           title="Alcoholic drinks per week") +
      scale_fill_manual(values = figcolors6)



# 7. GPA Vs Drinks_Score_Groups
    ggplot(data=sleep_df[sleep_df$Drinks_Score_Groups != "21-25"]) +
      geom_violin(aes(x=GPA, y=Drinks_Score_Groups, fill=Drinks_Score_Groups)) +
      theme(legend.position="top", plot.title=element_text(hjust=0.5)) +
      labs(x="GPA", y="Drinks_Score_Groups", title="GPA Vs Drinks_Score_Groups") +
      scale_fill_manual(values = figcolors6)

# 8. GPA Vs CognitionScore
    ggplot(data=sleep_df) +
      geom_point(aes(x=GPA, y=CognitionZscore)) +
      labs(x="GPA", y="Cognition ZScore", title="GPA Vs CognitionZscore") +
      theme(plot.title = element_text(hjust = 0.5)) 
    
    

  



  
  