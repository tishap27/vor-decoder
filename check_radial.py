import math
import sys

VOR = (45 + 26/60 + 30/3600, -(75 + 53/60 + 49/3600))  # YOW 114.6
VAR_W = 14  # approx magnetic variation, check a current chart


def expected(lat, lon):
    p1, l1 = map(math.radians, VOR)
    p2, l2 = map(math.radians, (lat, lon))
    dl = l2 - l1
    y = math.sin(dl) * math.cos(p2)
    x = math.cos(p1) * math.sin(p2) - math.sin(p1) * math.cos(p2) * math.cos(dl)
    true = math.degrees(math.atan2(y, x)) % 360
    a = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    nm = 2 * 3440.065 * math.asin(math.sqrt(a))
    return true, (true + VAR_W) % 360, nm


if __name__ == "__main__":
    t, m, nm = expected(float(sys.argv[1]), float(sys.argv[2]))
    print(f"true {t:.0f}  magnetic radial {m:.0f}  distance {nm:.1f} NM")