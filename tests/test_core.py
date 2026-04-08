import pytest
import random
import string


@pytest.fixture()
def master_password():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=12))

def test_kdf_and_salt_generation(master_password):
    from app.core.security import derive_key, gen_salt
    salt = gen_salt()
    assert isinstance(salt, bytes)

    key = derive_key(master_password, salt)
    assert isinstance(key, bytes)



def test_encryption_and_decryption(master_password):
    from app.core.security import encrypt_data, decrypt_data, derive_key, gen_salt

    salt = gen_salt()
    key = derive_key(master_password, salt)
    
    plain = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

    cipher = encrypt_data(key, plain)
    assert isinstance(cipher, bytes)
    decrypted = decrypt_data(key, cipher)
    assert isinstance(decrypted, str)



def test_decryption_with_wrong_password(master_password):
    from app.core.security import encrypt_data, decrypt_data, derive_key, gen_salt

    salt = gen_salt()
    key = derive_key(master_password, salt)

    plain = "secret123"
    cipher = encrypt_data(key, plain)

    wrong_key = derive_key("wrongpassword", salt)

    with pytest.raises(Exception):
        decrypt_data(wrong_key, cipher)



def test_tampered_cipher_fails(master_password):
    from app.core.security import encrypt_data, decrypt_data, derive_key, gen_salt

    salt = gen_salt()
    key = derive_key(master_password, salt)

    cipher = encrypt_data(key, "hello")

    tampered = cipher[:-1] + b"x"

    with pytest.raises(Exception):
        decrypt_data(key, tampered)



def test_kdf_deterministic(master_password):
    from app.core.security import derive_key, gen_salt

    salt = gen_salt()

    key1 = derive_key(master_password, salt)
    key2 = derive_key(master_password, salt)

    assert key1 == key2



def test_salt_uniqueness():
    from app.core.security import gen_salt

    salt1 = gen_salt()
    salt2 = gen_salt()

    assert salt1 != salt2



