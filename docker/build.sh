
docker build -f ./kibana/Dockerfile -t herold961/ucsd-kibana ./kibana
docker push herold961/ucsd-kibana

docker build -f ./nas/Dockerfile -t herold961/ucsd-nas ./nas
docker push herold961/ucsd-nas

docker build -f ./workstation/Dockerfile -t herold961/ucsd-workstation ./workstation
docker push herold961/ucsd-workstation
