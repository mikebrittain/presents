#!/usr/local/bin/gnuplot

reset

set terminal png
set output 'response_times.png'
set yrange [0:2000]
set xdata time
set timefmt "%d/%B/%Y:%H:%M:%S"
set format x "%H:%M"

set title "Listings, generation times (ms)"
set ylabel "millisec"
set key off

set term png size 800,600

plot \
  'response_times.dat' using 1:2 with points lc rgb "#33ccff", \
   800 t "SLA" lw 2 lc rgb "#ff0000"
