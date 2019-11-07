import sys, os
import subprocess as sp
from multiprocessing import Pool

agedornot = False

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
    'nu_pu300': '/Nu_E10-pythia8-gun/PhaseIITDRSpring19DR-PU300_106X_upgrade2023_realistic_v3_ext1-v2/GEN-SIM-DIGI-RAW',
}


dirscaffold = "crab_{suffix}"


def CheckCRABStatus(crabdirpath):
    print "> Checking status for CRAB directory path", crabdirpath + "..."
    statusoutput = sp.check_output("crab status -d {d}".format(d = crabdirpath), shell = True)
    serverstatus         = ""
    schedstatus          = ""

    nSubJobs             = 0
    nIdleSubJobs         = 0
    nRunningSubJobs      = 0
    nTransferringSubJobs = 0
    nFinishedSubJobs     = 0
    nFailedSubJobs       = 0

    for line in statusoutput.splitlines():
        if "Status on the CRAB server:" in line:
            serverstatus = line.replace("Status on the CRAB server:", "").replace(" ", "").replace("\t", "")
        if "Status on the scheduler:" in line:
            schedstatus  = line.replace("Status on the scheduler:", "").replace(" ", "").replace("\t", "")
        if "Jobs status" in line:
            nSubJobs = int(line.split("(")[-1][:-1].split("/")[-1])
        if "idle" in line and "Warning" not in line: nIdleSubJobs = int(line.split("(")[-1][:-1].split("/")[0])
        if "running" in line and "Warning" not in line: nRunningSubJobs = int(line.split("(")[-1][:-1].split("/")[0])
        if "transferring" in line and "Warning" not in line: nTransferringSubJobs = int(line.split("(")[-1][:-1].split("/")[0])
        if "finished" in line and "Warning" not in line: nFinishedSubJobs = int(line.split("(")[-1][:-1].split("/")[0])
        if "failed" in line and "Warning" not in line and "step" not in line: nFailedSubJobs = int(line.split("(")[-1][:-1].split("/")[0])


    #print "  - Job with server status:   ", serverstatus + "."
    #print "  - Job with scheduler status:", schedstatus + "."

    return (crabdirpath, serverstatus, schedstatus, "total:{tot}-idle:{idl}-running:{rn}-transferring:{trf}-finished:{fin}-failed:{fal}".format(tot = nSubJobs, idl = nIdleSubJobs, rn = nRunningSubJobs, trf = nTransferringSubJobs, fin = nFinishedSubJobs, fal = nFailedSubJobs))


def SendCRABJob(tsk):
    sample, cfg, scn, crabdirpath, outputdir = tsk
    from CRABAPI.RawCommand       import crabCommand
    from CRABClient.UserUtilities import config
    from multiprocessing          import Process

    print "# Sending CRAB job for sample", sample, ", configuration", cfg, "and ageing scenario", scn

    config = config()

    def submit(config):
        res = crabCommand('submit', config = config )

    config.General.workArea     = crabdirpath.split("/")[0]
    config.General.transferLogs = True

    config.JobType.pluginName  = 'Analysis'
    config.JobType.psetName    = 'dtDpgNtuples_phase2_cfg.py'
    if scn != "": config.JobType.inputFiles  = [ageing_scenarios[scn][0].replace("ageingInput=sqlite_file:", "")]
    config.JobType.pyCfgParams = running_options[cfg] + ageing_scenarios[scn]

    config.JobType.maxMemoryMB = 2500

    config.Data.inputDBS    = 'global'
    config.Data.splitting   = 'FileBased'
    config.Data.unitsPerJob = 1
    config.Data.publication = False
    config.Data.allowNonValidInputDataset = True

    config.Data.outLFNDirBase = outputdir

    config.Site.storageSite = 'T2_ES_IFCA'
    #config.Site.storageSite = 'T2_CH_CERN'
    config.Site.blacklist   = ['T2_BR_SPRACE', 'T2_US_Wisconsin', 'T1_RU_JINR', 'T2_RU_JINR', 'T2_EE_Estonia']

    config.General.requestName   = sample + '_' + cfg + ("_" + scn) * (scn != "")
    config.Data.inputDataset     = dataset[sample]
    config.Data.outputDatasetTag = sample + '_' + cfg + ("_" + scn) * (scn != "")

    p = Process(target=submit, args=(config,))
    p.start()
    p.join()
    return


