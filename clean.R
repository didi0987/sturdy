

## Load Libraries ----

pacman::p_load(tidyverse, tidytext, gutenbergr,spacyr,networkD3)


## Load Book from Project Gutenberg ----

#book <- gutenberg_download(42671, mirror = "http://mirror.csclub.uwaterloo.ca/gutenberg/")
book <-data.table::fread("42671.txt", sep = "\t",quote="")

colnames(book)<-c("text")


book_text_only <- book %>%tail(nrow(book) - 93) %>% head(13242) 

print(str_detect(unlist(book_text_only[1:20]),regex("^chapter [\\divxlc]",ignore_case=TRUE)))
#print(cumsum(str_detect(unlist(book_text_only[1:20]),regex("^chapter [\\divxlc]",ignore_case=TRUE))))

print(cumsum(c(1,2,3,5)))


book_chapters <- book_text_only %>% 
  mutate(linenumber = row_number(),chapter = cumsum(str_detect(text,regex("^chapter [\\divxlc]",ignore_case = TRUE))))%>% 
  ungroup()

# reassign the line number
book_chapters_clean<- book_chapters%>% filter(!(text==""),!(str_detect(text,regex("^chapter [\\divxlc]",ignore_case = TRUE))))%>%mutate(linenumber=row_number())%>% ungroup()


book_chapters_combined <- book_chapters_clean %>%
  select(chapter, text) %>%
  group_by(chapter) %>% 
  mutate(text = paste0(text, collapse = " ")) %>%
  slice(1) %>%
  unique()%>%
  ungroup()

data("stop_words")


write.csv(book_chapters_clean,"clean_book.csv")

