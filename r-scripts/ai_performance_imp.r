library(readr)
library(stringr)
library(dplyr)
library(ggplot2)

data <- read_csv("ai_benchmark.csv") %>% as.data.frame()
data$mapping <- as.character(interaction(data$td_mapping, data$data_mapping))

baseline <- data %>% filter(mapping ==  'none.none')

data <- data %>% 
          filter(mapping != 'none.none') %>%
          group_by(application, mode, mapping) %>%
          left_join(baseline, by=c("application", "mode")) %>%
          mutate(speedup = time.y / time.x * 100 - 100)

data$time.y <- NULL
data$mapping.y <- NULL

df <- data %>% group_by(application, mode, td_mapping.x, data_mapping.x) %>%
  summarize(mean=mean(speedup), se=3*sd(speedup)/sqrt(n())) %>%
  as.data.frame()

rm(baseline)
rm(data)

# só treinamento e thread mapping
plot = df %>% filter(data_mapping.x == 'none') %>% filter(mode == 'training')

plot$td_mapping.x <- plot$td_mapping.x %>% str_replace_all(c("compact" = "Compact", "rr" = "Round Robin", "scatter" = "Scatter"))

g1 <- ggplot(data=plot, aes(x = application, y = mean, fill = td_mapping.x)) +
        geom_bar(position = "dodge", stat="identity", width=0.7) +
        geom_errorbar(aes(ymin=mean-se, ymax=mean+se), width=0.5, size=0.3, position = position_dodge(width=0.7), stat="identity") +
        theme_bw(base_size = 20) +
        labs(x = "Application", y = "Performance Improvement (%)") +
        scale_y_continuous(breaks=seq(-10, 50, 10)) + 
        expand_limits(y = seq(-10, 50, by = 10)) +
        theme(
          legend.position="top",
          legend.direction = "horizontal",
          legend.title = element_blank(),
          legend.key.width = unit(2, "cm"),
          axis.ticks = element_line(colour = "black"),
          panel.border = element_rect(colour = "black"),
          axis.title=element_text(size=50),
          legend.text=element_text(size=50),
          axis.title.x = element_blank(),
          axis.text.x = element_text(colour = "black", size=45, angle = 50, hjust = 1),
          axis.text.y=element_text(colour = "black", size=45),
          axis.title.y = element_text(margin = margin(t = 0, r = 25, b = 0, l = 0))
        )

ggsave("../figures/Speedup-thread-training.pdf", plot=g1, width=23, height=14, limitsize = FALSE)



# só treinamento e data mapping
plot = df %>% filter(td_mapping.x == 'none') %>% filter(data_mapping.x != 'memALL') %>% filter(mode == 'training')

plot$data_mapping.x <- plot$data_mapping.x %>% str_replace_all(c("intALL" = "Interleave", "numaBalancing" = "NUMA Balancing"))

g1 <- ggplot(data=plot, aes(x = application, y = mean, fill = data_mapping.x)) +
  scale_fill_brewer(palette="Dark2") +
  geom_bar(position = "dodge", stat="identity", width=0.7) +
  geom_errorbar(aes(ymin=mean-se, ymax=mean+se), width=0.5, size=0.3, position = position_dodge(width=0.7), stat="identity") +
  theme_bw(base_size = 20) +
  labs(x = "Application", y = "Performance Improvement (%)") +
  scale_y_continuous(breaks=seq(-12, 2, 2)) + 
  expand_limits(y = seq(-12, 2, by = 2)) +
  theme(
    #panel.grid = element_blank(),
    legend.position="top",
    legend.direction = "horizontal",
    legend.title = element_blank(),
    legend.key.width = unit(2, "cm"),
    axis.ticks = element_line(colour = "black"),
    panel.border = element_rect(colour = "black"),
    axis.title=element_text(size=50),
    legend.text=element_text(size=50),
    axis.title.x = element_blank(),
    axis.text.x = element_text(colour = "black", size=45, angle = 50, hjust = 1),
    axis.text.y=element_text(colour = "black", size=45),
    axis.title.y = element_text(margin = margin(t = 0, r = 25, b = 0, l = 0))
  )

ggsave("../figures/Speedup-data-training.pdf", plot=g1, width=23, height=14, limitsize = FALSE)


##########################
###### inferencia ########
##########################

# só treinamento e thread mapping
plot = df %>% filter(data_mapping.x == 'none') %>% filter(mode == 'inference')

plot$td_mapping.x <- plot$td_mapping.x %>% str_replace_all(c("compact" = "Compact", "rr" = "Round Robin", "scatter" = "Scatter"))

g1 <- ggplot(data=plot, aes(x = application, y = mean, fill = td_mapping.x)) +
  geom_bar(position = "dodge", stat="identity", width=0.7) +
  geom_errorbar(aes(ymin=mean-se, ymax=mean+se), width=0.5, size=0.3, position = position_dodge(width=0.7), stat="identity") +
  theme_bw(base_size = 20) +
  labs(x = "Application", y = "Performance Improvement (%)") +
  scale_y_continuous(breaks=seq(-30, 30, 10)) + 
  expand_limits(y = seq(-30, 30, by = 10)) +
  theme(
    legend.position="top",
    legend.direction = "horizontal",
    legend.title = element_blank(),
    legend.key.width = unit(2, "cm"),
    axis.ticks = element_line(colour = "black"),
    panel.border = element_rect(colour = "black"),
    axis.title=element_text(size=50),
    legend.text=element_text(size=50),
    axis.title.x = element_blank(),
    axis.text.x = element_text(colour = "black", size=45, angle = 50, hjust = 1),
    axis.text.y=element_text(colour = "black", size=45),
    axis.title.y = element_text(margin = margin(t = 0, r = 25, b = 0, l = 0))
  )

ggsave("../figures/Speedup-thread-inference.pdf", plot=g1, width=23, height=14, limitsize = FALSE)



# só treinamento e data mapping
plot = df %>% filter(td_mapping.x == 'none') %>% filter(data_mapping.x != 'memALL') %>% filter(mode == 'inference')

plot$data_mapping.x <- plot$data_mapping.x %>% str_replace_all(c("intALL" = "Interleave", "numaBalancing" = "NUMA Balancing"))

g1 <- ggplot(data=plot, aes(x = application, y = mean, fill = data_mapping.x)) +
  scale_fill_brewer(palette="Dark2") +
  geom_bar(position = "dodge", stat="identity", width=0.7) +
  geom_errorbar(aes(ymin=mean-se, ymax=mean+se), width=0.5, size=0.3, position = position_dodge(width=0.7), stat="identity") +
  theme_bw(base_size = 20) +
  labs(x = "Application", y = "Performance Improvement (%)") +
  scale_y_continuous(breaks=seq(-6, 4, 2)) + 
  expand_limits(y = seq(-6, 4, by = 2)) +
  theme(
    #panel.grid = element_blank(),
    legend.position="top",
    legend.direction = "horizontal",
    legend.title = element_blank(),
    legend.key.width = unit(2, "cm"),
    axis.ticks = element_line(colour = "black"),
    panel.border = element_rect(colour = "black"),
    axis.title=element_text(size=50),
    legend.text=element_text(size=50),
    axis.title.x = element_blank(),
    axis.text.x = element_text(colour = "black", size=45, angle = 50, hjust = 1),
    axis.text.y=element_text(colour = "black", size=45),
    axis.title.y = element_text(margin = margin(t = 0, r = 25, b = 0, l = 0))
  )

ggsave("../figures/Speedup-data-inference.pdf", plot=g1, width=23, height=14, limitsize = FALSE)