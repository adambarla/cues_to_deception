library(readr)
library(ggplot2)

setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
data <- read_csv("processed_data.csv")

#### descriptive analysis ####
## summaries 
summary(data$group1_score) # strongly aligns with literature
summary(data$group2_score[data$cue_group=="GoodCues"]) # identical
summary(data$group2_score[data$cue_group=="BadCues"]) # cool

## 
table(data$cue_group)

## barplot next to one another
# data for the plot
freq_g1 <- as.vector(prop.table(table(data$group1_score)))
freq_bad <- as.vector(prop.table(table(data$group2_score[data$cue_group=="BadCues"])))
freq_good <- as.vector(prop.table(table(data$group2_score[data$cue_group=="GoodCues"])))

data_long <- data.frame(
  category = round(rep(seq(0,1, length.out = 4),3),3),
  Legend =  c(rep("No cues", 4), rep("bad cues", 4), rep("good cues", 4)),
  value = c(freq_g1, freq_bad, freq_good)
)

# plot
ggplot(data_long, aes(x = factor(category), y = value, fill = Legend)) +
  geom_bar(stat = "identity", position = "dodge") +
  labs(title = "Distributions of the scores",
       x = "Success rate",
       y = "Frequency") +
  theme_minimal()

## improvements
data$difference <- (data$group2_score-data$group1_score)*3 
table(data$difference, data$cue_group)
data$cue_group <- factor(data$cue_group,
                         levels = c("BadCues", "GoodCues"),
                         labels = c("bad cues", "good cues"))




ggplot(data, aes(x = factor(difference), fill = cue_group)) +
  geom_bar( alpha = 1, position = "dodge") +
  scale_fill_manual(values = c("bad cues" = "#F8766D", "good cues" = "#00BA38")) +
  labs(
    title = "Distributions of Score Differences",
    x = "Difference",
    y = "Count",
    fill = "Legend" 
  ) +
  theme_minimal()

### random bullshit 
big_data <- read_csv("processed_data_all_columns.csv")

## nationality
tapply(big_data$group1_score, big_data$nationality, mean)
table(big_data$nationality)

tapply(big_data$group2_score, big_data$nationality, mean)[c("Italy", "Morocco", "Lebanon", "France")]
tapply(big_data$group1_score, big_data$nationality, mean)[c("Italy", "Morocco", "Lebanon", "France")]

means_n1 <- tapply(big_data$group1_score, big_data$nationality, mean)[c("Italy", "Morocco", "Lebanon", "France")]
means_n2 <- tapply(big_data$group2_score, big_data$nationality, mean)[c("Italy", "Morocco", "Lebanon", "France")]

library(tibble)
library(tidyr)

df_nations <- tibble(
  nationality = rep(c("Italy", "Morocco", "Lebanon", "France"), 2),
  score_group = rep(c("Group 1", "Group 2"), each = 4),
  mean_score = c(means_n1, means_n2)
)

ggplot(df_nations, aes(x = score_group, y = mean_score, fill = nationality)) +
  geom_bar(stat = "identity", position = "dodge", color = "white", alpha = 0.9) +
  scale_fill_manual(values = c("France" = "#0055A4", "Italy" = "#007FFF", "Lebanon" = "#00BA38", "Morocco"= "firebrick")) +
  labs(
    title = "Average Scores by Nationality",
    x = "Nationality",
    y = "Mean Score",
    fill = "Legend"
  ) +
  theme_minimal()

## gender 
means_s1 <- tapply(big_data$group1_score, big_data$gender, mean)[1:2]
means_s2 <- tapply(big_data$group2_score, big_data$gender, mean)[1:2]

df_genders <- tibble(
  gender = rep(c("Female", "Male"), 2),
  score_group = rep(c("Group 1", "Group 2"), each = 2),
  mean_score = c(means_s1, means_s2)
)

ggplot(df_genders, aes(x = score_group, y = mean_score, fill = gender)) +
  geom_bar(stat = "identity", position = "dodge", color = "white", alpha = 0.9) +
  scale_fill_manual(values = c("Female" = "pink", "Male" = "#0055A4")) +
  labs(
    title = "Average Scores by Gender",
    x = "gender",
    y = "Mean Score",
    fill = "Legend"
  ) +
  theme_minimal()

##################
#### testing ####
## bad cues
bad_cues_df <- data.frame(
  y = c(data$group1_score[data$cue_group=="bad cues"], data$group2_score[data$cue_group=="bad cues"]),
  group = c(rep("Before cues", sum(data$cue_group=="bad cues")), rep("After cues", sum(data$cue_group=="bad cues")))
)
t.test(y ~ group, data = bad_cues_df)


## good cues 
good_cues_df <- data.frame(
  y = c(data$group1_score[data$cue_group=="good cues"], data$group2_score[data$cue_group=="good cues"]),
  group = c(rep("Before cues", sum(data$cue_group=="good cues")), rep("After cues", sum(data$cue_group=="good cues")))
)
t.test(y ~ group, data = good_cues_df)



### --- TEST 1 ---
# Do participants given GOOD cues show significantly greater improvement
# in lie detection performance than those given BAD cues?
# We test whether the average score change (difference) is higher for the "good cues" group.

t.test(
  difference ~ cue_group,
  data = data,
  alternative = "greater"  # one-sided test because we expect good cues > bad cues
)

### --- TEST 2 ---
# Does giving any kind of cues (good or bad) influence performance overall?
# This ignores the distinction between good and bad cues.
# We compare pre- and post-cue performance for all participants combined.

t.test(
  x = data$group1_score,     # performance before cues
  y = data$group2_score,     # performance after cues
  paired = TRUE,             # same participants tested before and after
  alternative = "two.sided"  # we test for any change (increase or decrease)
)

