
docker build -f ./docker/kibana/Dockerfile -t herold961/ucsd-kibana ./docker/kibana
docker push herold961/ucsd-kibana

docker build -f ./docker/nas/Dockerfile -t herold961/ucsd-nas ./docker/nas
docker push herold961/ucsd-nas

docker build -f ./docker/workstation/Dockerfile -t herold961/ucsd-workstation ./docker/workstation
docker push herold961/ucsd-workstation
