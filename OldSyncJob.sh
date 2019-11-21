
prod_bucket=nw-arch-oregon
cdn_bucket_name=nwdev-cloudfront
csrc_bucket_name=nw-maven-1

target_bucket_dir_client=client
target_bucket_dir_jars=client-source-staging

AWS_ACCESS_KEY_ID=$aws_key AWS_SECRET_ACCESS_KEY=$aws_secret \
aws s3 sync s3://$csrc_bucket_name/client-source s3://${prod_bucket}/${target_bucket_dir_jars} \
    --acl bucket-owner-full-control \
    --exact-timestamps \
    --region us-west-2 \
    --source-region us-west-1 \
    --endpoint-url http://s3-accelerate.amazonaws.com

AWS_ACCESS_KEY_ID=$aws_key AWS_SECRET_ACCESS_KEY=$aws_secret \
aws s3 sync s3://$cdn_bucket_name/ s3://${prod_bucket}/${target_bucket_dir_client} \
    --exclude 'dev/*' \
    --exclude '*/genapp/*' \
    --exclude '*/assests/*' \
    --exclude '*.js' \
    --exclude '*.txt' \
    --exclude '*.html' \
    --exclude '*.png' \
    --exclude '*.woff' \
    --exclude '*.woff2' \
    --exclude '*.eot' \
    --exclude '*.ttf' \
    --exclude '*.svg' \
    --exclude '*.css' \
    --acl public-read-write \
    --exact-timestamps \
    --region us-west-2 \
    --source-region us-west-1 \
    --endpoint-url http://s3-accelerate.amazonaws.com