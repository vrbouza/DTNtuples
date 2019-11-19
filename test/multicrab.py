import sys
import CentralSettings as cs
from multiprocessing import Pool

### Settings of the launch procedure: THEY ARE EXPECTED TO BE CHANGED DEPENDING ON THE EXECUTION

# This will be used to create the CRAB workarea, as well as the output folder
name = '2019_11_19_PruebaParalelizacion'

# The name will be append to the following path to set the output directory
outputdir = '/store/user/rodrigvi/'
#outputdir = '/store/user/sesanche/DT_L1_TDR_12_09_19'
#outputdir = '/store/user/rodrigvi/'
#outputdir = '/store/group/phys_muon/rodrigvi/'

listOfSamples = [
    "nopu",     # 0   PU central muon     gun sample
    "pu200",    # 200 PU central muon     gun sample
    #"nu_pu140", # 140 PU central neutrino gun sample
    #"nu_pu200", # 200 PU central neutrino gun sample
    #"nu_pu250", # 250 PU central neutrino gun sample
    #"nu_pu300", ### NOT FINISHED SAMPLE
]

listOfOptions = [
    'noage_norpc',          # Non-aged TP, with non-aged reco. segments, and with the AM not using RPC
    #'noage_withrpc',        # Non-aged TP, with non-aged reco. segments, and with the AM using RPC
    #'age_norpc',            # Aged TP,     with aged reco. segments,     and with the AM not using RPC
    #'age_withrpc',          # Aged TP,     with aged reco. segments,     and with the AM using RPC
    #'age_norpc_youngseg',   # Aged TP,     with non-aged reco. segments, and with the AM not using RPC
    #'age_withrpc_youngseg', # Aged TP,     with non-aged reco. segments, and with the AM using RPC
]

listOfScenarios = [
    'muonage_norpcage_nofail_3000_OLD', # DT ageing, without RPC failures, old 3000fb-1
    'muonage_norpcage_nofail_3000',     # DT ageing, without RPC failures, 3000fb-1
    'muonage_norpcage_fail_3000',       # DT ageing, with    RPC failures, 3000fb-1
    'muonage_norpcage_nofail_1000',     # DT ageing, without RPC failures, 1000fb-1
    'muonage_norpcage_fail_1000',       # DT ageing, with    RPC failures, 1000fb-1
]


if __name__ == '__main__':
    # Preventive errors.
    if len(listOfSamples) == 0: raise RuntimeError("FATAL: no samples chosen.")
    else:
        if len(listOfOptions) == 0: raise RuntimeError("FATAL: no settings for the execution chosen.")
        else:
            onlyaged = True
            for setting in listOfOptions:
                if "noage" in setting: onlyaged = False
            if onlyaged and len(listOfScenarios) == 0: raise RuntimeError("FATAL: only aged settings chosen, but no scenario available.")

    # Creating task list
    tasks = []
    for sample in listOfSamples:
        for cfg in listOfOptions:
            if "noage" in cfg: tasks.append( (sample, cfg, "", 'analysis_' + name, outputdir + "/" + name + "/"))
            else:
                for scn in listOfScenarios: tasks.append( (sample, cfg, scn, 'analysis_' + name, outputdir + "/" + name + "/"))

    print "\n> We are going to launch the following {n} CRAB tasks in the workarea {w} that will drop their output in the folder {o}.".format(n = len(tasks), w = 'analysis_' + name, o = outputdir + "/" + name + "/")
    for tsk in tasks: print "# Sample {s} with config. {c} and ageing scenario {sc}.".format(s = tsk[0], c = tsk[1], sc = tsk[2])
    print ""
    if not cs.confirm():
        print ""
        sys.exit()

    if len(sys.argv) > 1:
        ncores = int(sys.argv[1])
        print "\n> Parallelisation of CRAB task launching with", ncores
        pool = Pool(ncores)
        pool.map(cs.LaunchCRABTask, tasks)
        pool.close()
        pool.join()
        del pool
    else:
        for tsk in tasks: cs.LaunchCRABTask(tsk)
