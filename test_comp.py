import pytest
from comp import Compressor

@pytest.fixture
def compress():
    with open('data/test2.txt', 'r') as f:
        content = f.read()
    return Compressor(content)

def test_encode_text(compress):
    curr_node = compress.build_tree()
    compress.prefix_code(curr_node)
    result = compress.encode_text()
    assert isinstance(result, bytes)