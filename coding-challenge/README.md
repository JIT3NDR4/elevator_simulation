# ELEVATOR

Hi! Please follow the Instructions provided below to deploy the elevator.

## Prerequisites

- Docker (Used v27.2.0)
- Kubernetes (Used v1.30.2)
- Helm (Used v3.15.4)

## Installation

- Run the below script and it will take care of building the docker image and installing the helm chart

```
$ bash deploy.sh
```

## Accessing the APIs

- The APIs to push buttons and check the state of the elevator can be accessed at:
[http://localhost:30456/docs](http://localhost:30456/docs)
- If you want to use a different nodePort then you can change it in the elevator/values.yaml file

## Accessing the Logs

- If you have a kubernetes dashboard enabled then you can view the logs of elevator pod from the dashboard.
- Else if you do not have the dashboard enabled then you can follow the below steps
1. Get the elevator pods name
```
$ kubectl get pods
NAME                                   READY   STATUS    RESTARTS   AGE
elevator-deployment-6474688766-zbv58   1/1     Running   0          71s
```
2. Follow the logs of the pod
```
$ kubectl logs -f elevator-deployment-6474688766-zbv58
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     192.168.65.3:63046 - "GET /docs HTTP/1.1" 200 OK
INFO:     192.168.65.3:63046 - "GET /openapi.json HTTP/1.1" 200 OK
INFO:     192.168.65.3:55038 - "POST /outside HTTP/1.1" 200 OK
INFO:root:Elevator at floor -> 2, Direction -> UP
INFO:root:Elevator at floor -> 3, Direction -> UP
INFO:root:Elevator at floor -> 4, Direction -> UP
INFO:root:Elevator at floor -> 5, Direction -> UP
INFO:root:Elevator stopped at floor -> 5

```

## Uninstall the Helm Chart

- To uninstall the elevator helm chart, run the below command.
```
$ make uninstall
```

### Contact
---
Email: jitendra_vr@hotmail.com
Happy Coding! ✌🏻