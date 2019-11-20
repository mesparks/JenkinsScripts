#!/bin/bash
SRC_BUCKET_NAME=nwdev-cloudfront
DST_BUCKET_NAME=nw-testsync2

FILESTYPES_TO_EXCLUDE="*.js *.html"
DIRS_TO_EXCLUDE="assets/*"
EXCLUDE="--exclude *assets/*"
INCLUDE=" "

for exclude in $FILESTYPES_TO_EXCLUDE
do
  EXCLUDE="$EXCLUDE --exclude $exclude"
done

aws2 s3 ls s3://nwdev-cloudfront | grep  "/" | awk '{print $NF}' | grep -v assets | 
while read include_dir
do
   echo $include_dir
   for include_type in $FILESTYPES_TO_EXCLUDE
   do
      echo $include_type
      echo INCLUDE="$INCLUDE --include $include_dir/$include_type"
   done
done




echo $EXCLUDE $INCLUDE




#aws2 s3 ls s3://nwdev-cloudfront | grep  "/" | awk '{print $NF}' | grep -v assets |  while read line; do echo "--include *$line*"; done


#aws2 s3 sync s3://nw-testsync1/ s3//nw-testsync2 --exclude "assets/*" --exclude "*.js" --exclude "*.html"  --include "*master*/*.js" --include "*master*/*.html"