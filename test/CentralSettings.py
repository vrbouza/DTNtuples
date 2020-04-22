import os, sys
from multiprocessing import Process
### General settings
UnretrieveThreshold = 7

### Diccionaries with settings
running_options = {
    'noage_norpc'          : ["inputFolder=", 'applyTriggerAgeing=False', 'applySegmentAgeing=False', 'useRPC=0'],
    'age_norpc'            : ["inputFolder=", 'applyTriggerAgeing=True',  'applySegmentAgeing=True',  'useRPC=0'],
    'age_norpc_youngseg'   : ["inputFolder=", 'applyTriggerAgeing=True',  'applySegmentAgeing=False', 'useRPC=0'], # Ageing in trigger, but not in reco segments
    'noage_withrpc'        : ["inputFolder=", 'applyTriggerAgeing=False', 'applySegmentAgeing=False', 'useRPC=1'],
    'age_withrpc'          : ["inputFolder=", 'applyTriggerAgeing=True',  'applySegmentAgeing=True',  'useRPC=1'],
    'age_withrpc_youngseg' : ["inputFolder=", 'applyTriggerAgeing=True',  'applySegmentAgeing=False', 'useRPC=1'], # Ageing in trigger, but not in reco segments
}

ageing_scenarios = {
    'muonage_norpcage_nofail_3000_OLD': ['ageingInput=sqlite_file:MuonAgeingNotFailures_3000fbm1_OLDSCENARIO.db',         "ageingTag=MuonSystemAging_3000fbm1",                     "applyRpcAgeing=False"],
    'muonage_norpcage_nofail_3000'    : ['ageingInput=sqlite_file:MuonAgeingAndFailures_3000fbm1_DT_L1TTDR_v1_mc.db',     "ageingTag=MuonAgeingAndFailures_3000fbm1_DT_L1TTDR",     "applyRpcAgeing=False"],
    'muonage_norpcage_fail_3000'      : ['ageingInput=sqlite_file:MuonAgeingAndFailures_3000fbm1_DT-RPC_L1TTDR_v1_mc.db', "ageingTag=MuonAgeingAndFailures_3000fbm1_DT-RPC_L1TTDR", "applyRpcAgeing=True"],
    'muonage_norpcage_nofail_1000'    : ['ageingInput=sqlite_file:MuonAgeingAndFailures_1000fbm1_DT_L1TTDR_v1_mc.db',     "ageingTag=MuonAgeingAndFailures_1000fbm1_DT_L1TTDR",     "applyRpcAgeing=False"],
    'muonage_norpcage_fail_1000'      : ['ageingInput=sqlite_file:MuonAgeingAndFailures_1000fbm1_DT-RPC_L1TTDR_v1_mc.db', "ageingTag=MuonAgeingAndFailures_1000fbm1_DT-RPC_L1TTDR", "applyRpcAgeing=True"],
    ""                                : ["applyRpcAgeing=False"],
}

dataset = {
    "nopu"    : "/Mu_FlatPt2to100-pythia8-gun/PhaseIITDRSpring19DR-NoPU_106X_upgrade2023_realistic_v3-v1/GEN-SIM-DIGI-RAW",
    "pu200"   : "/Mu_FlatPt2to100-pythia8-gun/PhaseIITDRSpring19DR-PU200_106X_upgrade2023_realistic_v3-v2/GEN-SIM-DIGI-RAW",
    'nu_pu140': '/Nu_E10-pythia8-gun/PhaseIITDRSpring19DR-PU140_106X_upgrade2023_realistic_v3_ext3-v1/GEN-SIM-DIGI-RAW',
    'nu_pu200': '/Nu_E10-pythia8-gun/PhaseIITDRSpring19DR-PU200_106X_upgrade2023_realistic_v3-v3/GEN-SIM-DIGI-RAW',
    'nu_pu250': '/Nu_E10-pythia8-gun/PhaseIITDRSpring19DR-PU250_106X_upgrade2023_realistic_v3_ext2-v1/GEN-SIM-DIGI-RAW',
    'nu_pu300': '/Nu_E10-pythia8-gun/PhaseIITDRSpring19DR-PU300_106X_upgrade2023_realistic_v3_ext1-v2/GEN-SIM-DIGI-RAW',
}


