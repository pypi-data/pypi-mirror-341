import unittest
from pyfunc2.markdown.create_dir_structure import create_dir_structure
from pyfunc2.markdown.create_dir_structure_from_headers import create_dir_structure_from_headers
from pyfunc2.markdown.create_folders_files import create_folders_files
from pyfunc2.markdown.get_code_extension_dict import get_code_extension_dict
from pyfunc2.markdown.get_dictionary_structure_by_separator_list import get_dictionary_structure_by_separator_list
from pyfunc2.markdown.get_dictionary_structure_from_headers_content import get_dictionary_structure_from_headers_content
from pyfunc2.markdown.get_header_list import get_header_list
from pyfunc2.markdown.get_url_list import get_url_list
import os
import shutil

class TestMarkdownFunctions(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_docs"
        self.test_files = ["test_docs/intro.md", "test_docs/usage.md"]
        os.makedirs(self.test_dir, exist_ok=True)
        for f in self.test_files:
            os.makedirs(os.path.dirname(f), exist_ok=True)
            with open(f, "w") as file:
                file.write("# Test\n")

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_create_dir_structure(self):
        paths = ["test_docs/a", "test_docs/b"]
        create_dir_structure(paths)
        for path in paths:
            self.assertTrue(os.path.isdir(path))

    def test_create_dir_structure_from_headers(self):
        headers = ["# A", "## B"]
        create_dir_structure_from_headers(headers, root=self.test_dir)
        self.assertTrue(os.path.isdir(os.path.join(self.test_dir, "A")))
        self.assertTrue(os.path.isdir(os.path.join(self.test_dir, "A", "B")))

    def test_create_folders_files(self):
        structure = {self.test_dir: ["file1.md", "file2.md"]}
        create_folders_files(structure)
        for fname in structure[self.test_dir]:
            self.assertTrue(os.path.isfile(os.path.join(self.test_dir, fname)))

    def test_get_code_extension_dict(self):
        ext_dict = get_code_extension_dict()
        self.assertIsInstance(ext_dict, dict)
        self.assertIn("py", ext_dict)

    def test_get_dictionary_structure_by_separator_list(self):
        paths = ["a/b/c.txt", "a/b/d.txt", "a/e.txt"]
        structure = get_dictionary_structure_by_separator_list(paths)
        self.assertIsInstance(structure, dict)
        self.assertIn("a", structure)

    def test_get_dictionary_structure_from_headers_content(self):
        headers = ["# A", "## B"]
        contents = ["desc A", "desc B"]
        structure = get_dictionary_structure_from_headers_content(headers, contents)
        self.assertIsInstance(structure, dict)
        self.assertIn("A", structure)

    def test_get_header_list(self):
        markdown_text = "# A\n## B"
        headers = get_header_list(markdown_text)
        self.assertIn("# A", headers)
        self.assertIn("## B", headers)

    def test_get_url_list(self):
        markdown_text = "[OpenAI](https://openai.com)"
        urls = get_url_list(markdown_text)
        self.assertIn("https://openai.com", urls)

if __name__ == "__main__":
    unittest.main()
