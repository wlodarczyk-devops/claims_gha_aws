# Configure GitHub OIDC Claims for AWS

This repository configures custom GitHub OIDC `sub` claims for a target repository.
Use it when you want stricter IAM trust policies for GitHub Actions in AWS.

## Prerequisites

- AWS IAM role with the required permissions
- OIDC provider configured in AWS (`token.actions.githubusercontent.com`)
- GitHub Personal Access Token with permissions to manage repository settings
- Target GitHub organization and repository names

## Example IAM Trust Policy

```json
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

## GitHub Action Usage

Run `.github/workflows/create_claims.yaml` manually and provide:

- `organisation`
- `repository`
- `gh-token` (a PAT that can update repository OIDC customization)
- `use-default` (`true` or `false`, defaults to `false`)
- `include-claim-keys` (comma-separated list used when `use-default=false`)

The workflow executes `claims.py` and updates OIDC claim customization for the selected repository.
