# Instance Management
Lambda function that runs every day at 11 PM to terminate any running EC2 instance and release any dedicated hosts

# Build and deploy
`sam validate`

`sam  build`

`sam deploy --stack-name <my-stack-name>`

# Delete
`sam delete --stack-name <my-stack-name>`

# Edit schedule
