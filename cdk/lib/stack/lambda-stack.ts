import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as s3 from 'aws-cdk-lib/aws-s3';
import { getAccountUniqueName } from "../config/accounts";
import { MoneybookStackProps } from "../moneybook-stack";
import { SYSTEM_NAME } from "../config/commons";
import { PythonFunction } from '@aws-cdk/aws-lambda-python-alpha';
import { Runtime } from 'aws-cdk-lib/aws-lambda';
import * as path from "path";
import { ManagedPolicy, Role, ServicePrincipal, CompositePrincipal, PolicyDocument, PolicyStatement, Effect } from "aws-cdk-lib/aws-iam";

export class MoneybookLambdaStack extends cdk.Stack {

    constructor(scope: Construct, id: string, props: MoneybookStackProps) {
        super(scope, id, props);

        const lambdaRole = new Role(this, `${SYSTEM_NAME}-lambda-role`, {
            roleName: `${getAccountUniqueName(props.context)}-lambda-role`,
            assumedBy: new CompositePrincipal(
                new ServicePrincipal('lambda.amazonaws.com'),
            ),
            managedPolicies: [
                ManagedPolicy.fromAwsManagedPolicyName('service-role/AWSLambdaBasicExecutionRole'),
                ManagedPolicy.fromAwsManagedPolicyName('AmazonS3FullAccess'),
            ]
        })

        // index.py -> lambda_handler
        //
        new PythonFunction(this, `${SYSTEM_NAME}-create-file`, {
            functionName: `${getAccountUniqueName(props.context)}-create-file`,
            entry: path.join(__dirname, '../../../app/backend'),
            index: 'create_file.py',
            runtime: Runtime.PYTHON_3_10,
            role: lambdaRole,
            environment: {
                'BUCKET_NAME': props.s3Stack!.bucket.bucketName,
            }
        })

        new PythonFunction(this, `${SYSTEM_NAME}-create-csv`, {
            functionName: `${getAccountUniqueName(props.context)}-create-csv`,
            entry: path.join(__dirname, '../../../app/backend/c_csv'),
            index: 'c_csv.py',
            runtime: Runtime.PYTHON_3_10,
            role: lambdaRole,
            environment: {
                'BUCKET_NAME': props.s3Stack!.bucket.bucketName,
            }
        })

        new PythonFunction(this, `${SYSTEM_NAME}-read-csv`, {
            functionName: `${getAccountUniqueName(props.context)}-read-csv`,
            entry: path.join(__dirname, '../../../app/backend/r_csv'),
            index: 'r_csv.py',
            runtime: Runtime.PYTHON_3_10,
            role: lambdaRole,
            environment: {
                'BUCKET_NAME': props.s3Stack!.bucket.bucketName,
            }
        })

        new PythonFunction(this, `${SYSTEM_NAME}-update-csv`, {
            functionName: `${getAccountUniqueName(props.context)}-update-csv`,
            entry: path.join(__dirname, '../../../app/backend/u_csv'),
            index: 'u_csv.py',
            runtime: Runtime.PYTHON_3_10,
            role: lambdaRole,
            environment: {
                'BUCKET_NAME': props.s3Stack!.bucket.bucketName,
            }
        })

        new PythonFunction(this, `${SYSTEM_NAME}-delete-csv`, {
            functionName: `${getAccountUniqueName(props.context)}-delete-csv`,
            entry: path.join(__dirname, '../../../app/backend/d_csv'),
            index: 'd_csv.py',
            runtime: Runtime.PYTHON_3_10,
            role: lambdaRole,
            environment: {
                'BUCKET_NAME': props.s3Stack!.bucket.bucketName,
            }
        })
    }
}