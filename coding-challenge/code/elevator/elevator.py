#! /usr/bin/env python3

import time
import logging

logging.basicConfig(level=logging.INFO)


class Elevator:
    # Using Singleton Pattern to Make sure that only a single instance of the Elevator is created
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Elevator, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.current_floor = 1
        self.curr_direction = 'IDLE'
        self.is_moving = False
        self.up_requests = set()
        self.down_requests = set()
        self.inside_requests = set()

    def log(self, message):
        logging.info(message)

    def handle_inside_button_press(self, floor):
        # Handling Invalid floor Inputs
        if floor < 1 or floor > 6:
            msg = f'Invalid Floor {floor}'
            return False, msg
        self.inside_requests.add(floor)
        msg = f'Successfully pressed inside Button for floor {floor}'
        return True, msg

    def handle_outside_button_press(self, floor, direction):
        # Handling Invalid floor Inputs
        if floor < 1 or floor > 6:
            msg = f'Invalid Floor {floor}'
            return False, msg
         # Handling Invalid direction Inputs
        if direction not in ['UP', 'up', 'Up', 'DOWN', 'Down', 'down']:
            msg = f'Invalid Direction {direction}'
            return False, msg
        if direction in ['UP', 'up', 'Up']:
            if floor == 6:
                msg = f'Invalid Direction {direction} for floor 6'
                return False, msg
            self.up_requests.add(floor)
        elif direction in ['DOWN', 'Down', 'down']:
            if floor == 1:
                msg = f'Invalid Direction {direction} for floor 1'
                return False, msg
        self.down_requests.add(floor)
        msg = f'Successfully pressed {direction} Button on floor {floor}'
        return True, msg

    def handle_elevator_requests(self):
        if not self.inside_requests and not self.up_requests and not self.down_requests:
            self.curr_direction = 'IDLE'
            return

        if self.curr_direction == 'IDLE' and (self.inside_requests or self.up_requests or self.down_requests):
            self.get_direction()

        if self.curr_direction == 'UP':
            self.move_up()

        elif self.curr_direction == 'DOWN':
            self.move_down()

    def get_direction(self):
        if self.inside_requests or self.up_requests or self.down_requests:
            if (self.curr_direction == 'IDLE') and \
            any(floor > self.current_floor for floor in self.inside_requests.union(self.up_requests, self.down_requests)):
                self.curr_direction = 'UP'
            elif (self.curr_direction == 'IDLE') and \
                  any(floor < self.current_floor for floor in self.inside_requests.union(self.up_requests, self.down_requests)):
                self.curr_direction = 'DOWN'
            elif any(floor > self.current_floor for floor in self.inside_requests.union(self.up_requests)):
                self.curr_direction = 'UP'
            elif any(floor < self.current_floor for floor in self.inside_requests.union(self.down_requests)):
                self.curr_direction = 'DOWN'

    def move_up(self):
        while self.curr_direction == 'UP':
            # Prioritizing inside requests first
            next_floors = sorted(
                floor for floor in self.inside_requests if floor >= self.current_floor)
            # Prioritizing requests in the same direction (UP)
            if not next_floors:
                next_floors = sorted(
                    floor for floor in self.up_requests if floor >= self.current_floor)

            if not next_floors:
                # If no UP requests, then handle DOWN requests that are above the current floor
                next_floors = sorted(
                    (floor for floor in self.down_requests if floor > self.current_floor), reverse=True)

            if not next_floors:
                break

            for floor in next_floors:
                if floor == 6 and self.curr_direction == 'UP':
                    self.travel_to_floor(floor)
                    self.inside_requests.discard(floor)
                    self.down_requests.discard(floor)
                    self.curr_direction = 'DOWN'
                    break
                self.travel_to_floor(floor)
                self.inside_requests.discard(floor)
                self.up_requests.discard(floor)
                self.down_requests.discard(floor)
            self.check_direction_change()

    def move_down(self):
        while self.curr_direction == 'DOWN':
            # Prioritizing inside requests first
            next_floors = sorted(
                (floor for floor in self.inside_requests if floor <= self.current_floor), reverse=True)
            # Prioritizing requests in the same direction (DOWN)
            if not next_floors:
                next_floors = sorted(
                    (floor for floor in self.down_requests if floor <= self.current_floor), reverse=True)

            if not next_floors:
                # If no DOWN requests, then handle UP requests that are below the current floor
                next_floors = sorted(
                    floor for floor in self.up_requests if floor < self.current_floor)

            if not next_floors:
                break

            for floor in next_floors:
                if floor == 1 and self.curr_direction == 'DOWN':
                    self.travel_to_floor(floor)
                    self.inside_requests.discard(floor)
                    self.up_requests.discard(floor)
                    self.curr_direction = 'UP'
                    break
                self.travel_to_floor(floor)
                self.inside_requests.discard(floor)
                self.down_requests.discard(floor)
                self.up_requests.discard(floor)
            self.check_direction_change()

    def travel_to_floor(self, floor):
        while self.current_floor != floor:
            time.sleep(5)
            if self.current_floor < floor:
                self.is_moving = True
                self.current_floor += 1
                self.log(
                    f"Elevator at floor -> {self.current_floor}, Direction -> {self.curr_direction}")
            else:
                self.is_moving = True
                self.current_floor -= 1
                self.log(
                    f"Elevator at floor -> {self.current_floor}, Direction -> {self.curr_direction}")

            # Checking if there are any compatible floors in the current direction
            if self.curr_direction == 'UP':
                if (self.current_floor != floor) and (self.current_floor in self.inside_requests or self.current_floor in self.up_requests):
                    self.inside_requests.discard(self.current_floor)
                    self.up_requests.discard(self.current_floor)
                    self.is_moving = False
                    self.log(
                        f"Elevator stopped at floor -> {self.current_floor}")
                    time.sleep(10)
            elif self.curr_direction == 'DOWN':
                if (self.current_floor != floor) and (self.current_floor in self.inside_requests or self.curr_direction in self.down_requests):
                    self.inside_requests.discard(self.current_floor)
                    self.down_requests.discard(self.current_floor)
                    self.is_moving = False
                    self.log(
                        f"Elevator stopped at floor -> {self.current_floor}")
                    time.sleep(10)
        self.is_moving = False
        self.log(f"Elevator stopped at floor -> {self.current_floor}")
        time.sleep(10)

    def check_direction_change(self):
        if not self.inside_requests or not self.up_requests or not self.down_requests:
            self.curr_direction = 'IDLE'
        else:
            self.get_direction()

    def get_elevator_state(self):
        return {
            'current_direction': self.curr_direction,
            'current_floor': self.current_floor,
            'is_moving': self.is_moving
        }
