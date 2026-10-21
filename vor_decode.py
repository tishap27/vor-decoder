import sys
import numpy as np
from scipy import signal

FS_IN = 960_000
FS = FS_IN // 20  # 48 kHz after decimation


def load_iq(path):
    raw = np.fromfile(path, dtype=np.uint8).astype(np.float32) - 127.5
    return raw[0::2] + 1j * raw[1::2]


def decode(iq):
    # AM demod, normalised so 30 Hz depth reads as a fraction of carrier
    am = np.abs(iq)
    am = am / am.mean() - 1
    am = signal.decimate(am, 5, ftype="fir", zero_phase=True)
    am = signal.decimate(am, 4, ftype="fir", zero_phase=True)

    # Reference: 9960 Hz subcarrier -> FM demod -> 30 Hz tone
    sos = signal.butter(4, [9960 - 1000, 9960 + 1000], btype="bandpass", fs=FS, output="sos")
    sub = signal.sosfiltfilt(sos, am)
    ph = np.unwrap(np.angle(signal.hilbert(sub)))
    inf = np.diff(ph) * FS / (2 * np.pi)
    inf = np.append(inf, inf[-1])
    ref = inf - inf.mean()

    def lockin(x, f0=30.0):
        t = np.arange(len(x)) / FS
        return np.sum(x * np.exp(-2j * np.pi * f0 * t))

    win = FS  # 1 s = exactly 30 cycles
    rows = []
    for i in range(len(am) // win):
        s = slice(i * win, (i + 1) * win)
        zv, zr = lockin(am[s]), lockin(ref[s])
        brg = np.degrees(np.angle(zr * np.conj(zv))) % 360
        rows.append((brg, 2 * abs(zv) / win, 2 * abs(zr) / win))

    r = np.radians([x[0] for x in rows])
    c = np.mean(np.exp(1j * r))
    mean = np.degrees(np.angle(c)) % 360
    spread = np.degrees(np.sqrt(-2 * np.log(abs(c))))
    return rows, mean, spread


if __name__ == "__main__":
    rows, mean, spread = decode(load_iq(sys.argv[1]))
    for i, (b, depth, dev) in enumerate(rows):
        print(f"{i:2d}s  bearing {b:6.1f}  30Hz AM depth {depth:.2f}  FM dev {dev:5.0f} Hz")
    print(f"\nMEAN RADIAL: {mean:.1f}   (spread {spread:.1f} deg)")