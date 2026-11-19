import sys
import shutil
import hashlib
import os

def main():
    out = "/output"
    for arg in sys.argv[1:]:
        if arg.startswith("DIR="):
            out = arg.split("=", 1)[1]
    os.makedirs(out, exist_ok=True)
    shutil.copy("entry.png", os.path.join(out, "entry.png"))
    with open("entry.png", "rb") as f:
        print("sha256:", hashlib.sha256(f.read()).hexdigest())

if __name__ == "__main__":
    main()
