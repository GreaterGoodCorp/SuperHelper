from SuperHelper.Core.Utils import BitOps, Cryptographer
import pytest


def test_bit_ops():
    a: int = 0b10101010
    assert BitOps.is_bit_set(a, 1)
    assert BitOps.is_bit_set(a, 3)
    assert not BitOps.is_bit_set(a, 2)
    assert not BitOps.is_bit_set(a, 16)

    assert BitOps.set_bit(a, 1) == a
    assert BitOps.set_bit(a, 0) == 0b10101011
    assert BitOps.set_bit(a, 5) == a
    assert BitOps.set_bit(a, 4) == 0b10111010

    assert BitOps.unset_bit(a, 0) == a
    assert BitOps.unset_bit(a, 1) == 0b10101000
    assert BitOps.unset_bit(a, 4) == a
    assert BitOps.unset_bit(a, 5) == 0b10001010


def test_cryptographer():
    salt = Cryptographer.make_salt()
    assert len(salt) == 16
    assert Cryptographer.encode_salt(salt) is not None
    assert Cryptographer.decode_salt(Cryptographer.encode_salt(salt)) == salt

    true_key = "test_key"
    false_key = "t3st_k3y"
    assert Cryptographer.make_kdf(salt)
    assert Cryptographer.make_kdf(salt).derive(true_key.encode()) is not None
    assert Cryptographer.make_kdf(salt).derive(false_key.encode()) is not None

    data = "data"
    crypto = Cryptographer.make_encrypter(true_key)
    assert crypto.encrypt(data.encode()) is not None

    encrypted_data = crypto.encrypt(data.encode())
    crypto.is_encrypt = False
    assert crypto.decrypt(encrypted_data) == data.encode()
    with pytest.raises(ValueError):
        crypto.is_encrypt = True
        assert crypto.decrypt(encrypted_data) == data.encode()
