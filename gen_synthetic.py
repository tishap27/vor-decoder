import argparse
import numpy as np

FS = 960_000


def write_iq(path, bearing_deg, seconds=10, snr_db=20, cfo_hz=300.0, seed=0):
    rng = np.random.default_rng(seed)
    th = np.radians(bearing_deg)
    w = 2 * np.pi * 30
    phi0 = rng.uniform(0, 2 * np.pi)
    sigma = np.sqrt(1.1 / 10 ** (snr_db / 10) / 2)
    with open(path, "wb") as f:
        for k in range(int(seconds)):
            t = (np.arange(FS) + k * FS) / FS
            var = 0.3 * np.cos(w * t - th)                                   # 30 Hz AM, phase = bearing
            ref = 0.3 * np.cos(2 * np.pi * 9960 * t + 16 * np.sin(w * t))    # 9960 Hz FM, 480 Hz dev
            ident = 0.1 * np.cos(2 * np.pi * 1020 * t) * (np.floor(t * 2) % 4 == 0)
            s = 1 + var + ref + ident
            sig = s * np.exp(1j * (2 * np.pi * cfo_hz * t + phi0))
            sig += sigma * (rng.standard_normal(FS) + 1j * rng.standard_normal(FS))
            raw = np.empty(2 * FS, dtype=np.uint8)
            raw[0::2] = np.clip(sig.real * 60 + 127.5, 0, 255)
            raw[1::2] = np.clip(sig.imag * 60 + 127.5, 0, 255)
            f.write(raw.tobytes())


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("bearing", type=float)
    ap.add_argument("-o", "--out", default="synthetic.iq")
    ap.add_argument("--seconds", type=int, default=10)
    ap.add_argument("--snr", type=float, default=20)
    ap.add_argument("--cfo", type=float, default=300)
    a = ap.parse_args()
    write_iq(a.out, a.bearing, a.seconds, a.snr, a.cfo)
    print(f"wrote {a.out} with bearing {a.bearing}")