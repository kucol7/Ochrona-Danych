import sys, hashlib, os

def get_sha256(filepath):
    with open(filepath, "rb") as f:
        return hashlib.sha256(f.read()).digest()

def check_sums(sums_file):
    base_dir = os.path.dirname(sums_file)
    with open(sums_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            expected_hex, rel_path = line.split("  ", 1)
            full_path = os.path.join(base_dir, rel_path)
            
            if not os.path.exists(full_path):
                print(f"{rel_path}: BRAK")
            else:
                actual_hex = hashlib.sha256(open(full_path, "rb").read()).hexdigest()
                if actual_hex == expected_hex:
                    print(f"{rel_path}: OK")
                else:
                    print(f"{rel_path}: BŁĄD")

                    
t1 = b"Ala ma kota."
t2 = b"Ola ma kota."
h1 = hashlib.sha256(t1).digest()
h2 = hashlib.sha256(t2).digest()

diff_bits = sum(bin(b1 ^ b2).count('1') for b1, b2 in zip(h1, h2))

if len(sys.argv) > 1:
    check_sums(sys.argv[1])

print(f"Liczba roznic w bitach: {diff_bits}")
