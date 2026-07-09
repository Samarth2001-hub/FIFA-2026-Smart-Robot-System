from src.robot import Robot
import time

zones = [
    "A1","A2","B1","B2",
    "C1","C2","D1","D2"
]

robots = [

    Robot("R001","Atlas","A1",98),
    Robot("R002","Bolt","A2",96),
    Robot("R003","Nova","B1",92),
    Robot("R004","Echo","B2",90),
    Robot("R005","Orion","C1",95)

]

for i in range(10):

    print(f"\n========= STEP {i+1} =========")

    for robot in robots:

        robot.move(zones)

        print(robot)

    time.sleep(1)