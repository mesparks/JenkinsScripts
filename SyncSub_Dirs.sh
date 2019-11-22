prod_bucket=nw-testsync3
cdn_bucket_name=nwdev-cloudfront
csrc_bucket_name=nw-maven-1

target_bucket_dir_client=client
target_bucket_dir_jars=client-source-staging

aws s3 sync s3://$csrc_bucket_name/client-source s3://${prod_bucket}/${target_bucket_dir_jars} \
    --acl bucket-owner-full-control \
    --exact-timestamps \
    --region us-west-2 \
    --source-region us-west-1 \
    #--endpoint-url http://s3-accelerate.amazonaws.com


/home/nextw_source/utils/JenkinsScripts/syncdirs.py --srcbucket $cdn_bucket_name  --dstbucket $prod_bucket --nowork false