def RelaunchCRABJob(crabdirpath):
    options  = crabdirpath.split("/")[-1].replace("crab_", "")

    sample   = options.split("_")[0] if "nu_" not in options else "_".join(options.split("_")[:2])
    ageing   = options.split("_")[1] if "nu_" not in options else options.split("_")[2]
    rpcuse   = options.split("_")[2] if "nu_" not in options else options.split("_")[3]
    scenario = ""
    outdir   = ""
    if "noage" not in ageing: scenario = "_".join(options.split("_")[3:]) if "nu_" not in options else "_".join(options.split("_")[4:])

    useyoungseg = False
    if "youngseg" in scenario:
        useyoungseg = True
        scenario = scenario.replace("youngseg_", "")


    print "\n# Job for the sample", sample, "with ageing", ageing, "with rpc use", rpcuse, "and ageing scenario", scenario, "and with young segments (not aged)" if useyoungseg else "and with aged segments."

    if (agedornot and ("noage" in ageing)) or ((not agedornot) and ("noage" not in ageing)):
        print "# This script is not set to relaunch aged/unaged samples. Please, change the configuration at its beginning."
        return

    print "# Importing CRAB output directory..."
    logfile = open(crabdirpath + "/crab.log", "r")

    for line in logfile.readlines():
        if "config.Data.outLFNDirBase" in line:
            outdir = line.replace("config.Data.outLFNDirBase", "").replace(" ", "").replace("=", "").replace("'", "").replace('"', "").replace("\n", "")
            break
    if outdir == "": raise RuntimeError("FATAL: no CRAB output directory could be obtained from crab log.")
    logfile.close()

    print "# CRAB output directory is", outdir
    print "# Erasing CRAB workarea..."
    os.system("rm -rf " + crabdirpath)

    print "# Relaunching job..."
    SendCRABJob( (sample, ageing + "_" + rpcuse + "_youngseg" * useyoungseg, scenario, crabdirpath, outdir) )
    return


def ResubmitCRABJob(crabdirpath):
    print "> Resubmitting CRAB job with directory path", crabdirpath + "..."
    os.system("crab resubmit -d {d}".format(d = crabdirpath))

    return



def GetSubJobsFromJob(inputstring):
    nidle = 0; nrun = 0; ntransf = 0; nfin = 0; nfail = 0; ntot = 0

    tmplist = inputstring.split("-")
    for el in tmplist:
        if   "idle"         in el: nidle   = int(el.split(":")[1])
        elif "running"      in el: nrun    = int(el.split(":")[1])
        elif "transferring" in el: ntransf = int(el.split(":")[1])
        elif "finished"     in el: nfin    = int(el.split(":")[1])
        elif "failed"       in el: nfail   = int(el.split(":")[1])
        elif "total"        in el: ntot    = int(el.split(":")[1])

    return (nidle, nrun, ntransf, nfin, nfail, ntot)



def confirm():
    """
    Ask user to enter Y or N (case-insensitive).
    :return: True if the answer is Y.
    :rtype: bool
    """
    answer = ""
    while answer not in ["y", "n"]:
        answer = raw_input("Do you wish to continue? [Y/N]\n").lower()
    return answer == "y"


