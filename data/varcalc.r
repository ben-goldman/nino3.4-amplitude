# Imports
library(ncdf4)
library(zoo)
library(dplyr)
library(ggplot2)
library(WaveletComp)
library(reshape2)

# subtract ensemble mean from member
prepare <- function(x) {
    x.mean <- x %>% apply(1, mean)
    return(x - x.mean)
}

# calculate 20-year rolling variance
rollvar <- function(x) {
  out <- rollapply(x, width = 240, FUN = var, align = "center", fill = NA)
  return(out)
}

rollmean <- function(x) {
  out <- rollapply(x, width = 12, FUN = mean, align = "center", fill = NA)
  return(out)
}

getvar <- function(x) {
    apply(x, 2, rollvar)
}

# load variance from ensemble file
load_variance <- function(file) (read.table(file, sep = ",") %>% as.matrix %>% prepare %>% apply(2, rollvar))

load_temp <- function(file) (read.table(file, sep = ",") %>% as.matrix %>% apply(2, rollmean))

se <- function(x, ...) sd(x, ...)/sqrt(length(x))

# bind ensemble statistics into dataframe while preserving date offset
bind_stats <- function(this.date, this.mean, this.se, date.start = NA, date.end = NA) {
    if(length(this.mean) == length(this.date)) {
        this.df <- data.frame(date = this.date, mean = this.mean, se = this.se)
    } else {
        if(is.na(date.end)){
            date.end <- length(this.date)
        }
        if(is.na(date.start)){
            date.start <- 0
        }
        this.df <- data.frame(date = this.date, mean = c(
                                                    rep(NA, date.start),
                                                    this.mean,
                                                    rep(NA, (length(this.date) - date.end))),
                              se =
                                  c(rep(NA, date.start),
                                    this.se,
                                    rep(NA, (length(this.date) - date.end))))
        writeLines(as.character(date.start))
        writeLines(as.character(date.end))
        return(this.df)
    }
}

# Produce ensemble stats dataframe
make_df <- function(this, this.date, date.start = NA, date.end = NA) {
    this.mean <- this %>% apply(1, mean)
    this.se <- this %>% apply(1, se)
    writeLines(as.character(length(this.mean)))
    this.df <- bind_stats(this.date, this.mean, this.se, date.start, date.end)
    return(this.df)
}

make_df_manvar <- function(this, n, this.date, date.start = NA, date.end = NA) {
    this.mean <- this %>% apply(1, mean)
    this.se <- this %>% apply(1, se_bs, n = n)
    writeLines(as.character(length(this.mean)))
    this.df <- bind_stats(this.date, this.mean, this.se, date.start, date.end)
    return(this.df)
}

# calculate standard error in bootstrap process setting
se_bs <- function(x, n) {return(sd(x)/sqrt(n))}

# calculate single forcing impact through repeated random sampling
subtract.bootstrap <- function(data1, data2, reps, date, n) {
    len <- dim(data1)[1]
    num1 <- dim(data1)[2]
    num2 <- dim(data2)[2]
    out <- matrix(NA, ncol = reps, nrow = len)
#    writeLines(as.character(dim(out)))
#    writeLines(as.character(len))
    choice1 <- sample(x = 1:num1, size = reps, replace = TRUE)
    choice2 <- sample(x = 1:num2, size = reps, replace = TRUE)
    for(i in 1:reps){
#        writeLines(as.character(choice1[i]))
#        writeLines(as.character(choice2[i]))
        answer <- data1[, choice1[i]] - data2[, choice2[i]]
#        writeLines(as.character(length(answer)))
        out[, i] <- answer
    }
    out.mean <- out %>% apply(1, mean)
    out.se <- out %>% apply(1, se_bs, n)
    out.df <- bind_stats(date2, out.mean, out.se, date.start = 840)
    return(out.df)
}

subtract.bootstrap.raw <- function(data1, data2, reps) {
    len <- dim(data1)[1]
    num1 <- dim(data1)[2]
    num2 <- dim(data2)[2]
    out <- matrix(NA, ncol = reps, nrow = len)
#    writeLines(as.character(dim(out)))
#    writeLines(as.character(len))
    choice1 <- sample(x = 1:num1, size = reps, replace = TRUE)
    choice2 <- sample(x = 1:num2, size = reps, replace = TRUE)
    for(i in 1:reps){
#        writeLines(as.character(choice1[i]))
#        writeLines(as.character(choice2[i]))
        answer <- data1[, choice1[i]] - data2[, choice2[i]]
#        writeLines(as.character(length(answer)))
        out[, i] <- answer
    }
    return(out)
}

