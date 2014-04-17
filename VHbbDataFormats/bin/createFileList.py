
#!/usr/bin/env python

import commands
import re
import os
import FWCore.ParameterSet.Config as cms

import subprocess

import sys
import string
sys.path.append('./')


def processAllBatch(path,jobName):

    print '\nNow doing.............' , jobName
    os.system('lcg-ls -b -D srmv2  srm://stormfe1.pi.infn.it:8444/srm/managerv2?SFN=/cms/'+path+' > fileList_'+jobName+'_tmp.txt')
    os.system("sed -i 's/\/cms//g' fileList_"+jobName+"_tmp.txt")
    #os.system('cat fileList_'+jobName+'_tmp.txt | grep PAT | wc -l')

    output = open('fileList_'+jobName+'.txt','w')
    input  = open('fileList_'+jobName+'_tmp.txt','r')
    counter = 0

    jobs = []

    for line in input:
        foo = line.strip('\n')
        splits = string.split(foo, '_')

        #print splits

        stop        =   0
        count_split =  -1 

        for split in splits:
            count_split += 1
            if stop>0:
                break
            if string.find( split, 'PAT.edm')>0:
                stop = 1

        if stop==0:
            break
        
        job_number = int(splits[count_split])
        #print job_number

        isThere = False
        for job in jobs:
            if job==job_number:
                isThere = True        

        if not isThere:
            jobs.append( job_number )
            output.write( foo+'\n' )
            
        else:
            print "Job num. %s is duplicated" %  job_number
        
        counter += 1
        
    input.close()
    output.close()

    os.system('rm fileList_'+jobName+'_tmp.txt')
    
    print  "Total files: %s --> %s " % (counter, len(jobs))

#################################

processAllBatch( '/store/user/lpchbb/degrutto/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarballSummer12_DR53X-PU_S10_START53_V7A-v1/degrutto/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/HBB_EDMNtupleV42/9803889241b1fc304f795d3b3875632d/','DYJets50')
processAllBatch( '/store/user/lpchbb/degrutto//WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarballSummer12_DR53X-PU_S10_START53_V7A-v1/degrutto/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/HBB_EDMNtupleV42/9803889241b1fc304f795d3b3875632d/', 'WJetsToLNu' )

processAllBatch( '/store/user/lpchbb/degrutto/T_s-channel_TuneZ2star_8TeV-powheg-tauolaSummer12_DR53X-PU_S10_START53_V7A-v1_v2/degrutto/T_s-channel_TuneZ2star_8TeV-powheg-tauola/HBB_EDMNtupleV42/9803889241b1fc304f795d3b3875632d/', 'T_s-channel' )
processAllBatch( '/store/user/lpchbb/degrutto/T_t-channel_TuneZ2star_8TeV-powheg-tauolaSummer12_DR53X-PU_S10_START53_V7A-v1/degrutto/T_t-channel_TuneZ2star_8TeV-powheg-tauola/HBB_EDMNtupleV42/9803889241b1fc304f795d3b3875632d/', 'T_t-channel' )
processAllBatch( '/store/user/lpchbb/degrutto/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauolaSummer12_DR53X-PU_S10_START53_V7A-v1_v2/degrutto/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/HBB_EDMNtupleV42/9803889241b1fc304f795d3b3875632d/', 'T_tW-channel-DR' )
processAllBatch( '/store/user/lpchbb/degrutto/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauolaSummer12_DR53X-PU_S10_START53_V7A-v1/degrutto/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/HBB_EDMNtupleV42/9803889241b1fc304f795d3b3875632d/', 'Tbar_t-channel' )
processAllBatch( '/store/user/lpchbb/degrutto/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauolaSummer12_DR53X-PU_S10_START53_V7A-v1_v2/degrutto/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola/HBB_EDMNtupleV42/9803889241b1fc304f795d3b3875632d/', 'Tbar_s-channel' )
processAllBatch( '/store/user/lpchbb/degrutto/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauolaSummer12_DR53X-PU_S10_START53_V7A-v1_v2/degrutto/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/HBB_EDMNtupleV42/9803889241b1fc304f795d3b3875632d/', 'Tbar_tW-channel-DR' )

