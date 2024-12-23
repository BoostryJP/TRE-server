import secrets
from datetime import datetime
from hashlib import sha256

from py_ecc.bls.ciphersuites import G2Basic
from py_ecc.bls.hash import xor
from py_ecc.bls.hash_to_curve import hash_to_G2
from py_ecc.fields import optimized_bls12_381_FQ12
from py_ecc.optimized_bls12_381 import G1, curve_order
from py_ecc.optimized_bls12_381.optimized_curve import multiply
from py_ecc.optimized_bls12_381.optimized_pairing import pairing

################################################
# [Time-Server] Generate master key & pub key
################################################
master_sk = int.from_bytes(secrets.token_bytes(32)) % curve_order
print(f"<master_sk> = {master_sk}")

p_x = multiply(G1, master_sk)
print(f"<P_X> = {p_x}")

################################################
# [Time-Server] Generate time key
################################################
release_t = int(datetime(2025, 1, 1, 0, 0).timestamp())
print(f"<T> = {release_t}")

q_x = multiply(
    hash_to_G2(str(release_t).encode(), G2Basic.DST, G2Basic.xmd_hash_function),
    master_sk,
)
print(f"<Q_X> = {q_x}")

################################################
# [User] Encrypt message
################################################
original_txt = "test_text"
print(f"Text to encrypt = '{original_txt}'")

r = int.from_bytes(secrets.token_bytes(32)) % curve_order
c_1 = multiply(G1, r)
print(f"<C_1> = {c_1}")

c_2_fq12: optimized_bls12_381_FQ12 = (
    pairing(
        hash_to_G2(str(release_t).encode(), G2Basic.DST, G2Basic.xmd_hash_function), p_x
    )
    ** r
)
_hash = sha256()
for _item in c_2_fq12.coeffs:
    _item = int(_item)
    _hash.update(_item.to_bytes(48))
c_2 = xor(original_txt.encode("utf-8"), _hash.digest())
print(f"<C_2> = {c_2}")

################################################
# [User] Decrypt message
################################################
dec_key = pairing(q_x, c_1)
_hash = sha256()
for _item in dec_key.coeffs:
    _item = int(_item)
    _hash.update(_item.to_bytes(48))
print(xor(c_2, _hash.digest()))
decrypted_text = xor(c_2, _hash.digest()).decode()
print(f"Decrypted text = '{decrypted_text}' => {original_txt == decrypted_text}")
