#!/usr/bin/env bash
set -euo pipefail

# You probably shouldn't run this file, just copy and paste from it into the shell.

# clip 1850-2005 member at 1920

nces -d time,840,1871 "b.e11.B20TRC5CNBDRD.f09_g16.001.cam.h0.TREFHT.185001-200512.nc" "b.e11.B20TRC5CNBDRD.f09_g16.001.cam.h0.TREFHT.192001-200512.nc"

# Take 2

for i in {001..033};
do
    f1="b.e11.B20TRC5CNBDRD.f09_g16.$i.cam.h0.TREFHT.192001-200512.nc";
    f2="b.e11.BRCP85C5CNBDRD.f09_g16.$i.cam.h0.TREFHT.200601-208012.nc";
    f3="b.e11.BRCP85C5CNBDRD.f09_g16.$i.cam.h0.TREFHT.208101-210012.nc";
    ncrcat $f1 $f2 $f3 -D 2 -o "b.e11.BRCP85C5CNBDRD.f09_g16.$i.cam.h0.TREFHT.192001-210012.nc";
done

for i in {034,035,101,102,103,104,105};
do
    f1="b.e11.B20TRC5CNBDRD.f09_g16.$i.cam.h0.TREFHT.192001-200512.nc";
    f2="b.e11.BRCP85C5CNBDRD.f09_g16.$i.cam.h0.TREFHT.200601-210012.nc";
    ncrcat $f1 $f2 -D 2 -o "b.e11.BRCP85C5CNBDRD.f09_g16.$i.cam.h0.TREFHT.192001-210012.nc";
done

ncrcat b.e11.B20TRC5CNBDRD.f09_g16.035.cam.h0.TREFHT.192001-200512.nc b.e11.BRCP85C5CNBDRD.f09_g16.035.cam.h0.TREFHT.200601-210012.nc -D 3 -o b.e11.BRCP85C5CNBDRD.f09_g16.035.cam.h0.TREFHT.192001-210012.nc

# Try this to check stuff
for f in $(ls | grep "192001-210012.nc$"); do echo $f; ncdump -h $f | grep "currently"; echo ""; done
for f in $(ls | grep "192001-208012.nc$"); do echo $f; ncdump -h $f | grep "currently"; echo ""; done

# Last step for cesm1 trefht

ls | grep "b.e11.BRCP85C5CNBDRD.f09_g16.\d\{3\}.cam.h0.TREFHT.192001-210012.nc" | ncecat -D 3 -o "b.e11.BRCP85C5CNBDRD.f09_g16.all.cam.h0.TREFHT.192001-210012.nc"

# For CESM1SF TREFHT fields

# xAER
for i in {001..020};
do
    f1="b.e11.B20TRLENS_RCP85.f09_g16.xaer.$i.cam.h0.TREFHT.192001-200512.nc";
    f2="b.e11.B20TRLENS_RCP85.f09_g16.xaer.$i.cam.h0.TREFHT.200601-208012.nc";
    ncrcat $f1 $f2 -D 2 -o "b.e11.B20TRLENS_RCP85.f09_g16.xaer.$i.cam.h0.TREFHT.192001-208012.nc"
done

ls | grep "b.e11.B20TRLENS_RCP85.f09_g16.xaer.\d\{3\}.cam.h0.TREFHT.192001-208012.nc$" | ncecat -D 3 -o "b.e11.B20TRLENS_RCP85.f09_g16.xaer.all.cam.h0.TREFHT.192001-208012.nc"

# xGHG
for i in {001..020};
do
    f1="b.e11.B20TRLENS_RCP85.f09_g16.xghg.$i.cam.h0.TREFHT.192001-200512.nc";
    f2="b.e11.B20TRLENS_RCP85.f09_g16.xghg.$i.cam.h0.TREFHT.200601-208012.nc";
    ncrcat $f1 $f2 -D 2 -o "b.e11.B20TRLENS_RCP85.f09_g16.xghg.$i.cam.h0.TREFHT.192001-208012.nc"
done

ls | grep "b.e11.B20TRLENS_RCP85.f09_g16.xghg.\d\{3\}.cam.h0.TREFHT.192001-208012.nc$" | ncecat -D 3 -o "b.e11.B20TRLENS_RCP85.f09_g16.xghg.all.cam.h0.TREFHT.192001-208012.nc"

# xBMB
ls | grep "b.e11.B20TRLENS_RCP85.f09_g16.xbmb.\d\{3\}.cam.h0.TREFHT.192001-202912.nc$" | ncecat -D 3 -o "b.e11.B20TRLENS_RCP85.f09_g16.xbmb.all.cam.h0.TREFHT.192001-202912.nc"

