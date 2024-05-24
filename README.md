# Automatic Repo Checks

This analysis tool checks all repositories of the VV Gitlab Group.
Please note that the following environment variables must be set in the .env file.
```
GITLAB_USER_NAME=USERNAME
GITLAB_PRIVATE_TOKEN=TOKEN
EXERCISE=Exercise01
```

On Windows: Open Docker Desktop and allow tcp://localhost:2375 to access Docker from Host Machine
![image](https://github.com/Thomas-Mildner/VV_AutomaticRepoChecks/assets/12685945/05fc1101-693b-4df6-acac-72067f7722a3)


## How to use
Check out the Repository and run the Docker Compose File with following Command
```
docker-compose up --build
```

Otherwise, use the prebuid Docker image with the following docker-compose file:
Please note: Create a suitable .env environment file.
```
services:
  ss24_abnahme:
    build:
      context: .
    image: vvthromildner/vv_abnahme_script:latest
    ports:
      - "9000:9000"
    env_file:
      - .env
    volumes:
      - ./results:/app/results

volumes:
  results:

```

## Results

The Result Files are stored in result/sose24results.
Each Repository will be a seperate Markdown AnalyseFile.md.

All Results are stored in a CSV Report.
