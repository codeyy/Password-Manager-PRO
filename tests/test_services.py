import pytest

from app.services.strength_eval import strength


@pytest.fixture
def weak_password():
    return strength("password")

def test_strength_ordering():
    weak = strength("password")
    moderate = strength("dumb-horse-")
    strong = strength("9rT$pL@m2$b3Q")
    very_strong = strength("k&9$bZ!m8N@pL7qRz")

    assert moderate[0] > weak[0]
    assert strong[0] > moderate[0]
    assert very_strong[0] > strong[0]

@pytest.mark.parametrize("password", [
    "password",
    "123456789",
    "sunshine"
])
def test_strength_weak(password, weak_password):

    current = strength(password)
    
    assert current[0] >= weak_password[0]
    assert current[1] >= weak_password[1]


@pytest.mark.parametrize("password", [
    "dumb-horse-",
    "battery-dead--",
    "pale/bluesky"
])
def test_strength_moderate(password, weak_password):

    current = strength(password)
    
    assert current[0] > weak_password[0]
    assert current[1] > weak_password[1]


@pytest.mark.parametrize("password", [
    "9rT$pL@m2$b3Q",
    "p@ssw0rd!4u7a&x",
    "vL2weQdaxa9zRv"
])
def test_strength_strong(password, weak_password):

    current = strength(password)
    
    assert current[0] > weak_password[0]
    assert current[1] > weak_password[1]


@pytest.mark.parametrize("password", [
    "k&9$bZ!m8N@pL7qRz",
    "correct-horse-battery-staple",
    "sky#Blue#89#Tdree"
])
def test_strength_veryStrong(password, weak_password):

    current = strength(password)
    
    assert current[0] > weak_password[0]
    assert current[1] > weak_password[1]




def test_empty_password():
    entropy, _ = strength("")
    assert entropy == 0

def test_single_character():
    entropy, _ = strength("a")
    assert entropy >= 0

def test_long_password():
    entropy, _ = strength("a" * 100)
    assert entropy > 0