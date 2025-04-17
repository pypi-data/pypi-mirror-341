import os
import tempfile
import pytest
from pyfunc2.email.download_attachments_in_email import download_attachments_in_email

class DummyPart:
    def __init__(self, filename, content_type, payload):
        self.filename = filename
        self.content_type = content_type
        self.payload = payload
    def get_filename(self):
        return self.filename
    def get_content_type(self):
        print(f"[DummyPart] get_content_type called, returning: {self.content_type}")
        return self.content_type
    def get_payload(self, decode=False):
        return self.payload
    def get(self, key):
        if key == 'Content-Disposition':
            print(f"[DummyPart] get('Content-Disposition') called, returning: attachment; filename={self.filename}")
            return f'attachment; filename="{self.filename}"'
        return None
    def is_multipart(self):
        return False
    def get_content_maintype(self):
        maintype = self.content_type.split('/')[0]
        print(f"[DummyPart] get_content_maintype called, returning: {maintype}")
        return maintype

class DummyEmail:
    def __init__(self, parts):
        self.parts = parts
    def walk(self):
        print("[DummyEmail] walk called, returning parts:", self.parts)
        return self.parts
    def get_content_maintype(self):
        return 'multipart'
    def is_multipart(self):
        return True

@pytest.fixture
def dummy_data():
    part = DummyPart('testfile', 'application/pdf', b'PDFDATA')
    email_obj = DummyEmail([part])
    resp = 'OK'
    data = [(None, b'')]  # The function expects a list of tuples
    return resp, data, email_obj

def test_download_attachments_in_email_creates_file(monkeypatch, dummy_data):
    resp, data, email_obj = dummy_data
    monkeypatch.setattr('email.message_from_bytes', lambda b: email_obj)
    with tempfile.TemporaryDirectory() as tmpdir:
        monkeypatch.setattr('pyfunc2.file.check_and_create_path', lambda d: None)
        download_attachments_in_email(resp, data, emailid='1', outputdir=tmpdir + '/')
        print("Zawartość katalogu tymczasowego:", os.listdir(tmpdir))
        # Rekurencyjnie wypisz wszystkie pliki i foldery
        for root, dirs, files in os.walk(tmpdir):
            print(f"Katalog: {root}")
            for file in files:
                print(f"Plik: {file}")
        # Szukaj pliku 1_1.pdf w dowolnym miejscu
        found = False
        for root, dirs, files in os.walk(tmpdir):
            for file in files:
                if file == '1_1.pdf':
                    found = True
        assert found
