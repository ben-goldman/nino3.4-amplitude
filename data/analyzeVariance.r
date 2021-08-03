# Imports
library(ncdf4)
library(zoo)
library(dplyr)
library(ggplot2)
library(WaveletComp)
library(reshape2)

prepare <- function(x) {
    x.mean <- x %>% apply(1, mean)
    return(x - x.mean)
}

rollvar <- function(x) {
  out <- rollapply(x, width = 240, FUN = var, align = "center", fill = NA)
  return(out)
}

load_variance <- function(file) (read.table(file, sep = ",") %>% as.matrix %>% prepare %>% apply(2, rollvar))

se <- function(x, ...) sd(x, ...)/sqrt(length(x))

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

make_df <- function(this, this.date, date.start = NA, date.end = NA) {
    this.mean <- this %>% apply(1, mean)
    this.se <- this %>% apply(1, se)
    writeLines(as.character(length(this.mean)))
    this.df <- bind_stats(this.date, this.mean, this.se, date.start, date.end)
    return(this.df)
}

se_bs <- function(x, n) {return(sd(x)/sqrt(n))}

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

gsave <- function(name, plot = last_plot(), dimensions = c(8, 6), path = "./figures/") {
    ggsave(name, path = path, width = dimensions[1], height = dimensions[2])
}

date1 <- seq(1920, 2100, length.out = 2172)
date2 <- seq(1850, 2100, length.out = 3012)

# CESM1 LENS and SF
ff1 <- load_variance("./data/CESM1/ff.csv")
ghg1 <- load_variance("./data/CESM1/ghg.csv")
aer1 <- load_variance("./data/CESM1/aer.csv")
bmb1 <- load_variance("./data/CESM1/bmb.csv")
luc1 <- load_variance("./data/CESM1/luc.csv")

ff1_df <- make_df(ff1, date2, date.start = 840)
ghg1_df <- make_df(ghg1, date2, date.start = 840)
aer1_df <- make_df(aer1, date2, date.start = 840)
bmb1_df <- make_df(bmb1, date2, date.start = 840)
luc1_df <- make_df(luc1, date2, date.start = 840)

ff1_mean <- mean(ff1_df$mean, na.rm = TRUE)

cesm_1 <- ff1_df %>% mutate(case = factor("Full Forcing")) %>%
  bind_rows(ghg1_df %>% mutate(case = factor("Greenhouse"))) %>%
  bind_rows(aer1_df %>% mutate(case = factor("Aerosols"))) %>%
  bind_rows(bmb1_df %>% mutate(case = factor("Biomass")))  %>%
  bind_rows(luc1_df %>% mutate(case = factor("Land Use")))

ff2 <- load_variance("./data/CESM2/ff.csv")
ff2_df <- make_df(ff2, date2)

ff_members <- ff1 %>% melt() %>% mutate(date = (Var1/12 + 1920))

ff2_members <- ff2 %>% melt() %>% mutate(date = (Var1/12 + 1850))

ff_compare <- ff1_df %>% mutate(case = factor("CESM1")) %>%
    bind_rows(ff2_df %>% mutate(case = factor("CESM2")))

# Bootstrap process to generate sf timeseries
reps <- 1000

ghg1_sf <- subtract.bootstrap(ff1, ghg1, reps, date2, 20)
aer1_sf <- subtract.bootstrap(ff1, aer1, reps, date2, 20)
bmb1_sf <- subtract.bootstrap(ff1, bmb1, reps, date2, 15)
luc1_sf <- subtract.bootstrap(ff1, luc1, reps, date2, 5)

cesm1_sf <- data.frame(date = ff1_df$date, mean = ff1_df$mean - ff1_mean, se = ff1_df$se, case = factor("FF")) %>%
    bind_rows(ghg1_sf %>% mutate(case = factor("GHG"))) %>%
    bind_rows(aer1_sf %>% mutate(case = factor("AER"))) %>%
    bind_rows(bmb1_sf %>% mutate(case = factor("BMB"))) %>%
    bind_rows(luc1_sf %>% mutate(case = factor("LUC")))

