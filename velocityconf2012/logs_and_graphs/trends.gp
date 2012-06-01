#!/usr/local/bin/gnuplot

reset
set terminal pngcairo enhanced font "arial,11"  size 800,600                            
set output 'trends.png'

set grid
set title "Listings, generation times (ms)"
set ylabel "millisec"
set yrange [0:*]
set key below
set style fill solid 0.20 border

set xdata time
set timefmt "%d/%B/%Y:%H:%M:%S"
set format x "%H:%M"

plot 'response_median_perc95.dat' \
using 1:3 with filledcurve x1 linewidth 1 linecolor rgb "#548c6c" title "95th Percentile", \
"" using 1:2 with lines linewidth 2 linecolor rgb "#2192bf" title "Median", \
800 title "SLA" linewidth 2 linecolor rgb "#f28705"

