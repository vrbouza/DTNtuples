# DTNtuples
Ntuples for the analysis of the CMS drift tubes detector performance. These are the instructions to produce parallelised ntuples using central samples.

### Installation
Do the following in a CRAB-supported environment.
```
cmsrel CMSSW_10_6_1_patch2
cd CMSSW_10_6_1_patch2/src/
cmsenv
git cms-merge-topic oglez:Phase2_CMSSW_10_6_0_pre4_Summer2019 # phase-2 unpacker: NOT NECESSARY UNLESS WORKING WITH SLICE TEST DATA
git cms-merge-topic -u pozzobon:DTHough_NP_20191004_106X_noL1T # MTT-CHT emulator: NOT NECESSARY UNLESS THESE TP ARE WANTED
git cms-merge-topic -u dtp2-tpg-am:AM_106X_dev # AM emulator
git clone https://github.com/vrbouza/DTNtuples.git DTDPGAnalysis/DTNtuples
scramv1 b -j 5
```

### Customisation
The ntuples production depends on whether you want to produce them with the AM TP or the AM's TP as well as the HB ones too.

In the case that you do not want the HB's TP, you should comment all the hough algorithm-related lines, beginning from line ~150 the following:

```
process.load('L1Trigger.DTHoughTPG.DTTPG_cfi')
process.dtTriggerPhase2HbPrimitiveDigis = process.DTTPG.clone()
process.dtTriggerPhase2HbPrimitiveDigis.FirstBX = cms.untracked.int32(20)
process.dtTriggerPhase2HbPrimitiveDigis.LastBX = cms.untracked.int32(20)
process.dtTriggerPhase2HbPrimitiveDigis.dtDigiLabel = "simMuonDTDigis"
```

in addition of the respective entry in the process' path, which is:

```
+ process.dtTriggerPhase2HbPrimitiveDigis
```


If you want to have the HB's TP, you should take into account that this code is prepared to run with an automatised digi label selection, using the aged and the non aged too. The HB algorithm does not have this automatisation. You should therefore add the argument

```
dtDigiLabel = cms.InputTag("simMuonDTDigis")
```

to the DTTPG_cfi.py configuration file, that could in the minimum case has this shape:

```
import FWCore.ParameterSet.Config as cms

### Needed to access DTConfigManagerRcd and by DTTrig
#from L1TriggerConfig.DTTPGConfigProducers.L1DTTPGConfig_cff import *

DTTPG = cms.EDProducer( "DTTPG",
                        dtDigiLabel = cms.InputTag("simMuonDTDigis"),
)
```

Afterwards, you should look in the DTTPG.cc file for the line

```
  dtDigisToken = consumes< DTDigiCollection >( dtDigiTag );
```

and change it for (or comment it and add the following):

```
  dtDigisToken = consumes< DTDigiCollection >( aConfig.getParameter<edm::InputTag>("dtDigiLabel") );
```

Then, you should compile again everything.

### Test execution
To execute a test of the ntuple production you can use cmsRun with the dtDphgNtuples_phase2_cfg.py, but you should set all the arguments that you want by hand. For example:

```
cmsRun dtDpgNtuples_phase2_cfg.py applyTriggerAgeing=True useRPC=1 ageingInput=sqlite_file:MuonAgeingNotFailures_3000fbm1_OLDSCENARIO.db ageingTag=MuonSystemAging_3000fbm1 applyRpcAgeing=True inputFolder=\"FOLDER\"
```

You can check the list of arguments in CentralSettings.py, and you can also see how they affect the production checking the python config file itself. You should subtitute FOLDER by a folder with rootfiles suitable to produce ntuples from.


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

### Changing grouping algorithm of the AM
The production of ntuples with different grouping algorithms is not (yet) fully automatised. Currently, there is a line in the dtDpgNtuples_phase2_cfg.py file that sets the grouping. However this is still not automatised inside the multicrab & checkcrab scripts. Therefore, in the case of multicrab ntuple production with varied groupings for the AM algorithm, it is recommended to handle it manually: comment the present line that sets the grouping, which is
```
process.dtTriggerPhase2PrimitiveDigis.grouping_code = options.groupingCodeAM
```
and add it one like
```
process.dtTriggerPhase2PrimitiveDigis.grouping_code = 0
```
where you should change 0 for 1 (Hough transform-based grouping) or 2 (pseudo-Bayes grouping) accordingly.
