#!/usr/local/bin/gnuplot

reset

set terminal pngcairo enhanced font "arial,11"  size 800,400 
set output 'histogram.png'

set title "Listings response times (ms)"
set key off
set yrange [0:*]

set boxwidth 0.9 absolute
set style fill solid 1.00 border lt -1
set style histogram clustered gap 1
set style data histograms

plot 'response_histogram.dat' using 2:xtic(1)


