import os
import tempfile
import base64
import pytest
import sys
from pyfunc2 import all_lasts, email_update, img_to_base64, lasts, convert_char, to_lower_case

# --- all_lasts ---
def test_all_lasts_basic(monkeypatch):
    import pyfunc2.all_lasts
    def dummy_lasts(path, lines, emails, ftps, storage_root):
        return [f"image_{lines}"]
    def dummy_get_email_path(target, storage_root):
        return "/tmp"
    monkeypatch.setattr(sys.modules["pyfunc2.all_lasts"], "lasts", dummy_lasts)
    monkeypatch.setattr(sys.modules["pyfunc2.all_lasts"], "get_email_path", dummy_get_email_path)
    emails = [{"target": "test@example.com"}]
    result = all_lasts(images=[], lines=2, emails=emails)
    assert result == ["image_2"]

# --- email_update ---
def test_email_update(monkeypatch):
    import pyfunc2.email_update
    called = {'called': False}
    def dummy_download_all_attachments_in_inbox(server, username, password, data_path, source, limit):
        called['called'] = True
    def dummy_get_email_path(target, storage_root):
        return "/tmp"
    monkeypatch.setattr(sys.modules["pyfunc2.email_update"], "download_all_attachments_in_inbox", dummy_download_all_attachments_in_inbox)
    monkeypatch.setattr(sys.modules["pyfunc2.email_update"], "get_email_path", dummy_get_email_path)
    emails = [{"target": "test@example.com", "server": "s", "username": "u", "password": "p", "source": "src"}]
    email_update(emails, storage_root="", limit=1)
    assert called.get('called')

# --- img_to_base64 ---
def test_img_to_base64():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"testdata")
        f.flush()
        path = f.name
    try:
        result = img_to_base64(path)
        expected = base64.b64encode(b"testdata").decode('utf-8')
        assert result == expected
    finally:
        os.remove(path)

# --- lasts ---
def test_lasts(monkeypatch):
    import pyfunc2.lasts
    def dummy_email_update(emails, storage_root, limit):
        pass
    def dummy_file_list(image_path):
        return ["b.png", "a.jpg"]
    monkeypatch.setattr(sys.modules["pyfunc2.lasts"], "email_update", dummy_email_update)
    monkeypatch.setattr(sys.modules["pyfunc2.lasts"], "file_list", dummy_file_list)
    monkeypatch.setattr(os.path, "getmtime", lambda x: {"a.jpg": 1, "b.png": 2}[os.path.basename(x)])
    result = lasts("/tmp", limit=2, emails=[], ftps=[], storage_root="")
    assert result == ["b.png", "a.jpg"]

# --- convert_char ---
def test_convert_char():
    assert convert_char('A') == 'a'
    assert convert_char('Z') == 'z'
    assert convert_char('a') == 'a'
    assert convert_char('0') == '0'

# --- to_lower_case ---
def test_to_lower_case():
    assert to_lower_case('ABC') == 'abc'
    assert to_lower_case('AbC') == 'abc'
    assert to_lower_case('') == ''
    assert to_lower_case('123') == '123'
