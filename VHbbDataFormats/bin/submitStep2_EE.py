#!/usr/bin/env python

#############
# run at /VHbbAnalysis/VHbbDataFormats/bin
#############

import commands
import re
import os
import string
import FWCore.ParameterSet.Config as cms
import math

import sys
sys.path.append('./')

print "Import cfg file from ntuple.py"
from ntuple  import process 

debug    = False
doAllHad = False

#outdir = './Ntuples_allHadTrig'
outdir = './Ntuples_all'
print "Saving output to " + outdir

def processAllBatch(jobName, isPisa, outName, split, doAllHad=False): #isPisa is a placeholder

    process.fwliteInput.fileNames = ()
    process.fwliteInput.doAllHad = cms.bool(doAllHad)

    if string.find( jobName, 'Run2012' )>0:
        process.Analyzer.isMC   = cms.bool(False)
    
    input = open('filelists/filelist_'+jobName+'.txt','r')
    counter     = 1
    counterJobs = 0
    for line in input:
        foo = line.strip('\n')
        if counter>=split[0] and counter<=split[1]:
            process.fwliteInput.fileNames.append(foo)
            counterJobs += 1
        counter += 1

    input.close()

    outFileName = outName+'_'+str(split[0])+'-'+str(split[1])+'.root'
    
    process.fwliteOutput.fileName = cms.string(outdir+'/'+outFileName)

    out = open('myStep2_'+jobName+'_'+str(split[0])+'-'+str(split[1])+'.py','w')
    out.write(process.dumpPython())
    out.close()

    scriptName = 'myStep2_'+jobName+'_'+str(split[0])+'-'+str(split[1])+'.sh'
    
    f = open(scriptName,'w')
    f.write('#!/bin/bash\n\n')
    f.write('/bin/hostname \n\n')
    f.write('cd /home/liis/TTH_Ntuples/CMSSW_5_3_3/src/VHbbAnalysis/VHbbDataFormats/bin/\n')#/shome/liis/CMSSW_5_3_3_patch2_New/src/VHbbAnalysis/VHbbDataFormats/bin\n')
    f.write('export SCRAM_ARCH="slc5_amd64_gcc462"\n')
    f.write('source $VO_CMS_SW_DIR/cmsset_default.sh\n')
    f.write('eval `scramv1 runtime -sh`\n')
    f.write('\n')
    f.write('\n')

    mainexec = 'Ntupler myStep2_'+jobName+'_'+str(split[0])+'-'+str(split[1])+'.py'
    print mainexec
    f.write(mainexec+'\n\n')           

#    f.write("srmcp " + outdir + "/" + outFileName + "srm://ganymede.hep.kbfi.ee:8888/srm/v2/server?SFN=/hdfs/cms/store/user/liis/TTH_Ntuples_v3/ \n")
#    f.write("rm " + outdir + "/" + outFileName + "\n" )
            
    f.close()

    os.system('chmod +x '+scriptName)
    submitToQueue = 'qsub -N my'+jobName+'_'+str(split[0])+'-'+str(split[1])+' '+scriptName 

    if not debug:
        os.system(submitToQueue)
        print submitToQueue


    return float(counterJobs)/float(counter-1)

###########################################################################
###########################################################################


files_per_job = 10
#infile_path = "/hdfs/cms/store/user/liis/VHbb_patTuples/"

print "Processing data-samples..."
data_samples = {      # dataset_name: nr_of_files
#    "SingleMuRun2012AAug06": 49,
#    "SingleMuRun2012AJul13": 391,
#    "SingleMuRun2012BJul13": 1576,
#    "SingleMuRun2012CAug24Rereco": 196,
#    "SingleMuRun2012C-EcalRecover_11Dec2012-v1_v2": 51,
 #   "SingleMuRun2012CPromptv2": 1681, 
#    "SingleMuRun2012CPromptV2TopUp": 577,
#    "SingleMuRun2012D-PromptReco-v1": 1441,

#    "SingleElectronRun2012AAug06EdmV42": 50,
#    "SingleElectronRun2012AJul13EdmV42b": 416,
#    "SingleElectronRun2012BJul13EdmV42": 1607,
#    "SingleElectronRun2012CAug24RerecoEdmV42": 199,
#    "SingleElectronRun2012C-EcalRecover_11Dec2012-v1_v2": 54,
#    "SingleElectronRun2012CPromptv2EdmV42": 1745,
#    "SingleElectronRun2012CPromptV2TopUpEdmV42": 594, #592
#    "SingleElectronRun2012D-PromptReco-v1_v3": 3273,

#    "DoubleElectron_Run2012A-recover-06Aug2012-v1_ProcV2": 28,
#    "DoubleElectron_Run2012A-13Jul2012-v1_ProcFIXED": 182,
#    "DoubleElectron_Run2012A-13Jul2012-v1_ProcV2": 184,
#    "DoubleElectron_Run2012B-13Jul2012-v1_ProcFIXED": 475,
#    "DoubleElectron_Run2012B-13Jul2012-v1_ProcV2": 479,
#    "DoubleElectronRun2012CAug24RerecoEdmV42": 140,
#    "DoubleElectronRun2012C-EcalRecover_11Dec2012-v1_v2": 40,
#    "DoubleElectron_Run2012C-PromptReco-v2_HBB_EDMNtupleV42_ProcV1": 330,    
#    "DoubleElectron_Run2012C-PromptReco-v2_HBB_EDMNtupleV42_ProcV2": 87, 
#    "DoubleElectronRun2012D": 1867,
    }

