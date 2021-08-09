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

# load variance from ensemble file
load_variance <- function(file) (read.table(file, sep = ",") %>% as.matrix %>% prepare %>% apply(2, rollvar))

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
