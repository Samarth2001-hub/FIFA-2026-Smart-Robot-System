import random

class Robot:

    def __init__(self, robot_id, name, zone, battery):
        self.robot_id = robot_id
        self.name = name
        self.zone = zone
        self.battery = battery

    def move(self, zones):

        new_zone = random.choice(zones)

        while new_zone == self.zone:
            new_zone = random.choice(zones)

        self.zone = new_zone

        self.battery -= random.randint(1,3)

        if self.battery < 0:
            self.battery = 0

    def __str__(self):

        return f"{self.name} -> {self.zone} | Battery: {self.battery}%"