xlim1 <- c(1930, 2090)
xlim2 <- c(1860, 2090)

l <- 0.2
m <- 0.5
d <- 0.8

ggplot(cesm_1, aes(y = mean, x = date, color = case, fill = case, ymin = (mean - 2*se), ymax = (mean + 2*se)), show.legend = FALSE) +
  geom_line() +
  geom_ribbon(alpha = m, color = NA) +
  facet_grid(case ~ .) +
  theme(legend.position = "none") +
  xlim(xlim1) +
  labs(title = "CESM1 20-Year Variance", x = "Date", y = "Variance", color = "Case")
gsave("cesm1.pdf")

ggplot(cesm_1, aes(y = mean, x = date, color = case, fill = case, ymin = (mean - 2*se), ymax = (mean + 2*se))) +
  geom_line() +
  geom_ribbon(alpha = l, color = NA) +
  xlim(xlim1) +
  labs(title = "CESM1 20-Year Variance", x = "Date", y = "Variance", color = "Case", fill = "Case")
gsave("cesm1_2.pdf")

ggplot(ff1_df, aes(y = mean - ff1_mean, x = date, ymin = (mean - 2 * se - ff1_mean), ymax = (mean + 2 * se - ff1_mean))) +
  geom_line() +
  geom_ribbon(alpha = m, color = NA) +
  xlim(xlim1) +
  labs(title = "CESM1 LENS 20-Year Variance", x = "Date", y = "Variance", color = "Case", fill = "Case")
gsave("ff1.pdf")

ggplot(ff2_df, aes(y = mean, x = date, ymin = (mean - 2*se), ymax = (mean + 2*se))) +
  geom_line() +
  geom_ribbon(alpha = m, color = NA) +
  xlim(xlim2) +
  labs(title = "CESM2 LENS 20-Year Variance", x = "Date", y = "Variance", color = "Case", fill = "Case")
gsave("ff2.pdf")
## ggplot(ff_members, aes(x = date, y = value, group = Var2)) +
##     geom_line(alpha = .1)

## ggplot(ff2_members, aes(x = date, y = value, group = Var2)) +
##     geom_line(alpha = .1)

ggplot(ff_compare, aes(y = mean, x = date, color = case, fill = case, ymin = (mean - 2 * se), ymax = (mean + 2 * se))) +
  geom_line() +
  geom_ribbon(alpha = l, color = NA) +
  xlim(xlim2) +
  labs(title = "LENS 20-Year Variance", x = "Date", y = "Variance", color = "Case", fill = "Case")
gsave("ff_compare.pdf")

ggplot(cesm1_sf, aes(y = mean, x = date, color = case, fill = case, ymin = (mean - 2 * se), ymax = (mean + 2 * se))) +
  facet_grid(case ~ .) +
  geom_line() +
  geom_ribbon(alpha = m, color = NA) +
  xlim(xlim1) +
  labs(title = "CESM1 20-Year Variance", subtitle = "Single Forcing Net Impact", x = "Date", y = "Variance", color = "Case", fill = "Case")
gsave("cesm1_sf.pdf")

ggplot(cesm1_sf, aes(y = mean, x = date, color = case, fill = case, ymin = (mean - 2 * se), ymax = (mean + 2 * se))) +
  geom_line() +
  geom_ribbon(alpha = l, color = NA) +
  xlim(xlim1) +
  labs(title = "CESM1 20-Year Variance", subtitle = "Single Forcing Net Impact", x = "Date", y = "Variance", color = "Case", fill = "Case")
gsave("cesm1_sf_2.pdf")

ggplot(cesm1_sf %>% filter(case != "LUC"), aes(y = mean, x = date, color = case, fill = case, ymin = (mean - 2 * se), ymax = (mean + 2 * se))) +
  geom_line() +
  geom_ribbon(alpha = l, color = NA) +
  xlim(xlim1) +
  labs(title = "CESM1 20-Year Variance", subtitle = "Single Forcing Net Impact", x = "Date", y = "Variance", color = "Case", fill = "Case")
gsave("cesm1_sf_3.pdf")
