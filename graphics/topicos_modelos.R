library(readr)
library(tidyverse)
library(Hmisc)
library(plotly)
library("wesanderson")
library(ggrepel)

topicos_modelos <- read_csv("data/topicos_modelos.csv")

########################## Accuracy

############# Top 1
top_1 = topicos_modelos %>% 
  filter(top_autor == 1) %>% 
  select(num_topics, accuracy, topic_coherence) %>% 
  top_n(5, accuracy) %>% 
  arrange(desc(accuracy)) %>% 
  mutate_all(~round(., 4)) %>% 
  rename(`Número de topicos` =num_topics, Accuracy = accuracy,  `Topic Coherence` = topic_coherence)
  
top_1 %>% 
  latex(file="", rowname=NULL) 

############# Top 5
top_5 = topicos_modelos %>% 
  filter(top_autor == 5) %>% 
  select(num_topics, accuracy, topic_coherence) %>% 
  top_n(5, accuracy) %>% 
  arrange(desc(accuracy)) %>% 
  mutate_all(~round(., 4)) %>% 
  rename(`Número de topicos` =num_topics, Accuracy = accuracy,  `Topic Coherence` = topic_coherence)

top_5 %>% 
  latex(file="", rowname=NULL) 

############# Top 5
top_10 = topicos_modelos %>% 
  filter(top_autor == 10) %>% 
  select(num_topics, accuracy, topic_coherence) %>% 
  top_n(5, accuracy) %>% 
  arrange(desc(accuracy)) %>% 
  mutate_all(~round(., 4)) %>% 
  rename(`Número de topicos` =num_topics, Accuracy = accuracy,  `Topic Coherence` = topic_coherence)

top_10 %>% 
  latex(file="", rowname=NULL) 


gg = topicos_modelos %>% 
  mutate(num_topics = as.character(num_topics), top_autor= as.integer(top_autor)) %>% 
  rename(`Número de tópicos` =num_topics, Accuracy = accuracy,  `Top k autores` = top_autor) %>% 
  ggplot(aes(x=`Top k autores`, y = Accuracy, color=`Número de tópicos`, group=`Número de tópicos`)) +
  geom_line() +
  scale_fill_manual(values = wes_palette("Darjeeling1")) +
  labs(
    title = "Modelos LDA-Autor",
    subtitle = "Precision at k (P@k)"
  )
gg

ggplotly(gg)

topicos_top = topicos_modelos %>% 
  filter(top_autor == 10 & accuracy>0.3) %>% 
  arrange(desc(accuracy)) %>% 
  pull(num_topics)

gg_zoom = topicos_modelos %>% 
  filter(num_topics %in% topicos_top) %>% 
  mutate(num_topics = factor(num_topics, levels= topicos_top), top_autor= as.integer(top_autor)) %>% 
  rename(`Número de tópicos` =num_topics, Accuracy = accuracy,  `Top k autores` = top_autor) %>% 
  ggplot(aes(x=`Top k autores`, y = Accuracy, color=`Número de tópicos`, group=`Número de tópicos`)) +
  geom_line() +
  scale_fill_manual(values = wes_palette("Darjeeling1")) +
  scale_x_continuous(limits=c(9,10)) + scale_y_continuous(limits=c(0.3,0.35)) +
  labs(
    title = "Modelos LDA-Autor",
    subtitle = "Precision at k (P@k)"
  )
gg_zoom

## 1000 500
# ggplotly(gg)

########################## Topic Coherence
topic_coherence = topicos_modelos %>% 
  group_by(num_topics) %>% 
  summarise(topic_coherence = min(topic_coherence)) %>% 
  # top_n(10, topic_coherence) %>% 
  arrange(desc(topic_coherence)) %>% 
  mutate_all(~round(., 4)) %>% 
  rename(`Número de topicos` =num_topics, `Topic Coherence` = topic_coherence)

gg_topic = topic_coherence %>% 
  ggplot(aes(x = `Número de topicos`, y = `Topic Coherence`))+
  geom_line() +
  geom_point() +
  labs(
    title = "Modelos LDA-Autor",
    subtitle = "Topic Coherence"
  )

gg_topic

topic_coherence %>% 
  latex(file="", rowname=NULL) 

