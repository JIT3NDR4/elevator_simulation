#! /usr/bin/env python3
from pydantic import BaseModel


class OutsideButtonRequest(BaseModel):
    floor: int
    direction: str


class InsideButtonRequest(BaseModel):
    floor: int


class StateResponse(BaseModel):
    current_floor: int
    curr_direction: str
    is_moving: str


class ResponseModel(BaseModel):
    message: str
