import pytest

from SuperHelper.Core.Utils import BitOps, Cryptographer, TypeCheck


class TestBitOps:
    @staticmethod
    @pytest.fixture()
    def a():
        return 0b10101010

    @staticmethod
    def test_is_bit_set(a):
        assert BitOps.is_bit_set(a, 1)
        assert BitOps.is_bit_set(a, 3)
        assert not BitOps.is_bit_set(a, 2)
        assert not BitOps.is_bit_set(a, 16)

    @staticmethod
    def test_set_bit(a):
        assert BitOps.set_bit(a, 1) == a
        assert BitOps.set_bit(a, 0) == 0b10101011
        assert BitOps.set_bit(a, 5) == a
        assert BitOps.set_bit(a, 4) == 0b10111010

    @staticmethod
    def test_unset_bit(a):
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


def test_ensure_int():
    assert TypeCheck.ensure_int(12345) is None
    assert TypeCheck.ensure_int(12341234123412341234) is None
    with pytest.raises(TypeError):
        TypeCheck.ensure_int("12345")
    with pytest.raises(TypeError):
        TypeCheck.ensure_int(12345.0)


def test_ensure_custom():
    class Test:
        pass

    test = Test()
    assert TypeCheck.ensure_custom(Test, test) is None
    with pytest.raises(TypeError):
        TypeCheck.ensure_custom(Test, object())


def test_ensure_float():
    assert TypeCheck.ensure_float(12345.0) is None
    assert TypeCheck.ensure_float(123412341234123445.0000000000000000001) is None
    with pytest.raises(TypeError):
        TypeCheck.ensure_float(8j)
    with pytest.raises(TypeError):
        TypeCheck.ensure_float(12345)


def test_ensure_complex():
    assert TypeCheck.ensure_complex(12 + 5j) is None
    assert TypeCheck.ensure_complex(135453123123 + 0.00000000000000000001j) is None
    with pytest.raises(TypeError):
        TypeCheck.ensure_complex(8)
    with pytest.raises(TypeError):
        TypeCheck.ensure_complex("1234s")


def test_ensure_str():
    assert TypeCheck.ensure_str("") is None
    assert TypeCheck.ensure_str(r"1asm") is None
    with pytest.raises(TypeError):
        TypeCheck.ensure_str(8)
    with pytest.raises(TypeError):
        TypeCheck.ensure_str(["string"])


def test_ensure_bytes():
    assert TypeCheck.ensure_bytes(b"3123") is None
    assert TypeCheck.ensure_bytes(bytes(132423)) is None
    assert TypeCheck.ensure_bytes("n".encode()) is None
    with pytest.raises(TypeError):
        TypeCheck.ensure_bytes(8)
    with pytest.raises(TypeError):
        TypeCheck.ensure_bytes(["string"])


def test_ensure_bytearray():
    assert TypeCheck.ensure_bytearray(bytearray(5)) is None
    assert TypeCheck.ensure_bytearray(bytearray("41243", "utf-8")) is None
    with pytest.raises(TypeError):
        TypeCheck.ensure_bytearray(b"1234")
    with pytest.raises(TypeError):
        TypeCheck.ensure_bytearray(["string"])


def test_ensure_list():
    assert TypeCheck.ensure_list([]) is None
    assert TypeCheck.ensure_list("".split()) is None
    with pytest.raises(TypeError):
        TypeCheck.ensure_list(8)
    with pytest.raises(TypeError):
        TypeCheck.ensure_list("string")


def test_ensure_tuple():
    assert TypeCheck.ensure_tuple(tuple()) is None
    assert TypeCheck.ensure_tuple((5,)) is None
    with pytest.raises(TypeError):
        TypeCheck.ensure_tuple(8)
    with pytest.raises(TypeError):
        TypeCheck.ensure_tuple("string".split())


def test_ensure_set():
    assert TypeCheck.ensure_set(set()) is None
    assert TypeCheck.ensure_set({1}) is None
    with pytest.raises(TypeError):
        TypeCheck.ensure_set(8)
    with pytest.raises(TypeError):
        TypeCheck.ensure_set("string".split())


def test_ensure_dict():
    assert TypeCheck.ensure_dict(dict()) is None
    assert TypeCheck.ensure_dict({1: 5, "123": -8}) is None
    with pytest.raises(TypeError):
        TypeCheck.ensure_dict({1})
    with pytest.raises(TypeError):
        TypeCheck.ensure_dict("string".split())


def test_ensure_frozenset():
    assert TypeCheck.ensure_frozenset(frozenset(range(10))) is None
    with pytest.raises(TypeError):
        TypeCheck.ensure_frozenset({1})
    with pytest.raises(TypeError):
        TypeCheck.ensure_frozenset("string".split())


def test_ensure_generator():
    def a():
        yield 1

    a = a()
    assert TypeCheck.ensure_generator(a) is None
    with pytest.raises(TypeError):
        TypeCheck.ensure_generator({1})
    with pytest.raises(TypeError):
        TypeCheck.ensure_generator("string".split())


def test_ensure_memoryview():
    assert TypeCheck.ensure_memoryview(memoryview("a".encode())) is None
    with pytest.raises(TypeError):
        TypeCheck.ensure_memoryview({1})
    with pytest.raises(TypeError):
        TypeCheck.ensure_memoryview("string".split())


def test_ensure_function():
    assert TypeCheck.ensure_function(lambda: None) is None
    assert TypeCheck.ensure_function(test_ensure_dict) is None
    with pytest.raises(TypeError):
        TypeCheck.ensure_function({1})
    with pytest.raises(TypeError):
        TypeCheck.ensure_function("string".split())
