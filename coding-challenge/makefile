build:
	docker build -t elevator:v1 .

install:
	helm install elevator-deploy elevator/ --values elevator/values.yaml

uninstall:
	helm uninstall elevator-deploy