### General settings
UnretrieveThreshold = 7

### Directories with settings
running_options = {
    'noage_norpc'          : ['useRPC=0'],
    'age_norpc'            : ['applyTriggerAgeing=True', 'applySegmentAgeing=True', 'useRPC=0'],
    'age_norpc_youngseg'   : ['applyTriggerAgeing=True', 'useRPC=0'], # Ageing in trigger, but not in reco segments
    'noage_withrpc'        : ['useRPC=1'],
    'age_withrpc'          : ['applyTriggerAgeing=True', 'applySegmentAgeing=True', 'useRPC=1'],
    'age_withrpc_youngseg' : ['applyTriggerAgeing=True', 'useRPC=1'], # Ageing in trigger, but not in reco segments
}

ageing_scenarios = {
    'muonage_norpcage_nofail_3000_OLD': ['ageingInput=sqlite_file:MuonAgeingNotFailures_3000fbm1_OLDSCENARIO.db', "ageingTag=MuonSystemAging_3000fbm1"],
    'muonage_norpcage_nofail_3000'    : ['ageingInput=sqlite_file:MuonAgeingAndFailures_3000fbm1_DT_L1TTDR_v1_mc.db', "ageingTag=MuonAgeingAndFailures_3000fbm1_DT_L1TTDR"],
    'muonage_norpcage_fail_3000'      : ['ageingInput=sqlite_file:MuonAgeingAndFailures_3000fbm1_DT-RPC_L1TTDR_v1_mc.db', "ageingTag=MuonAgeingAndFailures_3000fbm1_DT-RPC_L1TTDR", "applyRpcAgeing=True"],
    'muonage_norpcage_nofail_1000'    : ['ageingInput=sqlite_file:MuonAgeingAndFailures_1000fbm1_DT_L1TTDR_v1_mc.db', "ageingTag=MuonAgeingAndFailures_1000fbm1_DT_L1TTDR"],
    'muonage_norpcage_fail_1000'      : ['ageingInput=sqlite_file:MuonAgeingAndFailures_1000fbm1_DT-RPC_L1TTDR_v1_mc.db', "ageingTag=MuonAgeingAndFailures_1000fbm1_DT-RPC_L1TTDR", "applyRpcAgeing=True"],
    "" : [],
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
def LaunchCRABTask(tsk):
    sample, cfg, scn, workarea, outputdir = tsk
    from CRABAPI.RawCommand       import crabCommand
    from CRABClient.UserUtilities import config

    print "# Launching CRAB task for sample {s}, config. {c} and ageing scenario {sc}.".format(s = sample, c = cfg, sc = scn)
    config = config()

    config.General.workArea     = workarea
    config.General.transferLogs = True

    config.JobType.pluginName  = 'Analysis'
    config.JobType.psetName    = 'dtDpgNtuples_phase2_cfg.py'
    if scn != "": config.JobType.inputFiles  = [ageing_scenarios[scn][0].replace("ageingInput=sqlite_file:", "")]
    config.JobType.pyCfgParams = running_options[cfg] + ageing_scenarios[scn]

    config.JobType.maxMemoryMB = 2500

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

    res = crabCommand('submit', config = config)
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
