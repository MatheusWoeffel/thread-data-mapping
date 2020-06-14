library(dplyr)
library(readr)
library(tidyr)
library(ggplot2)
library(stringr)

will_use_thread = FALSE
will_use_data = TRUE
archive_extension = ""

data <- read_csv("ai_benchmark.csv")
data$mapping <- as.character(interaction(data$`td_mapping`, data$`data_mapping`))

df <- data %>% group_by(application, mode, mapping) %>%
  summarize(N=n(), avg=mean(time), se=3*sd(time)/sqrt(N)) %>%
  as.data.frame()
baseline <- df %>% filter(mapping == "none.none") 
df <- df %>% left_join(baseline,by=c("application", "mode")) 
df <- df %>% mutate(normalized_time = (avg.x / avg.y) * 100)
df <- df %>% mutate(gain= 100 * (avg.y - avg.x) / avg.y)

require(scales)
for(currentMode in unique(df$mode)){
  for(currentApp in unique(df$application)){
    d <- df %>% filter(mode == currentMode)
    d <- d %>% filter(application == currentApp)
    
    if(!will_use_data){
      d <- d %>% filter(grepl("*.none", mapping.x))
      archive_extension="_only_thread"
    }
    
    if (!will_use_thread){
      d <- d %>% filter(grepl("^none", mapping.x))
      archive_extension="_only_data"
    }
    
    newChart <- ggplot(data=d, aes(x= application, y= avg.x, fill = mapping.x)) +
    #scale_y_continuous(trans = log2_trans(), 
    # breaks = trans_breaks("log2", function(x) 2^x),
    #labels = trans_format("log2", math_format(2^.x))) +
    geom_bar(stat = "identity", position = 'dodge', width=.9, colour = "black", size = 1) +
    geom_errorbar(aes(ymin=avg.x-se.x, ymax=avg.x+se.x), position = position_dodge(.9), width = 0.5) +
    theme_bw(base_size = 25) +
    labs(x = "Application", y = "Time (s)") +
    theme(
      legend.position="top",
      legend.text=element_text(size=20),
    ) + ggtitle(paste(currentApp, currentMode, sep=" "))
  ggsave(plot=newChart, path="./td_charts", paste(currentApp,"_",currentMode, archive_extension,"_errbar.pdf", sep=""), width=20, height=22)
}
}



