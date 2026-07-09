import matplotlib.pyplot as plt
import matplotlib.patches as patches


def draw_stadium():
    fig, ax = plt.subplots(figsize=(12,8))

    ax.set_xlim(0,100)
    ax.set_ylim(0,70)

    ax.set_facecolor("lightgreen")

    zones = {
        "A1":(10,55),
        "A2":(35,55),
        "B1":(60,55),
        "B2":(85,55),
        "C1":(10,15),
        "C2":(35,15),
        "D1":(60,15),
        "D2":(85,15)
    }

    for zone,(x,y) in zones.items():
        rect = patches.Rectangle(
            (x-5,y-5),
            10,
            10,
            linewidth=2,
            edgecolor="black",
            facecolor="white"
        )
        ax.add_patch(rect)

        ax.text(
            x,
            y,
            zone,
            fontsize=12,
            ha="center",
            va="center",
            weight="bold"
        )

    ax.set_title("FIFA World Cup 2026 Smart Stadium")

    plt.show()


if __name__ == "__main__":
    draw_stadium()