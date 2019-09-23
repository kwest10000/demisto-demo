# demisto-demo 

Use this docker to use a prebuilt container with this code installed

# Run existing docker
docker pull k1west2/demisto-api

# Build your own docker
docker login --username=yourusername
docker build -t demisto-api .
docker tag <build> your/dockerhub-repo:latest
docker push your/dockerhub-repo