# xLULC
ls | grep "b.e11.B20TRLENS_RCP85.f09_g16.xlulc.\d\{3\}.cam.h0.TREFHT.192001-202912.nc$" | ncecat -D 3 -o "b.e11.B20TRLENS_RCP85.f09_g16.xlulc.all.cam.h0.TREFHT.192001-202912.nc"

# 1850 ctl
ls | grep "b.e11.B1850C5CN.f09_g16.005.cam.h0.TREFHT.\d\{6\}-\d\{6\}.nc" | ncrcat -D 2 -o "b.e11.B1850C5CN.f09_g16.005.cam.h0.TREFHT.040001-220012.nc"

# CESM2 TREFHT
bits=(
"1011.001"
"1031.002"
"1051.003"
"1071.004"
"1091.005"
"1111.006"
"1131.007"
"1151.008"
"1231.011"
"1231.012"
"1231.013"
"1231.014"
"1231.015"
"1231.016"
"1231.017"
"1231.018"
"1231.019"
"1231.020"
"1251.011"
"1251.012"
"1251.013"
"1251.014"
"1251.015"
"1251.016"
"1251.017"
"1251.018"
"1251.019"
"1251.020"
"1281.011"
"1281.012"
"1281.013"
"1281.014"
"1281.015"
"1281.016"
"1281.017"
"1281.018"
"1281.019"
"1281.020"
"1301.011"
"1301.012"
"1301.013"
"1301.014"
"1301.015"
"1301.016"
"1301.017"
"1301.018"
"1301.019"
"1301.020"
)

 for b in {1..48};
 do
     echo $b;
     echo $bits[b];
     ls | grep "$bits[b]" | grep "smbb" | ncrcat -o "b.e21.BOTH.f09_g17.LE2-$bits[b].cam.h0.TREFHT.185001-210012.nc";
 done

 ls | grep "BOTH" | ncecat -D 2 -o "b.e21.BOTH.f09_g17.LE2-XXXX.all.cam.h0.TREFHT.185001-210012.nc"


 # CESM TEMPDT
 #
 #

# 1850 ctl
ls | grep "b.e11.B1850C5CN.f09_g16.005.pop.h.TEMPDT.\d\{6\}-\d\{6\}.nc" | ncrcat -D 2 -o "b.e11.B1850C5CN.f09_g16.005.pop.h.TEMPDT.040001-220012.nc"

# clip 1850-2005 member at 1920
nces -d time,840,1871 "b.e11.B20TRC5CNBDRD.f09_g16.001.pop.h.TEMPDT.185001-200512.nc" "b.e11.B20TRC5CNBDRD.f09_g16.001.pop.h.TEMPDT.192001-200512.nc"

# Take 2

for i in {001..033};
do
    f1="b.e11.B20TRC5CNBDRD.f09_g16.$i.pop.h.TEMPDT.192001-200512.nc";
    f2="b.e11.BRCP85C5CNBDRD.f09_g16.$i.pop.h.TEMPDT.200601-208012.nc";
    f3="b.e11.BRCP85C5CNBDRD.f09_g16.$i.pop.h.TEMPDT.208101-210012.nc";
    echo $i
    ncrcat $f1 $f2 $f3 -D 2 -o "b.e11.BRCP85C5CNBDRD.f09_g16.$i.pop.h.TEMPDT.192001-210012.nc";
done

for i in {034,035,101,102,103,104,105};
do
    f1="b.e11.B20TRC5CNBDRD.f09_g16.$i.pop.h.TEMPDT.192001-200512.nc";
    f2="b.e11.BRCP85C5CNBDRD.f09_g16.$i.pop.h.TEMPDT.200601-210012.nc";
    ncrcat $f1 $f2 -D 2 -o "b.e11.BRCP85C5CNBDRD.f09_g16.$i.pop.h.TEMPDT.192001-210012.nc";
done

ncrcat b.e11.B20TRC5CNBDRD.f09_g16.035.pop.h.TEMPDT.192001-200512.nc b.e11.BRCP85C5CNBDRD.f09_g16.035.pop.h.TEMPDT.200601-210012.nc -D 3 -o b.e11.BRCP85C5CNBDRD.f09_g16.035.pop.h.TEMPDT.192001-210012.nc

# Try this to check stuff
for f in $(ls | grep "192001-210012.nc$"); do echo $f; ncdump -h $f | grep "currently"; echo ""; done
for f in $(ls | grep "192001-208012.nc$"); do echo $f; ncdump -h $f | grep "currently"; echo ""; done

# Last step for cesm1 trefht

ls | grep "b.e11.BRCP85C5CNBDRD.f09_g16.\d\{3\}.pop.h.TEMPDT.192001-210012.nc" | ncecat -D 3 -o "b.e11.BRCP85C5CNBDRD.f09_g16.all.pop.h.TEMPDT.192001-210012.nc"