if __name__ == '__main__':
    if len(sys.argv) == 1: raise RuntimeError("FATAL: no folder given to check.")

    basedir = sys.argv[1]
    if basedir[-1] == "/": basedir = basedir[:-1]

    print "\n> We are going to check the folder", basedir, "to see if there are CRAB jobs that failed on submission."
    print "    - We will look for all folders with scaffold", dirscaffold.format(suffix = "*")
    print "\n----> REMEMBER TO SET CRAB PROPERLY!!! <----"

    listofsubdirs      = os.listdir(basedir)
    listofcrabdirpaths = [basedir + "/" + subdir for subdir in listofsubdirs]

    statuslist = []

    if len(sys.argv) >= 3:
        ncores = int(sys.argv[2])
        print "\n> Parallelising with", ncores, "cores."
        pool = Pool(ncores)
        statuslist = pool.map(CheckCRABStatus, listofcrabdirpaths)
        pool.close()
        pool.join()
        del pool
    else:
        for crabdirpath in listofcrabdirpaths:
            statuslist.append(CheckCRABStatus(crabdirpath))

    print "\n> Reviewing job' status..."
    totaljobs       = float(len(statuslist))
    relaunchinglist = []
    submittedlist   = []
    completedlist   = []
    onlytransflist  = []
    withfailedlist  = []
    notfinnotfaillist = []
    fullyidlelist   = []
    nSubJobsDict    = {}

    nidletotal = 0.; nruntotal = 0.; ntransftotal = 0.; nfintotal = 0.; nfailtotal = 0.; ntotalsubjobs = 0

    for job in statuslist:
        nidle, nrun, ntransf, nfin, nfail, ntot = GetSubJobsFromJob(job[3])
        nidletotal += nidle; nruntotal += nrun; nfintotal += nfin; nfailtotal += nfail; ntotalsubjobs += ntot
        nSubJobsDict[job[0]] = {
            "nidle"   : nidle,
            "nrun"    : nrun,
            "ntransf" : ntransf,
            "nfin"    : nfin,
            "nfail"   : nfail,
            "ntot"    : ntot
        }
        if job[1] == "SUBMITFAILED":
            crabdir = job[0].split("/")[-1]
            print "# Job of CRAB directory", crabdir, "with SUBMITFAILED server status: adding to relaunching list."
            relaunchinglist.append(job[0])
        if job[1] == "SUBMITTED":
            submittedlist.append(job[0])
            if   job[2] != "COMPLETED" and job[2] != "FAILED" and (nrun != 0 or ntransf != 0):
                notfinnotfaillist.append(job[0])
            elif job[2] != "COMPLETED" and job[2] != "FAILED":
                fullyidlelist.append(job[0])


        if job[2] == "COMPLETED":
            completedlist.append(job[0])

        if nidle == 0 and nrun == 0 and ntransf != 0 and nfail == 0: onlytransflist.append(job[0])
        if nfail != 0: withfailedlist.append(job[0])


    nnotfinishedsubjobs = nidletotal + nruntotal + nfailtotal

    print "\n========== GLOBAL CRAB REPORT =========="
    print "# Total jobs:                          ", int(totaljobs)
    print "# Submitted jobs:                      ", str(len(submittedlist)) + "/" + str(int(totaljobs)),   "(%3.1f "%(len(submittedlist)/totaljobs * 100) + "%)"
    print "# Unsubmitted jobs tagged for relaunch:", str(len(relaunchinglist)) + "/" + str(int(totaljobs)), "(%3.1f "%(len(relaunchinglist)/totaljobs * 100) + "%)"
    print "# Transferring (only) jobs:            ", str(len(onlytransflist)) + "/" + str(int(totaljobs)),  "(%3.1f "%(len(onlytransflist)/totaljobs * 100) + "%)"
    print "# With failed subjobs jobs:            ", str(len(withfailedlist)) + "/" + str(int(totaljobs)),  "(%3.1f "%(len(withfailedlist)/totaljobs * 100) + "%)"
    print "# In normal execution jobs:            ", str(len(notfinnotfaillist)) + "/" + str(int(totaljobs)),  "(%3.1f "%(len(notfinnotfaillist)/totaljobs * 100) + "%)"
    print "# Jobs submitted, but completely idle: ", str(len(fullyidlelist)) + "/" + str(int(totaljobs)),  "(%3.1f "%(len(fullyidlelist)/totaljobs * 100) + "%)"
    print "# Completed jobs:                      ", str(len(completedlist)) + "/" + str(int(totaljobs)),   "(%3.1f "%(len(completedlist)/totaljobs * 100) + "%)"
    print ""
    print "# Total subjobs:        ", int(ntotalsubjobs)
    print "# Idle subjobs:         ", str(int(nidletotal)) + "/" + str(int(ntotalsubjobs)), "(%3.1f "%(nidletotal/ntotalsubjobs * 100) + "% of total" + (nnotfinishedsubjobs != 0) * (", %3.1f "%(nidletotal/nnotfinishedsubjobs * 100) + "% of not completed nor transferring") + ")"
    print "# Running subjobs:      ", str(int(nruntotal)) + "/" + str(int(ntotalsubjobs)), "(%3.1f "%(nruntotal/ntotalsubjobs * 100) + "% of total" + (nnotfinishedsubjobs != 0) * (", %3.1f "%(nruntotal/nnotfinishedsubjobs * 100) + "% of not completed nor transferring") + ")"
    print "# Transferring subjobs: ", str(int(ntransftotal)) + "/" + str(int(ntotalsubjobs)), "(%3.1f "%(ntransftotal/ntotalsubjobs * 100) + "%)"
    print "# Finished subjobs:     ", str(int(nfintotal)) + "/" + str(int(ntotalsubjobs)), "(%3.1f "%(nfintotal/ntotalsubjobs * 100) + "%)"
    print "# Failed subjobs:       ", str(int(nfailtotal)) + "/" + str(int(ntotalsubjobs)), "(%3.1f "%(nfailtotal/ntotalsubjobs * 100) + "%)"

    print "\n========== DETAILED REPORT =========="
    print "> Jobs not even submitted:"
    if len(relaunchinglist) == 0: print "# There is not any CRAB job that was not submitted!"
    else:
        print "### There are", len(relaunchinglist), "CRAB jobs that were not submitted."
        for job in relaunchinglist: print "#", job

    print "\n> Jobs submitted, but completely idle:"
    if len(fullyidlelist) == 0: print "# There is not any CRAB job in such situation!"
    else:
        print "### There are", len(fullyidlelist), "CRAB jobs in such situation."
        for job in fullyidlelist: print "#", job

    print "\n> Jobs in normal execution:"
    if len(notfinnotfaillist) == 0: print "# There is not any CRAB job in normal execution!"
    else:
        print "### There are", len(notfinnotfaillist), "CRAB jobs in normal execution."
        for job in notfinnotfaillist: print "#", job

    print "\n> Jobs with only transferring subjobs:"
    if len(onlytransflist) == 0: print "# There is not any CRAB job with only transferring subjobs!"
    else:
        print "### There are", len(onlytransflist), "CRAB jobs with only transferring subjobs."
        for job in onlytransflist:
            print "### Job", job
            print "# Transferring subjobs:", str(nSubJobsDict[job]["ntransf"]) + "/" + str(nSubJobsDict[job]["ntot"]), "(%3.1f "%(nSubJobsDict[job]["ntransf"]/float(nSubJobsDict[job]["ntot"]) * 100) + "%)"

    print "\n> Jobs with failed subjobs:"
    if len(withfailedlist) == 0: print "# There is not any CRAB job with failed subjobs!"
    else:
        print "### There are", len(withfailedlist), "CRAB jobs with failed subjobs."
        for job in withfailedlist:
            print "### Job", job
            print "# Idle subjobs:        ", str(nSubJobsDict[job]["nidle"]) + "/" + str(nSubJobsDict[job]["ntot"]), "(%3.1f "%(nSubJobsDict[job]["nidle"]/float(nSubJobsDict[job]["ntot"]) * 100) + "%)"
            print "# Running subjobs:     ", str(nSubJobsDict[job]["nrun"]) + "/" + str(nSubJobsDict[job]["ntot"]), "(%3.1f "%(nSubJobsDict[job]["nrun"]/float(nSubJobsDict[job]["ntot"]) * 100) + "%)"
            print "# Transferring subjobs:", str(nSubJobsDict[job]["ntransf"]) + "/" + str(nSubJobsDict[job]["ntot"]), "(%3.1f "%(nSubJobsDict[job]["ntransf"]/float(nSubJobsDict[job]["ntot"]) * 100) + "%)"
            print "# Finished subjobs:    ", str(nSubJobsDict[job]["nfin"]) + "/" + str(nSubJobsDict[job]["ntot"]), "(%3.1f "%(nSubJobsDict[job]["nfin"]/float(nSubJobsDict[job]["ntot"]) * 100) + "%)"
            print "# Failed subjobs:      ", str(nSubJobsDict[job]["nfail"]) + "/" + str(nSubJobsDict[job]["ntot"]), "(%3.1f "%(nSubJobsDict[job]["nfail"]/float(nSubJobsDict[job]["ntot"]) * 100) + "%)\n"

    if len(relaunchinglist) == 0 and len(withfailedlist) == 0:
        print "\n> No jobs marked for relaunching nor resubmitting. Exitting."
        sys.exit()

    print "\nThere are a total of", len(relaunchinglist), "jobs marked for relaunching and", len(withfailedlist), "jobs marked for resubmitting.\n"
    if not confirm(): sys.exit()

    if len(relaunchinglist) != 0:
        print "\n>  Initiating relaunch..."
        for job in relaunchinglist: RelaunchCRABJob(job)
        print "\n> All jobs relaunched."

    if len(withfailedlist) != 0:
        print "\n> Initiating resubmit..."

        if len(sys.argv) >= 3:
            pool = Pool(ncores)
            pool.map(ResubmitCRABJob, withfailedlist)
            pool.close()
            pool.join()
            del pool
        else:
            for job in withfailedlist: ResubmitCRABJob(job)
        print "> All jobs resubmitted."
