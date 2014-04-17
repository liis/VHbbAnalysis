#! /bin/sh


data=$(ls DiJetPt_*)
outdir="srm://t3se01.psi.ch:8443/srm/managerv2?SFN=/pnfs/psi.ch/cms/trivcat/store/user/bianchi/HBB_EDMNtuple/AllHDiJetPt_V3/"

for name in ${data}
do
  echo "Copy: " $name 
  echo " -->  " ${outdir}"/"$1"/"${name}
  lcg-cp -b -D srmv2 $name  ${outdir}"/"$1"/"${name}
done