processAllBatch( '/store/user/lpchbb/dlopes/WW_Summer12_53X_V42b/dlopes/WW_TuneZ2star_8TeV_pythia6_tauola/HBB_EDMNtupleV42/9803889241b1fc304f795d3b3875632d', 'WW' )
processAllBatch( '/store/user/lpchbb/dlopes/WZ_Summer12_53X_V42b//dlopes/WZ_TuneZ2star_8TeV_pythia6_tauola//HBB_EDMNtupleV42/9803889241b1fc304f795d3b3875632d', 'WZ' )
processAllBatch( '/store/user/lpchbb/dlopes/ZZ_Summer12_53X_V42b/dlopes/ZZ_TuneZ2star_8TeV_pythia6_tauola/HBB_EDMNtupleV42/9803889241b1fc304f795d3b3875632d', 'ZZ' )

processAllBatch( '/store/user/arizzi/TTJets_SemiLeptMGDecays_8TeV-madgraph/TTJets_SemiLeptMGDecays_8TeV-madgraph_Summer12_DR53X-PU_S10_START53_V7A_ext-v1_EDMNtuple_V42_ProcV1/9803889241b1fc304f795d3b3875632d/', 'TTJets_SemiLeptMGDecays' )
processAllBatch( '/store/user/arizzi/TTJets_FullLeptMGDecays_8TeV-madgraph/TTJets_FullLeptMGDecays_8TeV-madgraph_Summer12_DR53X-PU_S10_START53_V7A-v2_EDMNtuple_V42_ProcV1/9803889241b1fc304f795d3b3875632d', 'TTJets_FullLeptMGDecays' )
processAllBatch( '/store/user/arizzi/TTJets_HadronicMGDecays_8TeV-madgraph/TTJets_HadronicMGDecays_8TeV-madgraph_Summer12_DR53X-PU_S10_START53_V7A_ext-v1_EDMNtuple_V42_ProcV1/9803889241b1fc304f795d3b3875632d/', 'TTJets_HadronicMGDecays' )

processAllBatch( '/store/user/nmohr/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/WZJetsTo2L2Q_TuneZ2star_8TeV_madgraph_tauola_TTJets_MassiveBinDECAY_TuneZ2star_8TeV_madgraph_tauola/6a5d9bb3161446313514456198d10252', 'TTJets_MassiveBinDECAY' )









#processAllBatch( '/store/user/lpchbb/dlopes/SingleMuRun2012AJul13EdmV42//dlopes/SingleMu/HBB_EDMNtupleV42//5acd311e7ac1c2e546a3f05006d77347','SingleMuRun2012AJul13')
#processAllBatch( '/store/user/lpchbb/dlopes/SingleMuRun2012AAug06EdmV42//dlopes/SingleMu/HBB_EDMNtupleV42//5acd311e7ac1c2e546a3f05006d77347','SingleMuRun2012AAug06')
#processAllBatch( '/store/user/lpchbb/dlopes/SingleMuRun2012BJul13EdmV42//dlopes/SingleMu/HBB_EDMNtupleV42//5acd311e7ac1c2e546a3f05006d77347','SingleMuRun2012BJul13')
#processAllBatch( '/store/user/lpchbb/dlopes/SingleMuRun2012CAug24RerecoEdmV42/dlopes/SingleMu/HBB_EDMNtupleV42//ab1a3db7adbffc128e4f72c6b5c4705e', 'SingleMuRun2012CAug24Rereco' )
#processAllBatch( '/store/user/lpchbb/dlopes/SingleMuRun2012CPromptv2EdmV42//dlopes/SingleMu/HBB_EDMNtupleV42/ab1a3db7adbffc128e4f72c6b5c4705e', 'SingleMuRun2012CPromptv2' )
#processAllBatch( '/store/user/lpchbb/dlopes/SingleMuRun2012CPromptV2TopUpEdmV42//dlopes/SingleMu/HBB_EDMNtupleV42/ab1a3db7adbffc128e4f72c6b5c4705e', 'SingleMuRun2012CPromptV2TopUp' )

