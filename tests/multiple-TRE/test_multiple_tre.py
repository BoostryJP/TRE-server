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


class TestMultipleTRE:
    def test_1(self):
        release_t = int(datetime(2025, 1, 1, 0, 0).timestamp())
        print(f"\n<T> = {release_t}")

        ################################################
        # [Time-Server-1] Generate key
        ################################################
        print("\n================== [Time-Server-1] ==================\n")

        # Generate master key
        master_sk_1 = int.from_bytes(secrets.token_bytes(32)) % curve_order
        print(f"<master_sk_1> = {master_sk_1}")

        p_x_1 = multiply(G1, master_sk_1)
        print(f"<P_X_1> = {p_x_1}")

        # Generate time key

        q_x_1 = multiply(
            hash_to_G2(str(release_t).encode(), G2Basic.DST, G2Basic.xmd_hash_function),
            master_sk_1,
        )
        print(f"<Q_X_1> = {q_x_1}")

        ################################################
        # [Time-Server-2] Generate key
        ################################################
        print("\n================== [Time-Server-2] ==================\n")

        # Generate master key
        master_sk_2 = int.from_bytes(secrets.token_bytes(32)) % curve_order
        print(f"<master_sk_2> = {master_sk_2}")

        p_x_2 = multiply(G1, master_sk_2)
        print(f"<P_X_2> = {p_x_2}")

        # Generate time key
        q_x_2 = multiply(
            hash_to_G2(str(release_t).encode(), G2Basic.DST, G2Basic.xmd_hash_function),
            master_sk_2,
        )
        print(f"<Q_X_2> = {q_x_2}")

        ################################################
        # [User] Encrypt message
        ################################################
        print("\n================== [User] Encrypt message ==================\n")

        original_txt = "test_text"
        print(f"Text to encrypt = '{original_txt}'")

        r = int.from_bytes(secrets.token_bytes(32)) % curve_order
        c_1 = multiply(G1, r)
        print(f"<C_1> = {c_1}")

        c_2 = original_txt.encode("utf-8")
        for p_x in [p_x_1, p_x_2]:
            c_2_fq12: optimized_bls12_381_FQ12 = (
                pairing(
                    hash_to_G2(
                        str(release_t).encode(), G2Basic.DST, G2Basic.xmd_hash_function
                    ),
                    p_x,
                )
                ** r
            )
            _hash = sha256()
            for _item in c_2_fq12.coeffs:
                _item = int(_item)
                _hash.update(_item.to_bytes(48))
            c_2 = xor(c_2, _hash.digest())

        print(f"<C_2> = {c_2}")

        ################################################
        # [User] Decrypt message
        ################################################
        print("\n================== [User] Decrypt message ==================\n")

        _decrypted_text = c_2
        for q_x in [q_x_1, q_x_2]:
            dec_key = pairing(q_x, c_1)
            _hash = sha256()
            for _item in dec_key.coeffs:
                _item = int(_item)
                _hash.update(_item.to_bytes(48))
            _decrypted_text = xor(_decrypted_text, _hash.digest())

        decrypted_text = _decrypted_text.decode()
        print(
            f"Decrypted text = '{decrypted_text}' => {original_txt == decrypted_text}"
        )

        assert original_txt == decrypted_text
