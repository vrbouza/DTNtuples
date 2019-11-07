import sys
from multiprocessing import Pool

name      = '2019_11_06_NeutrinoProduction'  #Part of the name of your output directory, adapt as needed.
#name      = '2019_11_05_HBproduccion'  #Part of the name of your output directory, adapt as needed.

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
    'muonage_norpcage_fail_3000'      : ['ageingInput=sqlite_file:MuonAgeingAndFailures_3000fbm1_DT_L1TTDR_v1_mc.db', "ageingTag=MuonAgeingAndFailures_3000fbm1_DT_L1TTDR"],
    'muonage_norpcage_nofail_3000'    : ['ageingInput=sqlite_file:MuonAgeingAndFailures_3000fbm1_DT-RPC_L1TTDR_v1_mc.db', "ageingTag=MuonAgeingAndFailures_3000fbm1_DT-RPC_L1TTDR", "applyRpcAgeing=True"],
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
    #'nu_pu300': '/Nu_E10-pythia8-gun/PhaseIITDRSpring19DR-PU300_106X_upgrade2023_realistic_v3_ext1-v2/GEN-SIM-DIGI-RAW',
}

listOfOptions = [
    'noage_norpc',
    #'noage_withrpc' ,
    #'age_norpc',
    #'age_withrpc'   ,
    #'age_norpc_youngseg',
    #'age_withrpc_youngseg',
]


listOfSamples = [
    #"nopu",
    #"pu200",
    #"nu_pu140",
    "nu_pu200",
    #"nu_pu250",
    #"nu_pu300",
]


listOfScenarios = [
    'muonage_norpcage_nofail_3000_OLD',
    'muonage_norpcage_nofail_3000',
    'muonage_norpcage_fail_3000',
    'muonage_norpcage_nofail_1000',
    'muonage_norpcage_fail_1000',
]


#def SendCrabJob(tsk):
    #sample, cfg, scn = tsk
    #from CRABAPI.RawCommand       import crabCommand
    #from CRABClient.UserUtilities import config
    #print "\n> Sending CRAB job for sample", sample, ", configuration", cfg, "and ageing scenario", scn
    #config = config()
    #print "wololo"
    #config.General.workArea     = 'analysis_' + name
    #config.General.transferLogs = True

    #config.JobType.pluginName  = 'Analysis'
    #config.JobType.psetName    = 'dtDpgNtuples_phase2_cfg.py'
    #if scn != "": config.JobType.inputFiles  = [ageing_scenarios[scn][0].replace("ageingInput=sqlite_file:", "")]
    #config.JobType.pyCfgParams = running_options[cfg] + ageing_scenarios[scn]

    #config.JobType.maxMemoryMB = 3000
    ##config.JobType.allowUndistributedCMSSW = True

    #config.Data.inputDBS    = 'global'
    #config.Data.splitting   = 'FileBased'
    #config.Data.unitsPerJob = 1
    ##config.Data.splitting   = 'Automatic'
    #config.Data.publication = False
    #config.Data.allowNonValidInputDataset = True

    ##config.Data.outLFNDirBase = '/store/user/sesanche/DT_L1_TDR_12_09_19'
    #config.Data.outLFNDirBase = '/store/user/rodrigvi/Producciones_2019-10-31/'
    ##config.Data.outLFNDirBase = '/store/group/phys_muon/rodrigvi/'

    #config.Site.storageSite = 'T2_ES_IFCA'
    ##config.Site.storageSite = 'T2_CH_CERN'
    #config.Site.blacklist   = ['T2_BR_SPRACE', 'T2_US_Wisconsin', 'T1_RU_JINR', 'T2_RU_JINR', 'T2_EE_Estonia']

    #config.General.requestName   = sample + '_' + cfg + "_" + scn + "LOSBUENOS"
    #config.Data.inputDataset     = dataset[sample]
    #config.Data.outputDatasetTag = sample + '_' + cfg + "_" + scn + "LOSBUENOS"

    #res = crabCommand('submit', config = config)
    #return



if __name__ == '__main__':
    from CRABClient.UserUtilities import config
    config = config()

    from CRABAPI.RawCommand import crabCommand
    from multiprocessing import Process

    def submit(config):
        res = crabCommand('submit', config = config )

    config.General.workArea     = 'analysis_' + name
    config.General.transferLogs = True

    config.JobType.pluginName = 'Analysis'
    config.JobType.psetName   = 'dtDpgNtuples_phase2_cfg.py'

    config.JobType.maxMemoryMB = 2500
    #config.JobType.allowUndistributedCMSSW = True

    config.Data.inputDBS    = 'global'
    config.Data.splitting   = 'FileBased'
    config.Data.unitsPerJob = 1
    #config.Data.splitting   = 'Automatic'
    config.Data.publication = False
    #config.Data.outLFNDirBase = '/store/user/sesanche/DT_L1_TDR_12_09_19'
    config.Data.outLFNDirBase = '/store/user/rodrigvi/2019_11_06_NeutrinoProduction/'
    #config.Data.outLFNDirBase = '/store/user/rodrigvi/2019_11_05_HBproduccion/'
    #config.Data.outLFNDirBase = '/store/group/phys_muon/rodrigvi/'
    config.Data.allowNonValidInputDataset = True

    config.Site.storageSite = 'T2_ES_IFCA'
    #config.Site.storageSite = 'T2_CH_CERN'
    config.Site.blacklist   = ['T2_BR_SPRACE', 'T2_US_Wisconsin', 'T1_RU_JINR', 'T2_RU_JINR', 'T2_EE_Estonia']

    listOfSamples.reverse()
    for sample in listOfSamples:
        for cfg in listOfOptions:
            if "noage" in cfg:
                print "\n> Sending CRAB jobs for request", sample + '_' + cfg
                config.General.requestName   = sample + '_' + cfg
                config.Data.inputDataset     = dataset[sample]
                config.Data.outputDatasetTag = sample + '_' + cfg
                config.JobType.pyCfgParams   = running_options[cfg]
                p = Process(target=submit, args=(config,))
                p.start()
                p.join()
            else:
                for scn in listOfScenarios:
                    print "\n> Sending CRAB jobs for request", sample + '_' + cfg + "_" + scn
                    config.JobType.inputFiles    = [ageing_scenarios[scn][0].replace("ageingInput=sqlite_file:", "")]
                    config.General.requestName   = sample + '_' + cfg + "_" + scn
                    config.Data.inputDataset     = dataset[sample]
                    config.Data.outputDatasetTag = sample + '_' + cfg + "_" + scn
                    config.JobType.pyCfgParams   = running_options[cfg] + ageing_scenarios[scn]
                    p = Process(target=submit, args=(config,))
                    p.start()
                    p.join()

    #tasks = []

    #for sample in listOfSamples:
        #for cfg in listOfOptions:
            #if "noage" in cfg: tasks.append( (sample, cfg, "") )
            #else:
                #for scn in listOfScenarios: tasks.append( (sample, cfg, scn) )

    #if len(sys.argv) > 1:
        #ncores = int(sys.argv[1])
        #print "\n> Parallelisation of CRAB job sending with", ncores
        #pool = Pool(ncores)
        #pool.map(SendCrabJob, tasks)
        #pool.close()
        #pool.join()
        #del pool
    #else:
        #for tsk in tasks: SendCrabJob(tsk)