### Function definitions
#configurationCache = {}
def LaunchCRABTask(tsk):
    sample, cfg, scn, workarea, outputdir = tsk
    from CRABAPI.RawCommand       import crabCommand
    from CRABClient.UserUtilities import config
    from CRABClient.JobType       import CMSSWConfig

    print "# Launching CRAB task for sample {s}, config. {c} and ageing scenario {sc}.".format(s = sample, c = cfg, sc = scn)
    #print "\nsyspath:", sys.path
    #print "\ncwd:", os.getcwd()
    #sys.exit()
    config = config()
    def submit(config):
        res = crabCommand('submit', config = config )

    config.General.workArea     = workarea
    config.General.transferLogs = True

    config.JobType.pluginName  = 'Analysis'

    config.JobType.psetName    = 'dtDpgNtuples_phase2_cfg.py'
    if scn != "": config.JobType.inputFiles  = [ageing_scenarios[scn][0].replace("ageingInput=sqlite_file:", "")]
    config.JobType.pyCfgParams = running_options[cfg] + ageing_scenarios[scn]

    config.JobType.maxMemoryMB = 2500
    config.JobType.allowUndistributedCMSSW = True

    config.Data.inputDBS    = 'global'
    config.Data.splitting   = 'FileBased'
    #config.Data.splitting   = 'Automatic'
    config.Data.unitsPerJob = 1
    config.Data.publication = False
    config.Data.allowNonValidInputDataset = True

    config.Data.outLFNDirBase = outputdir

    config.Site.storageSite = 'T2_ES_IFCA'
    #config.Site.storageSite = 'T2_CH_CERN'
    #config.Site.blacklist   = ['T2_BR_SPRACE', 'T2_US_Wisconsin', 'T1_RU_JINR', 'T2_RU_JINR', 'T2_EE_Estonia']
    #config.Site.blacklist   = []
    config.Site.ignoreGlobalBlacklist = True

    config.General.requestName   = sample + '_' + cfg + ("_" + scn) * (scn != "")
    config.Data.inputDataset     = dataset[sample]
    config.Data.outputDatasetTag = sample + '_' + cfg + ("_" + scn) * (scn != "")

    #res = crabCommand('submit', config = config)

    p = Process(target=submit, args=(config,))
    p.start()
    p.join()

    del config, p
    #CMSSWConfig.configurationCache.clear() #### NOTE: this is done in order to allow the parallelised CRAB job submission. For further
                                           ## information, please check the code on [1], the commit of [2] and the discussion of [3].
                                           ## [1]: https://github.com/dmwm/CRABClient/blob/master/src/python/CRABClient/JobType/CMSSWConfig.py
                                           ## [2]: https://github.com/dmwm/CRABClient/commit/a50bfc2d1f32093b76ba80956ee6c5bd6d61259e
                                           ## [3]: https://github.com/dmwm/CRABClient/pull/4824
    return


def confirm(message = "Do you wish to continue?"):
    """
    Ask user to enter y(es) or n(o) (case-insensitive).
    :return: True if the answer is Y.
    :rtype: bool
    """
    answer = ""
    while answer not in ["y", "n", "yes", "no"]:
        answer = raw_input(message + " [Y/N]\n").lower()
    return answer[0] == "y"


def CheckExistanceOfFolders(listoftasks):
    listoftaskswcreatedfolder = []
    for tsk in listoftasks:
        if os.path.isdir("./" + tsk[3] + "/crab_" + tsk[0] + '_' + tsk[1] + ("_" + tsk[2]) * (tsk[2] != "")): listoftaskswcreatedfolder.append(tsk)

    return listoftaskswcreatedfolder


def KillAndErase(tsk):
    print "### Task with folder", "crab_" + tsk[0] + '_' + tsk[1] + ("_" + tsk[2]) * (tsk[2] != "")
    print "# Killing..."
    os.system("crab kill -d ./{wa}/{fl}".format(wa = tsk[3], fl = "crab_" + tsk[0] + '_' + tsk[1] + ("_" + tsk[2]) * (tsk[2] != "")))
    print "# Erasing..."
    os.system("rm -rf ./{wa}/{fl}".format(wa = tsk[3], fl = "crab_" + tsk[0] + '_' + tsk[1] + ("_" + tsk[2]) * (tsk[2] != "")))
    return