##processAllBatch( '/store/user/nmohr/DoubleElectron/TBarToThadWlep_tW_channel_DR_8TeV_powheg_tauola_DoubleElectron_Run2012A-13Jul2012-v1_ProcV2/0260354141ac644fd026603611dde4ca', 'DoubleElectron_Run2012A-13Jul2012-v1' )
##processAllBatch( '/store/user/nmohr/DoubleElectron/TBarToThadWlep_tW_channel_DR_8TeV_powheg_tauola_DoubleElectron_Run2012A-recover-06Aug2012-v1_ProcV2/d286e060d8c6649e65456db4666c8187', '' )
##processAllBatch( '/store/user/nmohr/DoubleElectron/TBarToThadWlep_tW_channel_DR_8TeV_powheg_tauola_DoubleElectron_Run2012B-13Jul2012-v1_ProcV2/0260354141ac644fd026603611dde4ca', 'DoubleElectron_Run2012B-13Jul2012-v1', '' )
##processAllBatch( '/store/user/lpchbb/dlopes/DoubleElectronRun2012CAug24RerecoEdmV42/dlopes/DoubleElectron/HBB_EDMNtupleV42/ab1a3db7adbffc128e4f72c6b5c4705e/','DoubleElectronRun2012CAug24RerecoEdmV42')
##processAllBatch( '/store/user/bortigno/DoubleElectron/DoubleElectron_Run2012C-PromptReco-v2_HBB_EDMNtupleV42_ProcV1/ab1a3db7adbffc128e4f72c6b5c4705e', '' )
##processAllBatch( '/store/user/lpchbb/degrutto/DoubleElectronRun2012C-EcalRecover_11Dec2012-v1_v2/degrutto/DoubleElectron/DoubleElectronRun2012C-EcalRecover_11Dec2012-v1_v2/225d03e147cd35bb368280b3d5f9e456/', '' )
##processAllBatch( '/store/user/lpchbb/degrutto/DoubleElectronRun2012D/degrutto/DoubleElectron/DoubleElectronRun2012D/934bfbbec794fc84841053b5d64bf13c/', '' )

##processAllBatch( '/store/user/lpchbb/dlopes/SingleMuRun2012AJul13EdmV42/dlopes/SingleMu/HBB_EDMNtupleV42/5acd311e7ac1c2e546a3f05006d77347', 'SingleMuRun2012AJul13EdmV42' )
##processAllBatch( '/store/user/lpchbb/dlopes/SingleMuRun2012AAug06EdmV42//dlopes/SingleMu/HBB_EDMNtupleV42/5acd311e7ac1c2e546a3f05006d77347', 'SingleMuRun2012AAug06EdmV42' )
##processAllBatch( '/store/user/lpchbb/dlopes/SingleMuRun2012BJul13EdmV42//dlopes/SingleMu/HBB_EDMNtupleV42/5acd311e7ac1c2e546a3f05006d77347', 'SingleMuRun2012BJul13EdmV42' )
##processAllBatch( '/store/user/lpchbb/dlopes/SingleMuRun2012CAug24RerecoEdmV42/dlopes/SingleMu/HBB_EDMNtupleV42/ab1a3db7adbffc128e4f72c6b5c4705e', 'SingleMuRun2012CAug24RerecoEdmV42' )
##processAllBatch( '/store/user/lpchbb/dlopes/SingleMuRun2012CPromptv2EdmV42//dlopes/SingleMu/HBB_EDMNtupleV42/ab1a3db7adbffc128e4f72c6b5c4705e', 'SingleMuRun2012CPromptv2EdmV42' )
##processAllBatch( '/store/user/lpchbb/dlopes/SingleMuRun2012CPromptV2TopUpEdmV42//dlopes/SingleMu/HBB_EDMNtupleV42/ab1a3db7adbffc128e4f72c6b5c4705e', 'SingleMuRun2012CPromptV2TopUpEdmV42' )
##processAllBatch( '/store/user/lpchbb/degrutto/SingleElectronRun2012D-PromptReco-v1_v3/degrutto/SingleElectron/SingleElectronRun2012D-PromptReco-v1_v3/934bfbbec794fc84841053b5d64bf13c/', 'SingleElectronRun2012D-PromptReco-v1_v3' )
##processAllBatch( '/store/user/lpchbb/degrutto/SingleElectronRun2012C-EcalRecover_11Dec2012-v1_v2/degrutto/SingleElectron/SingleElectronRun2012C-EcalRecover_11Dec2012-v1_v2/225d03e147cd35bb368280b3d5f9e456/', 'SingleElectronRun2012C-EcalRecover_11Dec2012-v1_v2' )

##processAllBatch( '/store/user/lpchbb/degrutto/SingleMuRun2012D-PromptReco-v1/degrutto/SingleMu/SingleMuRun2012D-PromptReco-v1/934bfbbec794fc84841053b5d64bf13c/', 'SingleMuRun2012D-PromptReco-v1' )
##processAllBatch( '/store/user/lpchbb/degrutto/SingleMuRun2012C-EcalRecover_11Dec2012-v1_v2/degrutto/SingleMu/SingleMuRun2012C-EcalRecover_11Dec2012-v1_v2/225d03e147cd35bb368280b3d5f9e456/', 'SingleMuRun2012C-EcalRecover_11Dec2012-v1_v2' )

#processAllBatch( '', '' )



