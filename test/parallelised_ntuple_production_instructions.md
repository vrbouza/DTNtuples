# DTNtuples
Ntuples for the analysis of the CMS drift tubes detector performance. These are the instructions to produce parallelised ntuples using central samples.

### Installation
Do the following in a CRAB-supported environment.
```
cmsrel CMSSW_10_6_1_patch2
cd CMSSW_10_6_1_patch2/src/
cmsenv
git cms-merge-topic oglez:Phase2_CMSSW_10_6_0_pre4_Summer2019 # phase-2 unpacker: NOT NECESSARY UNLESS WORKING WITH SLICE TEST DATA
git cms-merge-topic -u pozzobon:DTHough_NP_20191004_106X_noL1T # MTT-CHT emulator
git cms-merge-topic -u dtp2-tpg-am:AM_106X_dev # AM emulator
git clone https://github.com/vrbouza/DTNtuples.git DTDPGAnalysis/DTNtuples
scramv1 b -j 5
```

### Ntuple parallelised production
The DT ntuple parallelised production is done with the help of the multicrab.py script. Previous to execute it, check that you have set CRAB and have a valid VOMS certificate.

Afterwards, you can send CRAB tasks for create ntuples by using the script as (inside the *test* folder)

```
python multicrab.py NCORES
```

where NCORES refers to the number of cores used to parallelise the CRAB task submission (this is an optional argument, it can be executed w/o it). But, **BEFORE EXECUTING THAT COMMAND**, you need to edit a couple of things of it, all of them at the beginning of the script. To be precise: the *name* and *outputdir* variables, and you will have to comment or uncomment the lines from the different Python diccionaries (samples, configuration and ageing scenarios) depending on the ntuples you want to obtain.

When you execute the script (as described previously), you will be told which tasks will be submitted to the WLGC and you will be asked for confirmation.

### Production checks while executing
As CRAB and Grafana are not very *helpful* sometimes, a specific Python tool, checkcrab.py, has been developed to cope with different (most probably not all) CRAB errors and problems and to provide a more credible status report than Grafana usually does.

Once you have your production ongoing, you can check its status using this tool as follows (inside the *test* folder).
```
python checkcrab.py WORKAREA NCORES
```
WORKAREA refers to the work area of your crab tasks (created as *analysis_* + *name*, where *name* is the homonymous variable used in multicrab) and is a compulsory argument, whereas NCORES refers to the same as before, and is optional.

Currently, the checkcrab.py script:
  * displays a complete report of your tasks, subdividing them in the different status they might have,
  * displays a complete report (whenever is possible) of all the jobs of all the tasks, also classifying them depending on their status,
  * allows you to resubmit failed jobs,
  * allows you to relaunch tasks whose submission failed or whose scheduler status is unretrievable (with a special treatment for those just-launched tasks).

Note that checkcrab.py does NOT check the output of the jobs in any way, nor is able of handling all possible CRAB problems/errors.

### Test execution
To execute a test of the ntuple production you can use cmsRun with the dtDphgNtuples_phase2_cfg.py, but you should set all the arguments that you want by hand. For example:

```
cmsRun dtDpgNtuples_phase2_cfg.py applyTriggerAgeing=True useRPC=1 ageingInput=sqlite_file:MuonAgeingNotFailures_3000fbm1_OLDSCENARIO.db ageingTag=MuonSystemAging_3000fbm1 applyRpcAgeing=True inputFolder=\"FOLDER\"
```

You can check the list of arguments in CentralSettings.py, and you can also see how they affect the production checking the python config file itself. You should subtitute FOLDER by a folder with rootfiles suitable to produce ntuples from.


