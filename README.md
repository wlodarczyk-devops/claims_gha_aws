# Claims - In Progress of better 

If You want to automate your github workflows against AWS, You can authorize via OIDC.
To granulate authorization, you should make it trough AWS IAM Role.
AWS doesn't support out-of-box claims send from Github, so we need to make our own for specific repository.

## Prerequisites:

 - AWS IAM Role with necessary permissions
 - Setup OIDC in AWS
 - Github Personal Token
 - Github user/user_id and Organisation name

## Example IAM Role Trust Entity
```

    {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Federated": "arn:aws:iam::<ACCOUNT_ID>:oidc-provider/token.actions.githubusercontent.com"
            },
            "Action": "sts:AssumeRoleWithWebIdentity",
            "Condition": {
                "StringEquals": {
                    "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
                },
                "StringLike": {
                    "token.actions.githubusercontent.com:sub": "repo:<ORGANISATION>/<REPOSITORY>:*actor_id:<USERNAME_ID>:actor:<USERNAME>"
	                }
	            }
	        }
	    ]
    }

```
## Github Action
To use workflow, You just need provide information:

 - Organisation
 - Repository
 - Personal Github Token

After that, it will setup Claims for your repository.
