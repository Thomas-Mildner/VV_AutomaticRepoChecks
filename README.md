# Automatic Repo Checks

This analysis tool checks all repositories of the VV Gitlab Group.
Please note that the following environment variables must be set in the .env file.
```
GITLAB_USER_NAME=USERNAME
GITLAB_PRIVATE_TOKEN=TOKEN
EXERCISE=Exercise01
```

## How to use
Check out the Repository and run the Docker Compose File with following Command
```
docker-compose up --build
```

## Results

The Result Files are stored in result/sose24results.
Each Repository will be a seperate Markdown AnalyseFile.md.

All Results are stored in a CSV Report.
