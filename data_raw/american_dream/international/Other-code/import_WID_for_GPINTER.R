# This script downloads data from the World Inequality Database (WID) and exports it
# It first installs the WID R package
# The data downloaded includes bracket thresholds and brackets top averages for the entire population and for 14 brackets:
# p10p100, p20p100, p30p100, p40p100, p50p100, p60p100, p70p100, p80p100, p90p100, p95p100, p99p100, p99.9p100, p99.99p100, p99.999p100
# Please refer to https://github.com/WIDworld/wid-r-tool for full documentation
#
# The current script downloads data for France between 1950 and 2000

rm(list = ls())
install.packages("devtools")
devtools::install_github("WIDworld/wid-r-tool")
library(wid)
thresholds <- download_wid(indicators = "tptinc", areas = c("FR"),perc=c("p0p100","p10p100","p20p100","p30p100","p40p100","p50p100","p60p100","p70p100","p80p100","p90p100","p95p100","p99p100","p99.9p100","p99.99p100","p99.999p100"),year=1950:2000,pop="j",ages="992")
averages <- download_wid(indicators = "aptinc", areas = c("FR"),perc=c("p0p100","p10p100","p20p100","p30p100","p40p100","p50p100","p60p100","p70p100","p80p100","p90p100","p95p100","p99p100","p99.9p100","p99.99p100","p99.999p100"),year=1950:2000,pop="j",ages="992")
merged <- rbind(averages, thresholds)
merged <- merged[ -c(1:3) ]
write.csv(merged,"WID_data.csv")