#!/usr/local/bin/gnuplot

reset

set terminal png
set output 'trends.png'

set grid
set title "Listings, generation times (ms)"
set ylabel "millisec"
set yrange [0:*]
set key below
set term png size 800,600

set xdata time
set timefmt "%d/%B/%Y:%H:%M:%S"
set format x "%H:%M"

plot 'response_median_perc95.dat' \
using 1:2 with lines linecolor rgb "#2192bf" title "Median", \
"" using 1:3 with lines linecolor rgb "#548c6c" title "95th Percentile", \
800 title "SLA" lw 2 linecolor rgb "#f28705"


