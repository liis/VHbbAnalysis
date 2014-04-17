#!/bin/bash

cd /home/liis/TTH_Ntuples/CMSSW_5_3_3/src/VHbbAnalysis/VHbbDataFormats/bin/
export SCRAM_ARCH="slc5_amd64_gcc462"
source $VO_CMS_SW_DIR/cmsset_default.sh
eval `scramv1 runtime -sh`


Ntupler myStep2_TTJets_FullLeptMGDecays_8TeV-madgraph_211-240.py

