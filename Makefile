
all-images: kibana-image nas-image workstation-image
	
kibana-image:
  docker build -f docker/kibana/Dockerfile -t herold961/ucsd-kibana
	docker push herold961/ucsd-kibana

nas-image:
  docker build -f docker/nas/Dockerfile -t herold961/ucsd-nas
	docker push herold961/ucsd-nas

workstation-image:
  docker build -f docker/workstation/Dockerfile -t herold961/ucsd-workstation
	docker push herold961/ucsd-workstation
  
