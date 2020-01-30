library(dplyr)
library(readr)
library(tidyr)
library(ggplot2)
library(stringr)

data <- read_csv("td_results/novos_resultados.csv")
data <- data %>% filter(data$'data-map' != "memALL")
data$Mapeamento <- as.character(interaction(data$`td-map`, data$`data-map`, sep="-"))
# data$Mapeamento <- ifelse(data$Mapeamento == "Baseline-Baseline", "Baseline", data$Mapeamento)
# data$Mapeamento <- ifelse(data$Mapeamento == "Baseline-Interleave", "Interleave", data$Mapeamento)
# data$Mapeamento <- ifelse(data$Mapeamento == "Baseline-NUMA Balancing", "NUMA Balancing", data$Mapeamento)
# data$Mapeamento <- ifelse(data$Mapeamento == "Compact-Baseline", "Compact", data$Mapeamento)
# data$Mapeamento <- ifelse(data$Mapeamento == "Scatter-Baseline", "Scatter", data$Mapeamento)
# data$Mapeamento <- ifelse(data$Mapeamento == "Round Robin-Baseline", "Round Robin", data$Mapeamento)
df <- data %>% group_by(maquina, Mapeamento, application, tipo) %>%
      as.data.frame() 

df <- df %>% filter(tipo=="training")

df <- df %>% mutate(tempo_s = tempo/1000)

for(currentApp in unique(df$application)){
     d <- df %>% filter(application == currentApp)
     newChart <- ggplot(data=d, aes(x= Mapeamento, y= tempo_s)) +
     geom_boxplot() +
     stat_boxplot() +
     theme_bw(base_size = 70) +
     labs(x = "Mapeamentos (threads-dados)", y = "Tempo de Execução (s)" ) +
     theme(
      #   panel.grid.major.x = element_blank(),
      #   #      panel.grid = element_blank(),
      legend.position="top",
      axis.text.x = element_text(angle = 60, hjust = 1),
      #   legend.position="top",
      #   legend.direction = "horizontal",
      #   legend.title = element_blank(),
      #   legend.key.width = unit(2, "cm"),
      #   axis.ticks = element_line(colour = "black"),
      #   panel.border = element_rect(colour = "black"),
       axis.text=element_text(colour = "black", size=55),
      #   axis.title=element_text(size=45),
      #   axis.text.x = element_text(angle = 90),
      #legend.text=element_text(size=20),
      #   #      legend.box.margin = margin(b = -1.5, unit="cm"),
      #   plot.margin = unit(c(0,0,0,0),"cm")
      # geom_errorbar(width=0.5, size=0.3, position = position_dodge(width=0.9), stat="identity") +
    ) 
      
  
  ggsave(plot=newChart, path="/home/mwc/td_results/charts", paste(currentApp, ".all.pdf", sep=""), width=25, height=22)
}







# df <- data %>% group_by(mapping,appA,sizeA,appB,sizeB,event) %>%
# summarize(N=n(), avg=mean(value), se=3*sd(value)/sqrt(N)) %>%
# as.data.frame()
# # k$mapping <- factor(k$mapping, levels = c("os", "homo", "hetero"),
#                     labels = c("Linux Default", "Round-robin", "Instruction-Aware"))
# 
# k
# g1 <- ggplot(data=k, aes( x = appB, y = norm, fill = mapping)) + 
#   geom_bar(stat = "identity", position = 'dodge', width=.9, colour = "black", size = 1) +
#   theme_bw(base_size = 50) +
#   #   scale_fill_manual(values=c("#333333")) +
#   scale_y_continuous(breaks=seq(0, 100, 25)) + 
#   expand_limits(y = seq(0, 120, by = 10)) +
#   labs(x = "Co-runners", y = "Normalized Execution Time (%)") +
#   #   facet_wrap(.~app2, ncol=1, scales="free_y") +
#   theme(
#     panel.grid.major.x = element_blank(),
#     #      panel.grid = element_blank(),
#     #      legend.position="top",
#     legend.position="top",
#     legend.direction = "horizontal",
#     legend.title = element_blank(),
#     legend.key.width = unit(2, "cm"),
#     axis.ticks = element_line(colour = "black"),
#     panel.border = element_rect(colour = "black"),
#     axis.text=element_text(colour = "black", size=116),
#     axis.title=element_text(size=45),
#     axis.text.x = element_text(angle = 90),
#     axis.title.x = element_blank(),
#     axis.title.y = element_blank(),
#     legend.text=element_text(size=45),
#     #      legend.box.margin = margin(b = -1.5, unit="cm"),
#     plot.margin = unit(c(0,0,0,0),"cm")
#   )
