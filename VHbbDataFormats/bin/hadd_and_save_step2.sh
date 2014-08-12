#! /bin/sh

###############################
# hadd the root-files, produced by VHbb submitStep2.py to have one flat tree per dataset
# Specify INDIR -- directory of root files to hadd
#         OUTDIR -- directory of merged root files
# Optionally set CLEAN_UP=1 to remove input files to hadd on the go
#                COPY_TO_STORAGE=1 to copy trees from /home/ directory to storage element -- note that copying is slow.
###############################

if [ -z $ROOTSYS ]; then
 echo "ROOTSYS is not defined: source ROOT, or hadd won't work!"
 exit
fi

eval `scramv1 runtime -sh`
`voms-proxy-init -voms cms`

DO_HADD=1  # set to 0 if merged files are already created
CLEAN_UP=0
COPY_TO_STORAGE=1
OVERWRITE_FILES_AT_STORAGE=0 # set different from 0, if you want to overwrite existing files at storage element

#INDIR="Ntuples_withPDF2"
INDIR=$1 # directory with unmerged root files
OUTDIR_LOCAL=$INDIR/Ntuples_merged

#--------- EE storage --------
#OUTDIR_STORAGE="/hdfs/cms/store/user/liis/TTH_Ntuples_allHadTrig/"
#OUTDIR_STORAGE="/hdfs/cms/store/user/liis/TTH_Ntuples_allHadTrig_v2/"
#SRMPATH="srm://ganymede.hep.kbfi.ee:8888/srm/v2/server?SFN="

# --------- PSI storage ---------
OUTDIR_STORAGE="/pnfs/psi.ch/cms/trivcat/store/user/liis/TTH_Ntuples_allHadTrig_v2/"
SRMPATH="srm://t3se01.psi.ch:8443/srm/managerv2?SFN="

BASE_STR="DiJetPt_"
DATASETS=(
"DYJetsToLL_M-10To50_TuneZ2Star_8TeV-madgraph" 
#"TTH_HToBB_M-110_8TeV-pythia6" "TTH_HToBB_M-115_8TeV-pythia6" "TTH_HToBB_M-120_8TeV-pythia6" 
"TTH_HToBB_M-125_8TeV-pythia6" 
#"TTH_HToBB_M-130_8TeV-pythia6" "TTH_HToBB_M-135_8TeV-pythia6" 
"TTWJets_8TeV-madgraph" "TTZJets_8TeV-madgraph" "WZ_TuneZ2star_8TeV_pythia6_tauola" "ZZ_TuneZ2star_8TeV_pythia6_tauola" "WW_TuneZ2star_8TeV_pythia6_tauola" 
"WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball" 
"Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola" 
"Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola" 
"Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola" 
"T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola" 
"T_s-channel_TuneZ2star_8TeV-powheg-tauola" 
"T_t-channel_TuneZ2star_8TeV-powheg-tauola" 
"TTJets_FullLeptMGDecays_8TeV-madgraph" 
"TTJets_HadronicMGDecays_8TeV-madgraph" 
"TTJets_MassiveBinDECAY_8TeV-madgraph" 
"TTJets_SemiLeptMGDecays_8TeV-madgraph" 
"DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph" 
#"SingleMuRun2012AAug06" "SingleMuRun2012AJul13" "SingleMuRun2012BJul13" "SingleMuRun2012CAug24Rereco" "SingleMuRun2012C-EcalRecover_11Dec2012-v1_v2" "SingleMuRun2012CPromptv2" "SingleMuRun2012CPromptV2TopUp" "SingleMuRun2012D-PromptReco-v1" "SingleElectronRun2012AAug06EdmV42" "SingleElectronRun2012AJul13EdmV42b" "SingleElectronRun2012BJul13EdmV42" "SingleElectronRun2012CAug24RerecoEdmV42"  "SingleElectronRun2012C-EcalRecover_11Dec2012-v1_v2" "SingleElectronRun2012CPromptv2EdmV42" "SingleElectronRun2012CPromptV2TopUpEdmV42" "SingleElectronRun2012D-PromptReco-v1_v3" "DoubleElectron_Run2012A-recover-06Aug2012-v1_ProcV2" "DoubleElectron_Run2012A-13Jul2012-v1_ProcFIXED" "DoubleElectron_Run2012A-13Jul2012-v1_ProcV2" "DoubleElectron_Run2012B-13Jul2012-v1_ProcFIXED" "DoubleElectron_Run2012B-13Jul2012-v1_ProcV2" "DoubleElectronRun2012CAug24RerecoEdmV42" "DoubleElectronRun2012C-EcalRecover_11Dec2012-v1_v2" "DoubleElectron_Run2012C-PromptReco-v2_HBB_EDMNtupleV42_ProcV1" "DoubleElectron_Run2012C-PromptReco-v2_HBB_EDMNtupleV42_ProcV2" "DoubleElectronRun2012D"
"QCD_Pt-150_bEnriched_TuneZ2star_8TeV-pythia6"
"QCD_Pt-30To50_bEnriched_TuneZ2star_8TeV-pythia6"
"QCD_Pt-50To150_bEnriched_TuneZ2star_8TeV-pythia6"
)   

for DATASET in ${DATASETS[@]}
  do
  NR_ROOTFILES=`ls $INDIR"/"*$DATASET*.root 2> /dev/null | wc -l`
  echo Processing dataset $DATASET with $NR_ROOTFILES input files
  
  if [ $NR_ROOTFILES != 0 ]; then
      if [ $DO_HADD == 1 ]; then #create merged files
	  hadd -f $OUTDIR_LOCAL"/"$BASE_STR$DATASET.root $INDIR"/"*$DATASET*.root
      fi

      if [ $CLEAN_UP == 1 ]; then # clean up the rootfiles
	  echo "Removing initial root files... "
	  rm $INDIR"/"*$DATASET*.root
      fi  
  fi

  if [ $COPY_TO_STORAGE == 1 ] && [ -e $OUTDIR_LOCAL"/"$BASE_STR$DATASET.root ]; then
      echo copying $OUTDIR_LOCAL"/"$BASE_STR$DATASET.root to storage: $OUTDIR_STORAGE

      if [ -e $OUTDIR_STORAGE$BASE_STR$DATASET.root ] && [ $OVERWRITE_FILES_AT_STORAGE == 0 ] ; then
	  echo WARNING! Dataset already exists at destination -- file not copied!

      elif [ -e $OUTDIR_STORAGE$BASE_STR$DATASET.root ] && [ $OVERWRITE_FILES_AT_STORAGE == 1 ] ; then
	  echo Removing existing file from storage
	  srmrm $SRMPATH$OUTDIR_STORAGE$BASE_STR$DATASET.root
	  echo Replacing with new file
	  srmcp -2 "file:///./"$OUTDIR_LOCAL"/"$BASE_STR$DATASET.root $SRMPATH$OUTDIR_STORAGE$BASE_STR$DATASET.root
      else
	  echo "File does not exit in storage --> write"
	  srmcp -2 "file:///./"$OUTDIR_LOCAL"/"$BASE_STR$DATASET.root $SRMPATH$OUTDIR_STORAGE$BASE_STR$DATASET.root
      fi 
      echo ...done
  fi # end if copy to storage

done