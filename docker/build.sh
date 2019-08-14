
source .env

if [ -z "$ELASTIC_PASSWORD" ] ; then
  echo "Add environment variable ELASTIC_PASSWORD='{password}' to .env file in current directory" 1>&2
  exit 64
fi

docker build --no-cache -f ./docker/kibana/Dockerfile -t herold961/ucsd-kibana ./docker/kibana
docker push herold961/ucsd-kibana

docker build --no-cache -f ./docker/nas/Dockerfile -t herold961/ucsd-nas ./docker/nas --build-arg ELASTIC_PASSWORD=$ELASTIC_PASSWORD
docker push herold961/ucsd-nas

docker build --no-cache -f ./docker/workstation1/Dockerfile -t herold961/ucsd-workstation1 ./docker/workstation1 --build-arg ELASTIC_PASSWORD=$ELASTIC_PASSWORD
docker push herold961/ucsd-workstation1

docker build --no-cache -f ./docker/workstation2/Dockerfile -t herold961/ucsd-workstation2 ./docker/workstation2 --build-arg ELASTIC_PASSWORD=$ELASTIC_PASSWORD
docker push herold961/ucsd-workstation2

docker build --no-cache -f ./docker/jupyter/Dockerfile -t herold961/ucsd-jupyter ./docker/jupyter
docker push herold961/ucsd-jupyter