########################## 
topicos_modelos_106_111 <- read_csv("data/topicos_modelos_111_106.csv") %>% 
  rename(`Número de topicos` =num_topics, Accuracy = accuracy,  `Topic Coherence` = topic_coherence,  `Top k autores`= top_autor)
  
############# Top 5
top_5 = topicos_modelos_106_111 %>% 
  filter(top_autor == 5) %>% 
  select(`Número de topicos`, Accuracy, `Topic Coherence`) %>% 
  top_n(5, Accuracy) %>% 
  arrange(desc(Accuracy)) %>% 
  mutate_all(~round(., 4))

top_5 %>% 
  latex(file="", rowname=NULL) 

############# Top 10
top_10 = topicos_modelos_106_111 %>% 
  filter(top_autor == 10) %>% 
  select(`Número de topicos`, Accuracy, `Topic Coherence`) %>% 
  top_n(5, Accuracy) %>% 
  arrange(desc(Accuracy)) %>% 
  mutate_all(~round(., 4))

top_10 %>% 
  latex(file="", rowname=NULL) 
  
######################################

topicos_modelos_106_111 %>% 
  mutate(`Número de topicos` = factor(`Número de topicos`)) %>% 
  ggplot(aes(x=`Top k autores`, y=Accuracy, color=`Número de topicos`, group=trial_id)) + 
  geom_line()+
  labs(
    title = "Mejor modelos LDA-Autor",
    subtitle = "Precision at k (P@k)"
  )


######################################
topicos_modelos_106_111 %>% 
  mutate(`Número de topicos` = factor(`Número de topicos`)) %>% 
  filter(`Top k autores` %in% c(1,5,10)) %>% 
  ggplot(aes(x=`Número de topicos`, y=Accuracy)) + 
  geom_boxplot()+
  facet_grid(rows=vars(`Top k autores`), scales="free_y", labeller=label_bquote(rows =textstyle("P@")* .(`Top k autores`))) +
  labs(
    title = "Mejor modelos LDA-Autor",
    subtitle = "Precision at k (P@k)"
  )
  

################################################
# Kmeans tsne

k_means_tsne <- read_csv("data/kmeans_tsne.csv") %>% 
  mutate(group = factor(group))


k_means_tsne %>% 
  ggplot(aes(x=x, y=y, color=group, label=author_name )) + 
  geom_point() +
  # geom_text(hjust=0, vjust=0)+
  geom_text_repel()+
  labs(
    title = "K-meadias",
    subtitle = "Reducción de dimension via t-SNE"
  )


################################################
# Similarity
similarity_matrix <- read_csv("data/similarity_matrix.csv") %>% 
  rename(autor_i = X1) %>% 
  pivot_longer(!autor_i, names_to="autor_j",values_to = "Similitud")

similarity_matrix %>% 
  ggplot(aes(x= autor_j, y=autor_i, fill=Similitud)) + 
  geom_tile() +
  scale_fill_gradientn(colours = wes_palette("Zissou1", 100, type = "continuous")) +
  theme(axis.text.x = element_text(angle = 90))+
  labs(
    title = "Matriz de similitud",
    x="Autor",
    y="Autor"
  )


################################################
# UMAP
df_umap = read_csv("data/df_umap.csv") %>% 
  mutate(group = factor(group))

df_umap %>% 
  ggplot(aes(x=x, y=y, color=group, label=author_name )) + 
  geom_point() +
  # geom_text(hjust=0, vjust=0)+
  geom_text_repel(max.overlaps = 30, max.time=60)+
  labs(
    title = "Clustering espectral",
    subtitle = "Reducción de dimension via UMAP"
  )

################################################
# UMAP supervisado
df_umap_supervisado = read_csv("data/df_umap_supervisado.csv") %>% 
  mutate(group = factor(group))

df_umap_supervisado %>% 
  ggplot(aes(x=x, y=y, color=group, label=author_name )) + 
  geom_point() +
  # geom_text(hjust=0, vjust=0)+
  geom_text_repel(max.overlaps = 70, max.time=60)+
  labs(
    title = "Clustering espectral",
    subtitle = "Reducción de dimension via UMAP Supervisado"
  )
