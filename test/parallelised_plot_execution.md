# Parallelised efficiency and resolution plot execution
### Installation
It is not necessary to do this in a CRAB-supported environment, nor with an available CMSSW release.

```
git clone https://github.com/vrbouza/DTNtuples.git -b simulation_workflows
```
### Analysis -- Efficiencies
To analyse the ntuples to obtain efficiency plots, a parallelised helper (runall.py) is available and, by default, configured to TDR-like parameters, as well as the analysis itself (DTNtupleTPGSimAnalyzer_Efficiency.C). To execute the analysis, you need to configure the place in the script where the ntuples are located. Afterwards, do the following (inside the test folder).
```
python runall.py NCORES
```
Here, NCORES refer to the number of processes on which the execution is going to be parallelised. This script will produce files in the results subfolder that are needed for the plotter step.

Due to requirements from development of these plots, several configuration options are available to add suffixes, e.g.. This work consistently with the efficiencies plotter (plotter_eff.py).

### Analysis -- Resolutions
There is not a parallelising helper for this analysis, at this moment only the standard execution procedure is available, i.e.:

```
root -b -l
root [0] .x loadTPGSimAnalysis.C
root [1] DTNtupleTPGSimAnalyzer analysis("/PATH/TO/NTUPLE.root","OUTPUTNTUPLE.root")
root [2] analysis.Loop()
```
This loads internally the dependencies of the resolution analysis (DTNtupleTPGSimAnalyzer_Resolution.C) and executes it.

### Plotting
There are two plotting scripts, both of them executed the same way (python script.py). Because of rushes and development, their code might not be easy at first sight to understand. They are set by default with TDR-like parameters. Note that, **before executing them** the output path must be established.

For the efficiency plots, the script is plotter_eff.py, whereas the script plotter.py serves for the resolution ones.
