import pytest
from comp import Compressor

with open('data/test2.txt', 'r') as f:
    content = f.read()

@pytest.fixture
def compress():
    return Compressor(content)

def test_character_frequencies(compress):
    assert compress.character_frequencies() == {'s': 1, 'x': 1, 'e': 2, 't': 4}