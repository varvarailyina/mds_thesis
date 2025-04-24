###################### MDS THESIS: APPLY ED8 DICTIONARY ########################
# varvara ilyina

# ed8 function adopted from Widmann / Wich (2023) analysis
# https://github.com/tweedmann/3x8emotions


# clear environment
rm(list = ls())

# load libraries
library(quanteda)
library(tidyverse)
library(stringr)

# set wd
setwd("/Users/varvarailyina/hertie/mds_thesis/")

# load in dictionary
ed8 <- dictionary(file = "./data/in/ed8.yml", format = "YAML")

# load data
data <- read_csv("./data/out/df_sentences.csv")

#-------------------------------------------------------------------------------

# select needed variables
data <- data %>%
  as.data.frame() %>%
  select(doc_id, party, date, month, text, sentence)

# clean sentence column
data <- data %>%
  
  # drop short sentences (length > 3)
  filter(str_length(str_trim(sentence)) > 3) %>%
  
  # drop if just symbols
  filter(!str_detect(sentence, '^[\\W_]+$')) %>%
  
  # drop if filenames or URLs
  filter(!str_detect(sentence, '(?i)\\.pdf$|\\.docx?$|\\.csv$|http[s]?://|www\\.')) %>%
  
  # drop if emails
  filter(!str_detect(sentence, '\\S+@\\S+')) %>%
  
  # drop low-information sentences
  filter(str_count(sentence, '\\S+') > 2) %>%
  
  # drop duplicates and NAs
  filter(!is.na(sentence)) %>%
  distinct(sentence, .keep_all = TRUE) %>%
  
  # reset row index
  mutate(row_id = row_number())

# set rownames
rownames(data) <- data$row_id

#-------------------------------------------------------------------------------

# define function to apply ed8 dictionary on sentence-level
get_ed8_emotions <- function(data){
  
  # create a corpus from df
  corp <- corpus(data$sentence, docvars = data)
  
  # tokenize corpus and pre-process (remove punctuation, numbers, and urls)
  toks <- tokens(corp, remove_punct = TRUE, remove_numbers = TRUE, remove_url = TRUE)
  
  # create DFM just to measure number of terms before removing stopwords
  terms_dfm <- dfm(toks)
  
  # create bigram-compounds to include negation control
  toks_neg_bigram <- tokens_compound(toks, pattern = phrase("nicht *"))
  toks_neg_bigram <- tokens_compound(toks_neg_bigram, pattern = phrase("nichts *"))
  toks_neg_bigram <- tokens_compound(toks_neg_bigram, pattern = phrase("kein *"))
  toks_neg_bigram <- tokens_compound(toks_neg_bigram, pattern = phrase("keine *"))
  toks_neg_bigram <- tokens_compound(toks_neg_bigram, pattern = phrase("keinen *"))
  
  # turn tokens into DFM, remove stopwords
  emo_dfm <- dfm(toks_neg_bigram, remove = stopwords("de"))
  
  # apply dictionary
  dict_dfm_results <- dfm_lookup(emo_dfm, ed8)
  
  # convert results back to data frame
  results_df <- cbind(data, convert(dict_dfm_results, to = 'data.frame'))
  
  # assign length to each documents
  results_df$terms_raw <- ntoken(terms_dfm)
  results_df$terms <- ntoken(emo_dfm)
  
  return(results_df)
}


# apply function (need a "sentence" column)
results <- get_ed8_emotions(data)

#-------------------------------------------------------------------------------

# create normalized emotional scores (divide ed8-scores by doc length)
df_res <- results %>%
  janitor::clean_names() %>%
  mutate(
    ed8_anger_norm = ed8_anger / terms,
    ed8_fear_norm = ed8_fear / terms,
    ed8_disgust_norm = ed8_disgust / terms,
    ed8_sadness_norm = ed8_sadness / terms,
    ed8_joy_norm = ed8_joy / terms,
    ed8_enthusiasm_norm = ed8_enthusiasm / terms,
    ed8_pride_norm = ed8_pride / terms,
    ed8_hope_norm = ed8_hope / terms
    ) %>%
  select(-row_id, -doc_id_2)

# save results
write.csv(df_res, "./data/out/df_res_ed8.csv")
