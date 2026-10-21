from gen_synthetic import write_iq
from vor_decode import load_iq, decode


def angdiff(a, b):
    return abs((a - b + 180) % 360 - 180)


if __name__ == "__main__":
    ok_all = True
    for b in [0, 45, 90, 135, 180, 270, 359]:
        write_iq("t.iq", b, seconds=5, snr_db=20)
        _, mean, spread = decode(load_iq("t.iq"))
        ok = angdiff(mean, b) < 2
        ok_all &= ok
        print(f"true {b:3d}  decoded {mean:6.1f}  spread {spread:4.1f}  {'PASS' if ok else 'FAIL'}")
    print("\nALL PASS" if ok_all else "\nSOME FAILED")