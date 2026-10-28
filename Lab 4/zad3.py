import sys, hashlib

def generate_variant(lines, v):
    out = []
    for i, line in enumerate(lines):
        line_clean = line.rstrip(b"\r\n")
        if (v >> i) & 1:
            out.append(line_clean + b" \n")
        else:
            out.append(line_clean + b"\n")
    return b"".join(out)

def h24(data):
    return hashlib.sha256(data).hexdigest()[:6]

orig_file = "oryginal.txt"
mod_file = "zmieniony.txt"

with open(orig_file, "rb") as f:
    orig_lines = f.readlines()
with open(mod_file, "rb") as f:
    mod_lines = f.readlines()

orig_hashes = {}
for v in range(8192):
    var_bytes = generate_variant(orig_lines, v)
    orig_hashes[h24(var_bytes)] = v
found_pair = None
orig_v0_hash = h24(generate_variant(orig_lines, 0))
matches_with_v0 = 0
for v in range(8192):
    var_bytes = generate_variant(mod_lines, v)
    h = h24(var_bytes)
    if found_pair is None and h in orig_hashes:
        found_pair = (orig_hashes[h], v, h)
    if h == orig_v0_hash:
        matches_with_v0 += 1

print(f"Znaleziona para: v_oryg={found_pair[0]}, v_zmien={found_pair[1]}, h24={found_pair[2]}")
print(f"Liczba wariantow mających h24 równy h24 niezmienionego oryginału: {matches_with_v0}")
