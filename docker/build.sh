
if [ -z "$ELASTIC_PASSWORD" ] ; then
  echo "Env variable ELASTIC_PASSWORD required" 1>&2
  exit 64
fi

docker build --no-cache -f ./docker/kibana/Dockerfile -t herold961/ucsd-kibana ./docker/kibana
docker push herold961/ucsd-kibana

docker build --no-cache -f ./docker/nas/Dockerfile -t herold961/ucsd-nas ./docker/nas --build-arg ELASTIC_PASSWORD=$ELASTIC_PASSWORD --build-arg CERTS_DIR=$CERTS_DIR
docker push herold961/ucsd-nas

docker build --no-cache -f ./docker/workstation/Dockerfile -t herold961/ucsd-workstation ./docker/workstation --build-arg ELASTIC_PASSWORD=$ELASTIC_PASSWORD --build-arg CERTS_DIR=$CERTS_DIR
docker push herold961/ucsd-workstation
