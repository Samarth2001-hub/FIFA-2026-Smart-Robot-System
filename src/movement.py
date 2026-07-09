import pandas as pd
import random
import time

zones = ["A1","A2","B1","B2","C1","C2","D1","D2"]

while True:

    df = pd.read_csv("data/robot_data.csv")

    for i in range(len(df)):

        # Random new zone
        df.loc[i, "Current_Zone"] = random.choice(zones)

        # Random battery drain
        battery = df.loc[i, "Battery"] - random.randint(0,2)

        if battery < 20:
            battery = 100

        df.loc[i, "Battery"] = battery

        # Status update
        if battery < 25:
            df.loc[i,"Status"] = "Charging"
        else:
            df.loc[i,"Status"] = random.choice(
                ["Active","Active","Idle"]
            )

    df.to_csv("data/robot_data.csv", index=False)

    print("Robot positions updated...")

    time.sleep(5)