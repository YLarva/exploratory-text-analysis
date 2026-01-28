# family analysis
# 12 december 2025
# Ryan Hull


# libraries
library(ggplot2)
library(dplyr)
library(tidyr)


# data
marge <- read.csv("marge_annotated_dialogue.csv")
bart <- read.csv("bart_annotated_dialogue.csv")
lisa <- read.csv("lisa_annotated_dialogue.csv")

marge_family <- marge[marge$annotation=="2",]
bart_family <- bart[bart$annotation=="2",]
lisa_family <- lisa[lisa$annotation=="2",]

# names and regex
lisa_names <- c("lis","lisa","Lis","Lisa","sister")
bart_names <- c("Bart","bart","son")
marge_names <- c("marge","mom","Mom","Marge","Mama", "mother")
maggie_names <- c("maggie","Maggie")
homer_names <- c("Homer", "Homie", "Home", "Dad", "Father")

lisa_rgx <- paste(lisa_names, collapse = "|")
bart_rgx <- paste(bart_names, collapse="|")
marge_rgx <- paste(marge_names, collapse="|")
maggie_rgx <- paste(maggie_names, collapse="|")
homer_rgx <- paste(homer_names, collapse = "|")

bart_mentions_lisa <- sum(grepl(lisa_rgx, df=bart_family$dialogue, ignore.case=TRUE))
bart_mentions_marge <- sum(grepl(marge_rgx, df=bart_family$dialogue, ignore.case=TRUE))
bart_mentions_maggie <- sum(grepl(maggie_rgx, df=bart_family$dialogue, ignore.case=TRUE))
bart_mentions_homer <- sum(grepl(homer_rgx, df=bart_family$dialogue, ignore.case=TRUE))

lisa_mentions_bart <- sum(grepl(bart_rgx, df=bart_family$dialogue, ignore.case=TRUE))
lisa_mentions_marge <- sum(grepl(marge_rgx, df=bart_family$dialogue, ignore.case=TRUE))
lisa_mentions_maggie <- sum(grepl(maggie_rgx, df=bart_family$dialogue, ignore.case=TRUE))
lisa_mentions_homer <- sum(grepl(homer_rgx, df=bart_family$dialogue, ignore.case=TRUE))

marge_mentions_bart <- sum(grepl(bart_rgx, df=bart_family$dialogue, ignore.case=TRUE))
marge_mentions_lisa <- sum(grepl(lisa_rgx, df=bart_family$dialogue, ignore.case=TRUE))
marge_mentions_maggie <- sum(grepl(maggie_rgx, df=bart_family$dialogue, ignore.case=TRUE))
marge_mentions_homer <- sum(grepl(homer_rgx, df=bart_family$dialogue, ignore.case=TRUE))

# above won't work for finding totals. below function will
count_occ <- function(pattern, text) {
  sum(lengths(regmatches(text, gregexpr(pattern, text, ignore.case = TRUE))))
}

bart_mentions_lisa   <- count_occ(lisa_rgx,   bart_family$dialogue)
bart_mentions_marge  <- count_occ(marge_rgx,  bart_family$dialogue)
bart_mentions_maggie <- count_occ(maggie_rgx, bart_family$dialogue)
bart_mentions_homer  <- count_occ(homer_rgx,  bart_family$dialogue)

lisa_mentions_bart   <- count_occ(bart_rgx,   lisa_family$dialogue)
lisa_mentions_marge  <- count_occ(marge_rgx,  lisa_family$dialogue)
lisa_mentions_maggie <- count_occ(maggie_rgx, lisa_family$dialogue)
lisa_mentions_homer  <- count_occ(homer_rgx,  lisa_family$dialogue)

marge_mentions_bart   <- count_occ(bart_rgx,   marge_family$dialogue)
marge_mentions_lisa   <- count_occ(lisa_rgx,   marge_family$dialogue)
marge_mentions_maggie <- count_occ(maggie_rgx, marge_family$dialogue)
marge_mentions_homer  <- count_occ(homer_rgx,  marge_family$dialogue)



# HEAT MAP !!!

matrix <- matrix(
  c(
    0, bart_mentions_lisa, bart_mentions_marge, bart_mentions_homer, bart_mentions_maggie,
    lisa_mentions_bart, 0, lisa_mentions_marge, lisa_mentions_homer, lisa_mentions_maggie,
    marge_mentions_bart, marge_mentions_lisa, 0, marge_mentions_homer, marge_mentions_maggie
  ),
  nrow=3,
  byrow=TRUE
)

rownames(matrix) <- c("Bart", "Lisa", "Marge")
colnames(matrix) <- c("Bart","Lisa","Marge","Homer","Maggie")

mentions_df <- as.data.frame(matrix) %>%
  mutate(Speaker = rownames(.)) %>%
  pivot_longer(
    cols = Speaker, 
    names_to = "Adressee",
    values_to = "Count"
  )

# need different df format.... above not working. do manually

mentions_wide <- data.frame(
  Speaker = c("Bart", "Lisa", "Marge"),
  Bart = c(0, 39, 38),
  Lisa = c(15, 0, 24),
  Marge = c(12, 12, 0),
  Homer = c(34, 25, 52),
  Maggie = c(1, 6, 11)
)

mentions_df_wide_wide <- mentions_wide %>% ## THIS IS THE USEFUL ONE
  pivot_longer(
    cols = -Speaker,
    names_to = "Target",
    values_to = "Count"
  )

# the heat
ggplot(mentions_df_wide_wide, aes(x = Speaker, y = Target, fill = Count)) +
  geom_tile(color = "white") +
  scale_fill_gradient(low = "white", high = "red") +
  theme_minimal() +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1),
    panel.grid = element_blank()
  ) +
  labs(fill = "Mentions",
       title = "Simpsons Family Mentions Breakdown")



# bar chart
ggplot(mentions_df_wide_wide, aes(x = Speaker, y = Count, fill = Target)) +
  geom_col(position = position_dodge(width = 0.7)) +
  labs(
    x = "Speaker",
    y = "Number of Mentions",
    fill = "Target"
  ) +
  theme_minimal()
  

# quick analysis of numbers
all <-  rbind(bart, lisa, marge)

nb_all <- nrow(all)

annotation_2 <- all[all$annotation =="2",]
nb_family <- nrow(annotation_2)

percent_family <- nb_family / nb_all
print(percent_family)




