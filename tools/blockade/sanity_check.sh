#!/bin/bash

slow_sec=(100us 200us 300us 400us 500us 600us 700us 800us 900us 1ms 2ms 3ms 4ms 5ms 6ms 7ms 8ms 9ms 10ms 20ms 30ms 40ms 50ms 60ms 70ms 80ms 90ms 100ms 200ms 300ms 400ms 500ms 600ms 700ms 800ms 900ms 1s)

flaky_sec=(p0.1 p0.2 p0.3 p0.4 p0.5 p0.6 p0.7 p0.8 p0.9 p1 p2 p3 p4 p5 p6 p7 p8 p9 p10 p20 p30 p40 p50 p60 p70 p80 p90 p100)


for i in "${flaky_sec[@]}"; do
   cat blockade-flaky-${i}.yaml | grep ${i#p}%
done


for i in "${slow_sec[@]}"; do
  cat blockade-slow-${i}.yaml | grep $i
done