date1 <- seq(1920, 2100, length.out = 2172)
date2 <- seq(1850, 2100, length.out = 3012)

# CESM1 LENS and SF
ff1 <- load_temp("./data/CESM1/ff.csv")
ghg1 <- load_temp("./data/CESM1/ghg.csv")
aer1 <- load_temp("./data/CESM1/aer.csv")
bmb1 <- load_temp("./data/CESM1/bmb.csv")
luc1 <- load_temp("./data/CESM1/luc.csv")

# create ensemble statistics dataframe for CESM1 ff and SF
ff1_df <- make_df(ff1 %>% prepare () %>% getvar(), date2, date.start = 840)
ghg1_df <- make_df(ghg1 %>% getvar(), date2, date.start = 840)
aer1_df <- make_df(aer1 %>% getvar(), date2, date.start = 840)
bmb1_df <- make_df(bmb1 %>% getvar(), date2, date.start = 840)
luc1_df <- make_df(luc1 %>% getvar(), date2, date.start = 840)

ff1_mean <- mean(ff1_df$mean, na.rm = TRUE)

# ensemble statistics for all CESM1 members in single dataframe
cesm_1 <- ff1_df %>% mutate(case = "FF") %>%
  bind_rows(ghg1_df %>% mutate(case = "GHG")) %>%
  bind_rows(aer1_df %>% mutate(case = "AER")) %>%
  bind_rows(bmb1_df %>% mutate(case = "BMB"))  %>%
  bind_rows(luc1_df %>% mutate(case = "LUC"))
cesm_1$case <- as.factor(cesm_1$case)

# Ensemble statistics for CESM2 FF
ff2 <- load_temp("./data/CESM2/ff.csv")
ff2_df <- make_df(ff2 %>% prepare() %>% getvar(), date2)
ff_members <- ff1 %>% getvar() %>% melt() %>% mutate(date = (Var1/12 + 1920))
ff2_members <- ff2 %>% getvar() %>% melt() %>% mutate(date = (Var1/12 + 1850))

ff_compare <- ff1_df %>% mutate(case = "CESM1") %>%
    bind_rows(ff2_df %>% mutate(case = "CESM2"))
ff_compare$case <- as.factor(ff_compare$case)

# Bootstrap process to generate sf timeseries
reps <- 100

ghg1_sf <- subtract.bootstrap.raw(ff1, ghg1, reps) %>% getvar() %>% make_df_manvar(20, date2, date.start = 840)
aer1_sf <- subtract.bootstrap.raw(ff1, aer1, reps) %>% getvar() %>% make_df_manvar(20, date2, date.start = 840)
bmb1_sf <- subtract.bootstrap.raw(ff1, bmb1, reps) %>% getvar() %>% make_df_manvar(15, date2, date.start = 840)
luc1_sf <- subtract.bootstrap.raw(ff1, luc1, reps) %>% getvar() %>% make_df_manvar(5, date2, date.start = 840)

# bootstrap ensemble statistics in single dataframe
cesm1_sf <- data.frame(date = ff1_df$date, mean = ff1_df$mean, se = ff1_df$se, case = "FF") %>%
    bind_rows(ghg1_sf %>% mutate(case = "GHG")) %>%
    bind_rows(aer1_sf %>% mutate(case = "AER")) %>%
    bind_rows(bmb1_sf %>% mutate(case = "BMB")) %>%
    bind_rows(luc1_sf %>% mutate(case = "LUC"))
cesm1_sf$case <- as.factor(cesm1_sf$case)

# save all output data

write.csv2(cesm_1, "./data/CESM1/cesm1_stats.csv", row.names = FALSE)
write.csv2(ff2_df, "./data/CESM2/ff2_stats.csv", row.names = FALSE)
write.csv2(cesm1_sf, "./data/CESM1/cesm1_sf.csv", row.names = FALSE)
