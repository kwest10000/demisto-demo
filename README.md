# demisto-demo 

This docker is a prebuilt container with this code installed

docker pull k1west2/demisto-api

# Build your own docker
Clone this repository into a directory and run these cmds from there.

docker login --username=yourusername  
docker build -t demisto-api .  
docker tag <build> your/dockerhub-repo:latest   
docker push your/dockerhub-repo   



