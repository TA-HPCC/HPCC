# Analysis
This folder includes code and scripts for analysis.

## FCT analysis
`fct_analysis.py` is used to analyze fct. It reads multiple fct files (simulation's output), and prints data that can produce figures like Figure 11 (a) and (c) in [HPCC paper](https://liyuliang001.github.io/publications/hpcc.pdf).

Usage: please check `python fct_analysis.py -h` and read line 20-26 in `fct_analysis.py`

## How To Use FCT Analysis scipts
This is a short guide of how to use our analysis script, if needed you can change the script accordingly
### For plotting HPCC INT vs PINT vs LINT vs DINT
1. run all the simulation and make sure all of the fct files are in simulation/mix (**if using our script, don't rename the fct files**)
2. `bash plotWb.sh` (for web-search traffic) or `bash plotFb.sh` (for facebook-hadoop traffic)

### For plotting DINT parameter tuning
1. run the simulation one by one with the diffrent parameters according to your need

2. rename tail of the fct file name before running the next simulation according to this :
- obs window : dint_[obs_window] ; example : fct_fat_fb50_b100_dint_1m.txt
- alpha : dint_a[alpha value] ; example : fct_fat_fb50_b100_dint_a1.5.txt
- k : dint_k[k value] ; example : fct_fat_fb50_b100_dint_k16.txt

3. change line 24-27 of `fct_analysis_dint.py` to the files you just rename following this :
- for obs window :
```
'dint_1k',
'dint_10k',
'dint_100k',
'dint_1m',
```
- for alpha :
```
'dint_a1.5',
'dint_a1.25',
'dint_a1.125',
'dint_a1.0625',
```
- for k :
```
'dint_k16',
'dint_k8',
'dint_k4',
'dint_k2',
```
if you use other values for your experiments or want to change the order, you need to modify `plotDINT.py` accordingly

4. modify `plotDINTwb.sh` or `plotDINTfb.sh` to suit your need. Check `fct_analysis_dint.py` and `plotDINT.py` for how to change the parameters to your needs

5. `bash plotDINTWb.sh` (for web-search traffic) or `bash plotDINTFb.sh` (for facebook-hadoop traffic)



## Trace reader guide from original PINT repo (This experiment doesn't use trace reader)
`trace_reader` is used to parse the .tr files output by the simulation.

### Usage: 
1. `make trace_reader`

2. `./trace_reader <.tr file> [filter_expr]`. The filter_expr is used to filter events. For example, `time > 2000010000` will display only events after 2000010000, `sip=0x0b000101&dip=0x0b000201` will display only events with sip=0x0b000101 and dip=0x0b000201. Feel free to play with it (we may come up with more detailed descriptions in the future. For now, please read trace_filter.hpp for more details).

### Output:
Each line is like:

`2000055540 n:338 4:3 100608 Enqu ecn:0 0b00d101 0b012301 10000 100 U 161000 0 3 1048(1000)`

It means: at time 2000055540ns, at node 338, port 4, queue #3, the queue length is 100608B, and a packet is enqueued; the packet does not have ECN marked, is from 11.0.209.1:10000 to 11.1.35.1:100, is a data packet (U), sequence number 161000, tx timestamp 0, priority group 3, packet size 1048B, payload 1000B.

There are other types of packets. Please refer to print_trace() in utils.hpp for details.