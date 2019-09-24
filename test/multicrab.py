name      = 'DT_TDR_sep24_HBageingfixed'  #Part of the name of your output directory, adapt as needed.
steam_dir = 'Summer16_FlatPU28to62/'  #Part of the name of your output directory, adapt as needed. 
running_options = {
   'noage_norpc'            : ['useRPC=0'],
   'age_norpc'              : ['applyTriggerAgeing=True', 'applySegmentAgeing=True', 'ageingInput=sqlite_file:MuonSystemAging.db','useRPC=0'],
   'age_norpc_youngseg'     : ['applyTriggerAgeing=True', 'ageingInput=sqlite_file:MuonSystemAging.db','useRPC=0'],
   'noage_withrpc'          : ['useRPC=1'],
   'age_withrpc'            : ['applyTriggerAgeing=True', 'applySegmentAgeing=True', 'ageingInput=sqlite_file:MuonSystemAging.db','useRPC=1'],
   'age_withrpc_youngseg'   : ['applyTriggerAgeing=True', 'ageingInput=sqlite_file:MuonSystemAging.db','useRPC=1'],
}
runATCAF = False

dataset = {
   "nopu"  : "/Mu_FlatPt2to100-pythia8-gun/PhaseIITDRSpring19DR-NoPU_106X_upgrade2023_realistic_v3-v1/GEN-SIM-DIGI-RAW",
   "pu200" : "/Mu_FlatPt2to100-pythia8-gun/PhaseIITDRSpring19DR-PU200_106X_upgrade2023_realistic_v3-v2/GEN-SIM-DIGI-RAW",
}

listOfOptions = [
  #'noage_norpc'   ,
#   'noage_withrpc' ,
  #'age_norpc'     ,
#   'age_withrpc'   ,
  'age_norpc_youngseg',
  'age_withrpc_youngseg',
]

listOfSamples = [
"nopu",
"pu200",
]

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
   config.JobType.inputFiles  = ['MuonSystemAging.db']
   #config.JobType.allowUndistributedCMSSW = True

   config.Data.inputDBS    = 'global'
   config.Data.splitting   = 'FileBased'
   config.Data.publication = True
   config.Data.unitsPerJob = 1
   #config.Data.outLFNDirBase = '/store/user/sesanche/DT_L1_TDR_12_09_19'
   #config.Data.outLFNDirBase = '/store/user/rodrigvi/'
   config.Data.outLFNDirBase = '/store/group/phys_muon/rodrigvi/'

   #config.Site.storageSite = 'T2_ES_IFCA'
   config.Site.storageSite = 'T2_CH_CERN'
   config.Site.blacklist   = ['T2_BR_SPRACE', 'T2_US_Wisconsin', 'T1_RU_JINR', 'T2_RU_JINR', 'T2_EE_Estonia']
   if runATCAF :
      config.Site.whitelist = ['T3_CH_CERN_CAF']
      config.Site.ignoreGlobalBlacklist = True
      config.Data.ignoreLocality = True

   listOfSamples.reverse()
   for sample in listOfSamples:
      for cfg in listOfOptions:
         config.General.requestName = sample + '_' + cfg
         config.Data.inputDataset = dataset[sample]
         config.Data.outputDatasetTag = sample + '_' + cfg
         config.JobType.pyCfgParams = running_options[cfg]
         p = Process(target=submit, args=(config,))
         p.start()
         p.join()

