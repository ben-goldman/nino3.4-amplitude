#!/usr/bin/env bash
set -euo pipefail

# You probably shouldn't run this file, just copy and paste from it into the shell.

# clip 1850-2005 member at 1920

nces -d time,840,1871 "b.e11.B20TRC5CNBDRD.f09_g16.001.cam.h0.TREFHT.185001-200512.nc" "b.e11.B20TRC5CNBDRD.f09_g16.001.cam.h0.TREFHT.192001-200512.nc"

# ensemble concatenate cesm1 trefht members *DEPRECATED*

ls | grep "b.e11.B20TRC5CNBDRD.f09_g16.\d\{3\}.cam.h0.TREFHT.192001-200512.nc" | ncecat -D 2 -o "b.e11.B20TRC5CNBDRD.f09_g16.all.cam.h0.TREFHT.192001-200512.nc"
ls | grep "b.e11.BRCP85C5CNBDRD.f09_g16.\d\{3\}.cam.h0.TREFHT.200601-208012.nc" | ncecat -D 2 -o "b.e11.BRCP85C5CNBDRD.f09_g16.001-033.cam.h0.TREFHT.200601-208012.nc"
ls | grep "b.e11.BRCP85C5CNBDRD.f09_g16.\d\{3\}.cam.h0.TREFHT.208101-210012.nc" | ncecat -D 2 -o "b.e11.BRCP85C5CNBDRD.f09_g16.001-033.cam.h0.TREFHT.208101-210012.nc"
ls | grep "b.e11.BRCP85C5CNBDRD.f09_g16.\d\{3\}.cam.h0.TREFHT.200601-210012.nc" | ncecat -D 2 -o "b.e11.BRCP85C5CNBDRD.f09_g16.034-105.cam.h0.TREFHT.200601-210012.nc"

# record concatenate 2006-2080 and 2080-2100 files *DEPRECATED*

ls | grep "b.e11.BRCP85C5CNBDRD.f09_g16.001-033.cam.h0.TREFHT.\d\{6\}-\d\{6\}.nc" | ncrcat -D 2 -o "b.e11.BRCP85C5CNBDRD.f09_g16.001-033.cam.h0.TREFHT.200601-210012.nc"
ncecat -D 2 "b.e11.BRCP85C5CNBDRD.f09_g16.001-033.cam.h0.TREFHT.200601-210012.nc" "b.e11.BRCP85C5CNBDRD.f09_g16.034-105.cam.h0.TREFHT.200601-210012.nc" "b.e11.BRCP85C5CNBDRD.f09_g16.all.cam.h0.TREFHT.200601-210012.nc"

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

# Last step for cesm1 trefht

ls | grep "b.e11.BRCP85C5CNBDRD.f09_g16.\d\{3\}.cam.h0.TREFHT.192001-210012.nc" | ncecat -D 3 -o "b.e11.BRCP85C5CNBDRD.f09_g16.all.cam.h0.TREFHT.192001-210012.nc"
