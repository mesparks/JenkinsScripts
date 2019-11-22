#!/usr/bin/env python3
import boto3
import subprocess
import sys
import argparse
import logging


parser = argparse.ArgumentParser(description='S3 Copier')
parser.add_argument("--srcbucket", help="Source Destination Bucket",default="nw-testsync1", type=str)
parser.add_argument("--dstbucket", help="Destination S3 Bucket",default="nw-testsync2", type=str)
parser.add_argument("--dstdir", help="Destination Directory",default="client", type=str)
parser.add_argument("--nowork", help="By default, just show command and do not do work",default="true", type=str)
parser.add_argument("--acl", help="ACL to use",default="bucket-owner-full-control", type=str)

# parser.add_argument("--dstregion", help="Destination Region",default="us-west-1", type=str)
# parser.add_argument("--dstregion", help="Destination Region",default="us-west-1", type=str)
args = parser.parse_args()

# extra_args = "--acl public-read-write --exact-timestamps --endpoint-url http://s3-accelerate.amazonaws.com"
extra_args = "--acl  %s --exact-timestamps  --exclude 'dev/*' --exclude '*/genapp/*'" % args.acl
# Setting logging facility
logging.basicConfig(format='%(asctime)s- %(levelname)s - %(message)s', level=logging.INFO)

src_bucket_name = args.srcbucket
dst_bucket_name = args.dstbucket

dst_directory = args.dstdir
# dirs = []
root_excludes = ["*.js","*.html","*assets*","*.txt","*.png","*.woff","*.woff2","*.eot","*.ttf","*.css","*.svg"]
exclude_dirs = ["*genapp*","assets/","dev/"]
logging.info("Getting directories from bucket")
logging.info("Excluding file types: %s", root_excludes)
logging.info("Global Excludes: %s", exclude_dirs)
# Getting directories from root of src bucket
client = boto3.client('s3')
# Let's determine bucket regions
src_bucket_region = client.get_bucket_location(Bucket=src_bucket_name)["LocationConstraint"]
dst_bucket_region = client.get_bucket_location(Bucket=dst_bucket_name)["LocationConstraint"]
# If regions are different then append them to the aws command
if src_bucket_region != dst_bucket_region:
    logging.info("Buckets are in diferent regions, adding region flags")
    extra_args = extra_args + " " +  "--region %s --source-region %s" % (dst_bucket_region, src_bucket_region)


def getdirs(bucket_name):
    dirs = []
    result = client.list_objects(Bucket=bucket_name, Delimiter='/')
    for o in result.get('CommonPrefixes'):
        dirs.append(o.get('Prefix'))
    return dirs




# exclude_line = ""
# # Build Exclude Dir Line
# for exclude in exclude_dirs:
#     exclude_line = exclude_line + " " + "--exclude \"%s*\" " % exclude

# # Build Exclude File Types
# for exclude in root_excludes:
#     exclude_line = exclude_line + " " + "--exclude \"%s\" " % exclude


# include_line = ""


def sync_subdir(subdir):
    sync_cmd = ("aws s3 sync s3://%s/%s s3://%s/%s/%s %s " % (src_bucket_name, subdir,dst_bucket_name,dst_directory, subdir, extra_args))
    logging.info ("Running AWS Sync Command: %s" % sync_cmd)
    if args.nowork == "true":
        logging.info("Not doing any work, if you want to do work set --nowork to false")
        return 0

    # Keep a filecount for output
    filescount = 0
    p = subprocess.Popen(sync_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while(True):
        # returns None while subprocess is running
        retcode = p.poll() 
        line = p.stdout.readline()
        logging.debug(line.decode("utf-8"))
        if " error " in line.decode("utf-8"):
            logging.error(line.decode("utf-8"))
        elif "copy" in line.decode("utf-8"):
            filescount = filescount + 1
            if filescount % 500 == 0:
                logging.info("Files copied: %d" % filescount)
        else:
            logging.info(line.decode("utf-8"))
        # yield line
        if retcode is not None:
            break

    logging.info("Copied %d files . . ." % filescount)
    logging.info ("Ran AWS Sync Command: %s" % sync_cmd)
    if retcode == 0:
        logging.info ("Return Code: %d" % retcode)
    else:
        logging.error("Return Code: %d" % retcode)
    return retcode




dirs = getdirs(src_bucket_name)
logging.info("Found Directories: %s", dirs)
# Build include line
for dir in dirs:
    if dir not in exclude_dirs:
        logging.info("Syncing directory %s" % dir)
        ret_code = sync_subdir(dir)
        if ret_code != 0:
            sys.exit(ret_code)