# sailpoint-assignment

# Run below command to build image from Docketfile

docker build -t assignment:latest .

# Run Below command to get a summary :

docker run assignment:latest -t '<GITHUB_TOKEN>' -u '<GITHUB_REPO_PULL_URL>' -f <FROM_GMAIL_ADDRESS> -r <TO_GMAIL_ADDRESS> -p <GMAIL_APP_PASSWORD>