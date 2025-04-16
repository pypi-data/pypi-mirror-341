Hairfall<-c(12,13,14,17,15,18,12,13,14,17,19,18)
Hairfall

Hairfall.timeseries<-ts(Hairfall,start=c(2024,4),frequency=12)
Hairfall.timeseries
plot(Hairfall.timeseries)   