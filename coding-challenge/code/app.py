#! /usr/bin/env python3

import uvicorn
import threading
from fastapi import FastAPI, Response, status

from models import models
from elevator.elevator import Elevator


elevator = Elevator()


def run_elevator_system():
    while True:
        elevator.handle_elevator_requests()


app = FastAPI()


@app.post('/outside')
def outside_button(request: models.OutsideButtonRequest, response: Response):
    floor, direction = request.floor, request.direction
    ok, message = elevator.handle_outside_button_press(floor, direction)
    if not ok:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return models.ResponseModel(message=message)
    else:
        response.status_code = status.HTTP_200_OK
        return models.ResponseModel(message=message)


@app.post('/inside')
def inside_button(request: models.InsideButtonRequest, response: Response):
    floor = request.floor
    ok, message = elevator.handle_inside_button_press(floor)
    if not ok:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return models.ResponseModel(message=message)
    else:
        response.status_code = status.HTTP_200_OK
        return models.ResponseModel(message=message)


@app.get('/state', response_model=models.StateResponse)
def elevator_state():
    return {
        'current_floor': elevator.current_floor,
        'curr_direction': elevator.curr_direction,
        'is_moving': 'Moving' if elevator.is_moving else 'Stopped'
    }


if __name__ == '__main__':
    thread = threading.Thread(target=run_elevator_system, daemon=True)
    thread.start()
    uvicorn.run(app, host='0.0.0.0', port=8000)
    # thread.join()
