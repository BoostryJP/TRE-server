"""
Copyright BOOSTRY Co., Ltd.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.

You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

See the License for the specific language governing permissions and
limitations under the License.

SPDX-License-Identifier: Apache-2.0
"""

import random
import secrets
from datetime import datetime
from hashlib import sha512

from py_ecc.bls.ciphersuites import G2Basic
from py_ecc.bls.hash import xor
from py_ecc.bls.hash_to_curve import hash_to_G2
from py_ecc.fields import optimized_bls12_381_FQ12
from py_ecc.optimized_bls12_381 import G1, curve_order
from py_ecc.optimized_bls12_381.optimized_curve import multiply
from py_ecc.optimized_bls12_381.optimized_pairing import pairing

release_t = int(datetime(2025, 1, 1, 0, 0).timestamp())
print(f"\n<T> = {release_t}")

################################################
# [Time-Server-1] Generate master key
################################################
print("\n================== [Time-Server-1] Generate master key ==================\n")

# Generate master key
master_sk_1 = int.from_bytes(secrets.token_bytes(32)) % curve_order
print(f"<master_sk_1> = {master_sk_1}")

p_x_1 = multiply(G1, master_sk_1)
print(f"<P_X_1> = {p_x_1}")

################################################
# [Time-Server-2] Generate master key
################################################
print("\n================== [Time-Server-2] Generate master key ==================\n")

# Generate master key
master_sk_2 = int.from_bytes(secrets.token_bytes(32)) % curve_order
print(f"<master_sk_2> = {master_sk_2}")

p_x_2 = multiply(G1, master_sk_2)
print(f"<P_X_2> = {p_x_2}")

################################################
# [User-1] Encrypt message
################################################
print("\n================== [User-1] Encrypt message ==================\n")

user1_fragment = int.from_bytes(secrets.token_bytes(32)) % curve_order
user1_original_txt = user1_fragment.to_bytes(32).hex()
print(f"Text to encrypt = '{user1_original_txt}'")

r = int.from_bytes(secrets.token_bytes(32)) % curve_order
user1_c_1 = multiply(G1, r)
print(f"<C_1> = {user1_c_1}")

user1_c_2 = user1_original_txt.encode("utf-8")
for p_x in [p_x_1, p_x_2]:
    c_2_fq12: optimized_bls12_381_FQ12 = (
        pairing(
            hash_to_G2(str(release_t).encode(), G2Basic.DST, G2Basic.xmd_hash_function),
            p_x,
        )
        ** r
    )
    _hash = sha512()
    for _item in c_2_fq12.coeffs:
        _item = int(_item)
        _hash.update(_item.to_bytes(48))
    user1_c_2 = xor(user1_c_2, _hash.digest())

print(f"<C_2> = {user1_c_2}")

################################################
# [User-2] Encrypt message
################################################
print("\n================== [User-2] Encrypt message ==================\n")

user2_fragment = int.from_bytes(secrets.token_bytes(32)) % curve_order
user2_original_txt = user2_fragment.to_bytes(32).hex()
print(f"Text to encrypt = '{user2_original_txt}'")

r = int.from_bytes(secrets.token_bytes(32)) % curve_order
user2_c_1 = multiply(G1, r)
print(f"<C_1> = {user2_c_1}")

user2_c_2 = user2_original_txt.encode("utf-8")
for p_x in [p_x_1, p_x_2]:
    c_2_fq12: optimized_bls12_381_FQ12 = (
        pairing(
            hash_to_G2(str(release_t).encode(), G2Basic.DST, G2Basic.xmd_hash_function),
            p_x,
        )
        ** r
    )
    _hash = sha512()
    for _item in c_2_fq12.coeffs:
        _item = int(_item)
        _hash.update(_item.to_bytes(48))
    user2_c_2 = xor(user2_c_2, _hash.digest())

print(f"<C_2> = {user2_c_2}")

################################################
# [Time-Server-1] Generate time key
################################################
print("\n================== [Time-Server-1] Generate time key ==================\n")

q_x_1 = multiply(
    hash_to_G2(str(release_t).encode(), G2Basic.DST, G2Basic.xmd_hash_function),
    master_sk_1,
)
print(f"<Q_X_1> = {q_x_1}")

################################################
# [Time-Server-2] Generate time key
################################################
print("\n================== [Time-Server-2] Generate time key ==================\n")

q_x_2 = multiply(
    hash_to_G2(str(release_t).encode(), G2Basic.DST, G2Basic.xmd_hash_function),
    master_sk_2,
)
print(f"<Q_X_2> = {q_x_2}")

################################################
# [Lottery-Organizer] Decrypt message (User-1)
################################################
print(
    "\n================== [Lottery-Organizer] Decrypt message (User-1) ==================\n"
)

_decrypted_text = user1_c_2
for q_x in [q_x_1, q_x_2]:
    dec_key = pairing(q_x, user1_c_1)
    _hash = sha512()
    for _item in dec_key.coeffs:
        _item = int(_item)
        _hash.update(_item.to_bytes(48))
    _decrypted_text = xor(_decrypted_text, _hash.digest())

user1_decrypted_text = _decrypted_text.decode()
print(
    f"Decrypted text (from Q_X_1, Q_X_2) = '{user1_decrypted_text}' => {user1_original_txt == user1_decrypted_text}"
)

user1_decrypted_fragment = int(user1_decrypted_text, 16)

################################################
# [Lottery-Organizer] Decrypt message (User-2)
################################################
print(
    "\n================== [Lottery-Organizer] Decrypt message (User-2) ==================\n"
)

_decrypted_text = user2_c_2
for q_x in [q_x_1, q_x_2]:
    dec_key = pairing(q_x, user2_c_1)
    _hash = sha512()
    for _item in dec_key.coeffs:
        _item = int(_item)
        _hash.update(_item.to_bytes(48))
    _decrypted_text = xor(_decrypted_text, _hash.digest())

user2_decrypted_text = _decrypted_text.decode()
print(
    f"Decrypted text (from Q_X_1, Q_X_2) = '{user2_decrypted_text}' => {user2_original_txt == user2_decrypted_text}"
)

user2_decrypted_fragment = int(user2_decrypted_text, 16)

################################################
# [Lottery-Organizer] Derive seed
################################################
print("\n================== [Lottery-Organizer] Derive seed & RNG ==================\n")

_seed = (user1_decrypted_fragment * user2_decrypted_fragment) % curve_order
print(f"Seed = {_seed}")

random.seed(_seed)
print(f"Random number = {random.random()}")
