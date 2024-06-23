# HPCC simulation
This is the simulator for HPCC, HPCC-PINT, HPCC-LINT, and HPCC-DINT, which are other versions of HPCC implementing PINT, LINT, and DINT protocols
This simulator is modified from the [HPCC-PINT](https://github.com/ProbabilisticINT/HPCC-PINT) repository, which is introduced in PINT: Probabilistic In-band Network Telemetry (ACM SIGCOMM 2020) and implements LINT and DINT based on the original [DINT](https://github.com/HenriqueBBrum/DINT) repository.

## NS-3 simulation
The ns-3 simulation is under `simulation/`. Refer to the README.md under it for more details.

## Traffic generator
The traffic generator is under `traffic_gen/`. Refer to the README.md under it for more details.

## Analysis
We provide a few analysis scripts under `analysis/` to view the packet-level events, and analyzing the fct in the same way as [PINT](https://liyuliang001.github.io/publications/pint.pdf) Figure 7 and 8.
Refer to the README.md under it for more details.

## Generating the figures in the paper
1. Generate traffic workload at 50% load: `bash gen_traffic_files.sh`

2. Set error rate: `python set_error_rate.py <new error rate>`

* By default the error rate is set to `0`


3. Run simulations: 

* First enter the folder and configure: `bash build.sh` 

* HPCC-PINT under web search: `bash run_hpcc_pint1_wb.sh`

* HPCC-PINT under Hadoop: `bash run_hpcc_pint1_fb.sh`

* HPCC-PINT with p=1/16 of packets carrying feedback under web search: `bash run_hpcc_pint16_wb.sh`

* HPCC-PINT with p=1/16 of packets carrying feedback under Hadoop: `bash run_hpcc_pint16_fb.sh`

* HPCC-PINT with p=1/256 of packets carrying feedback under web search: `bash run_hpcc_pint256_wb.sh`

* HPCC-PINT with p=1/256 of packets carrying feedback under Hadoop: `bash run_hpcc_pint256_fb.sh`

* HPCC under web search: `bash run_hpcc_wb.sh`

* HPCC under Hadoop: `bash run_hpcc_fb.sh`

* Each simulation will run for about 1 day.

4. Get the fct analysis result

* First enter the folder `cd analysis`

* Our plot script requires python-tk. So if you don't have it, please install it (e.g., `sudo apt install python-tk`).

* Fig 7: `bash plotVsHPCC.sh`. Figures are called `web_search_95p.pdf` and `facebook_95p.pdf`.

* Fig 8: `bash plotProbHPCC.sh`. Figures are called `ProbHPCC_PINT_wb.pdf` and `ProbHPCC_PINT_fb.pdf`.

<!-- ## More results
More results of HPCC in various topologies and conditions can be seen in the paper. -->

## Questions
For technical questions, please create an issue in this repo, so other people can benefit from your questions. 
You may also check the issue list first to see if people have already asked the questions you have :)

For other questions, please contact the authors of the paper.