for data_sample in data_samples:
    nr_input_files = data_samples[data_sample]
    nr_jobs = int(math.ceil(float(nr_input_files)/files_per_job))
    print "Submitting " + data_sample + " with " + str(nr_jobs) + " jobs"

    total = 0
    for k in range(nr_jobs):
        print "Processing job nr. ", k
        total += processAllBatch(data_sample, 1, data_sample, [k*files_per_job+1,(k+1)*files_per_job], doAllHad=doAllHad)
    print '**************************************\nFraction of processed sample: %s\n**************************************\n' % total

mc_samples = {
#    "DYJetsToLL_M-10To50_TuneZ2Star_8TeV-madgraph": 1663,
#    "TTH_HToBB_M-110_8TeV-pythia6": 35,
#    "TTH_HToBB_M-115_8TeV-pythia6": 17,
#    "TTH_HToBB_M-120_8TeV-pythia6": 25,
    "TTH_HToBB_M-125_8TeV-pythia6": 16,
#    "TTH_HToBB_M-130_8TeV-pythia6": 22,
#    "TTH_HToBB_M-135_8TeV-pythia6": 18,
#    "TTWJets_8TeV-madgraph": 8,
#    "TTZJets_8TeV-madgraph": 14,
  #  "DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph": 297,

 #   "WW_TuneZ2star_8TeV_pythia6_tauola": 668,
 #   "WZ_TuneZ2star_8TeV_pythia6_tauola": 670,
 #   "ZZ_TuneZ2star_8TeV_pythia6_tauola": 659,
#    "WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball": 133,

#    "T_s-channel_TuneZ2star_8TeV-powheg-tauola": 13,
#    "T_t-channel_TuneZ2star_8TeV-powheg-tauola": 34,
#    "T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola": 25,
#    "Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola": 7,
#    "Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola": 20,
#    "Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola": 27,

#    "TTJets_SemiLeptMGDecays_8TeV-madgraph": 1697,
#    "TTJets_FullLeptMGDecays_8TeV-madgraph": 782,
#    "TTJets_HadronicMGDecays_8TeV-madgraph": 922,    

#    "QCD_Pt-150_bEnriched_TuneZ2star_8TeV-pythia6": 17,
#    "QCD_Pt-30To50_bEnriched_TuneZ2star_8TeV-pythia6": 173,
#    "QCD_Pt-50To150_bEnriched_TuneZ2star_8TeV-pythia6": 107,

#    "QCD_Pt_80_170_BCtoE_TuneZ2star_8TeV_pythia6": 66,
#    "QCD_Pt_170_250_BCtoE_TuneZ2star_8TeV_pythia6": 68,
#    "QCD_Pt_250_350_BCtoE_TuneZ2star_8TeV_pythia6": 54,
#    "QCD_Pt_350_BCtoE_TuneZ2star_8TeV_pythia6": 62,
    }

for mc_sample in mc_samples:
    nr_input_files = mc_samples[mc_sample]
    nr_jobs = int(math.ceil(float(nr_input_files)/files_per_job))
#    jobname_mc = (mc_sample.split("DiJetPt_")[1]).split("_8TeV")[0]
    print "Submitting " + mc_sample + " with " + str(nr_jobs) + " jobs"

    total = 0
    for k in range(nr_jobs):
        print "Processing....", k
        total += processAllBatch(mc_sample, 1, mc_sample, [k*files_per_job  +1,(k+1)*files_per_job ])
        print '\n**************************************\nFraction of processed sample: %s\n**************************************' % total

