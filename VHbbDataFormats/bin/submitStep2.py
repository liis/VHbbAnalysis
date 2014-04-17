#!/usr/bin/env python
import commands
import re
import os
import string
import FWCore.ParameterSet.Config as cms

import sys
sys.path.append('./')

from ntuple  import process 

debug    = False

#indir = '/hdfs/cms/store/user/liis/VHbb_patTuples'
#outdir = '/hdfs/cms/store/user/liis/TTH_Ntuples_v3'
#outdir = '/scratch/liis/'
outdir = './Ntuples_new'

def processAllBatch(jobName, isPisa, outName, split):

    process.fwliteInput.fileNames = ()

    if string.find( jobName, 'Run2012' )>0:
        process.Analyzer.isMC  = cms.bool(False)
    
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


total = 0.
for k in range(8): 
    print "\nProcessing job....", k
    total += processAllBatch("T_t-channel", 1, "DiJetPt_T_t-channel_TuneZ2star_8TeV-powheg-tauola", [k*5+1, (k+1)*5 ])
print '\n**************************************\nFraction of processed sample: %s\n**************************************' % total
 
total = 0.
for k in range(70):
    print "\nProcessing....", k
#    total += processAllBatch("DYJets10to50", 0, "DiJetPt_DYJetsToLL_M-10To50_TuneZ2Star_8TeV-madgraph", [k*40+1,(k+1)*40])
print '\n**************************************\nFraction of processed sample: %s\n**************************************' % total

total = 0.
for k in range(297):
    print "\nProcessing....", k
    total += processAllBatch("DYJets50", 1, "DiJetPt_DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph", [k*1+1,(k+1)*1])
print '\n**************************************\nFraction of processed sample: %s\n**************************************' % total


total = 0.
for k in range(15):
    print "\nProcessing....", k
    total += processAllBatch("WJetsToLNu", 1, "DiJetPt_WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball", [k*10+1,(k+1)*10])
print '\n**************************************\nFraction of processed sample: %s\n**************************************' % total


total = 0.
for k in range(2):
    print "\nProcessing....", k
    total += processAllBatch("T_s-channel", 1, "DiJetPt_T_s-channel_TuneZ2star_8TeV-powheg-tauola", [k*10  +1,(k+1)*10 ])
print '\n**************************************\nFraction of processed sample: %s\n**************************************' % total


total = 0.
for k in range(4):
    print "\nProcessing....", k
    total += processAllBatch("T_t-channel", 1, "DiJetPt_T_t-channel_TuneZ2star_8TeV-powheg-tauola", [k*10  +1,(k+1)*10 ])
print '\n**************************************\nFraction of processed sample: %s\n**************************************' % total


total = 0.
for k in range(3):
    print "\nProcessing....", k
    total += processAllBatch("T_tW-channel-DR", 1, "DiJetPt_T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola", [k*10  +1,(k+1)*10 ])
print '\n**************************************\nFraction of processed sample: %s\n**************************************' % total


total = 0.
for k in range(2):
    print "\nProcessing....", k
    total += processAllBatch("Tbar_s-channel", 1, "DiJetPt_Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola", [k*10  +1,(k+1)*10 ])
print '\n**************************************\nFraction of processed sample: %s\n**************************************' % total


total = 0.
for k in range(4):
    print "\nProcessing....", k
    total += processAllBatch("Tbar_t-channel", 1, "DiJetPt_Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola", [k*10  +1,(k+1)*10 ])
print '\n**************************************\nFraction of processed sample: %s\n**************************************' % total


total = 0.
for k in range(3):
    print "\nProcessing....", k
    total += processAllBatch("Tbar_tW-channel-DR", 1, "DiJetPt_Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola", [k*10  +1,(k+1)*10 ])
print '\n**************************************\nFraction of processed sample: %s\n**************************************' % total




total = 0.
for k in range(14*5):
    print "Processing....", k
    total += processAllBatch("WW", 1, "DiJetPt_WW_TuneZ2star_8TeV_pythia6_tauola", [k*10  +1,(k+1)*10 ])
print '\n**************************************\nFraction of processed sample: %s\n**************************************' % total


total = 0.
for k in range(14*5):
    print "Processing....", k
    total += processAllBatch("WZ", 1, "DiJetPt_WZ_TuneZ2star_8TeV_pythia6_tauola", [k*10  +1,(k+1)*10 ])
print '\n**************************************\nFraction of processed sample: %s\n**************************************' % total


total = 0.
for k in range(14*5):
    print "Processing....", k
    total += processAllBatch("ZZ", 1, "DiJetPt_ZZ_TuneZ2star_8TeV_pythia6_tauola", [k*10  +1,(k+1)*10 ])
print '\n**************************************\nFraction of processed sample: %s\n**************************************' % total


total = 0.
for k in range(34*5):
    print "Processing....", k
    total += processAllBatch("TTJets_SemiLeptMGDecays", 1, "DiJetPt_TTJets_SemiLeptMGDecays_8TeV-madgraph", [k*10  +1,(k+1)*10 ])
print '\n**************************************\nFraction of processed sample: %s\n**************************************' % total


total = 0.
for k in range(16*5):
    print "Processing....", k
    total += processAllBatch("TTJets_FullLeptMGDecays", 1, "DiJetPt_TTJets_FullLeptMGDecays_8TeV-madgraph", [k*10 +1,(k+1)*10 ])
print '\n**************************************\nFraction of processed sample: %s\n**************************************' % total


total = 0.
for k in range(20*5):
    print "Processing....", k
    total += processAllBatch("TTJets_HadronicMGDecays",  1, "DiJetPt_TTJets_HadronicMGDecays_8TeV-madgraph", [k*10  +1,(k+1)*10 ])
print '\n**************************************\nFraction of processed sample: %s\n**************************************' % total


total = 0.
for k in range(9):
    print "Processing....", k
    total += processAllBatch("TTJets_MassiveBinDECAY", 1, "DiJetPt_TTJets_MassiveBinDECAY_8TeV-madgraph", [k*5  +1,(k+1)*5 ])
print '\n**************************************\nFraction of processed sample: %s\n**************************************' % total


total = 0.
for k in range(4):
    print "\nProcessing....", k
    ###total += processAllBatch("TTH125", 0, "DiJetPt_TTH_HToBB_M-125_8TeV-pythia6", [k*4  +1,(k+1)*4 ])
print '\n**************************************\nFraction of processed sample: %s\n**************************************' % total


total = 0.
for k in range(4):
    print "\nProcessing....", k
    ###total += processAllBatch("TTZ", 0, "DiJetPt_TTZJets_8TeV-madgraph", [k*4  +1,(k+1)*4 ])
print '\n**************************************\nFraction of processed sample: %s\n**************************************' % total

total = 0.
for k in range(2):
    print "\nProcessing....", k
    ###total += processAllBatch("TTW", 0, "DiJetPt_TTWJets_8TeV-madgraph", [k*4  +1,(k+1)*4 ])
print '\n**************************************\nFraction of processed sample: %s\n**************************************' % total


