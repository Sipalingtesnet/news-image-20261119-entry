import sys
import shutil
import hashlib
import os

def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copy(src, dst)
    
    with open(src, "rb") as f:
        h_src = hashlib.sha256(f.read()).hexdigest()
    with open(dst, "rb") as f:
        h_dst = hashlib.sha256(f.read()).hexdigest()
        
    print(f"sha256: {h_dst}")
    if h_src != h_dst:
        print("Error: sha256 mismatch between source and copied entry.png", file=sys.stderr)
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
