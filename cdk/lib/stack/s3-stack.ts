import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as s3 from 'aws-cdk-lib/aws-s3';
import { getAccountUniqueName, Account } from '../config/accounts';
import { MoneybookStackProps } from '../moneybook-stack';
import { SYSTEM_NAME } from '../config/commons';

export class MoneybookS3Stack extends cdk.Stack {
    public bucket: s3.IBucket
    
    constructor(scope: Construct, id: string, props: MoneybookStackProps) {
        super(scope, id, props);

        const bucekt = new s3.Bucket(this, `${SYSTEM_NAME}-S3`, {
            bucketName: `${getAccountUniqueName(props.context)}-moneybook-bucket`.toLowerCase(),
            publicReadAccess: false,
            blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
            encryption: s3.BucketEncryption.S3_MANAGED,
        });
        this.bucket = bucekt;
    }
}
