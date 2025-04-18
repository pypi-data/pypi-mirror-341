import os
import pytest
from PIL import Image
from captcha_library.module import generate_captcha

@pytest.fixture
def captcha_file(tmp_path):
    filename = tmp_path / "test_captcha.png"
    captcha_text = generate_captcha(filename)
    return filename, captcha_text

def test_captcha_generation(captcha_file):
    filename, captcha_text = captcha_file
    
    assert os.path.exists(filename)
    
    with Image.open(filename) as img:
        assert img.size == (300, 200)
    
    assert len(captcha_text) == 6
    
    forbidden_chars = {'0', 'O', '1', 'I'}
    assert not any(char in captcha_text for char in forbidden_chars)