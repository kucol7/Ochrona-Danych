import sys, hashlib, hmac, os

def load_db(filepath):
    db = {}
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                login, iters, salt_hex, hash_hex = line.split(":")
                db[login] = (int(iters), bytes.fromhex(salt_hex), bytes.fromhex(hash_hex))
    return db

def weryfikuj(db, login, password):
    if login not in db:
        return False
    iters, salt, expected_hash = db[login]
    calc_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, iters, 32)
    return hmac.compare_digest(calc_hash, expected_hash)

db_file = sys.argv[1]
db = load_db(db_file)

print("ZADANIE 2.1")
print("anna, Kasztan-2026:", weryfikuj(db, "anna", "Kasztan-2026"))
print("anna, kasztan-2026:", weryfikuj(db, "anna", "kasztan-2026"))
print("piotr, Żółw na łące:", weryfikuj(db, "piotr", "Żółw na łące"))
print("kasia, Kasztan-2026:", weryfikuj(db, "kasia", "Kasztan-2026"))

def dodaj(login, password):
    salt = os.urandom(16)
    iters = 600000
    calc_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, iters, 32)
    return iters, salt, calc_hash





print("\nZADANIE 2.2")
iters1, salt1, hash1 = dodaj("test1", "KochamPolitechnikeWarszawska")
iters2, salt2, hash2 = dodaj("test2", "KochamPolitechnikeWarszawska")

print("Czy sole są takie same? ", salt1 == salt2)
print("Czy skróty są takie same? ", hash1 == hash2)

db_test = {
    "test1": (iters1, salt1, hash1),
    "test2": (iters2, salt2, hash2)
}
print("Weryfikacja test1:", weryfikuj(db_test, "test1", "KochamPolitechnikeWarszawska"))
print("Weryfikacja test2:", weryfikuj(db_test, "test2", "KochamPolitechnikeWarszawska"))


