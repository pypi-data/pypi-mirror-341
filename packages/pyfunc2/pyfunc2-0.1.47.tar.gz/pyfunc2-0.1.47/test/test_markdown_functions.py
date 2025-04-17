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
        md_text = "A\nB"
        base_dir = self.test_dir
        create_dir_structure(md_text, base_dir)
        self.assertTrue(os.path.isdir(os.path.join(base_dir, "A")))
        self.assertTrue(os.path.isdir(os.path.join(base_dir, "B")))

    def test_create_dir_structure_from_headers(self):
        # Prepare a markdown file
        md_path = os.path.join(self.test_dir, "headers.md")
        with open(md_path, "w") as f:
            f.write("# A\n## B\n")
        create_dir_structure_from_headers(md_path, path=self.test_dir)
        self.assertTrue(os.path.isdir(os.path.join(self.test_dir, "A")))
        self.assertTrue(os.path.isdir(os.path.join(self.test_dir, "B")))

    def test_create_folders_files(self):
        # Prepare a markdown file
        md_path = os.path.join(self.test_dir, "files.md")
        with open(md_path, "w") as f:
            f.write("# Section\n```bash\necho hello\n```\n")
        create_folders_files(md_path, path=self.test_dir)
        self.assertTrue(os.path.isfile(os.path.join(self.test_dir, "Section", "1.bash")))

    def test_get_code_extension_dict(self):
        content = """```python\nprint('hello')\n```"""
        ext_list = ["python"]
        ext_head_list = {"python": "#!/bin/python"}
        result = get_code_extension_dict(content, ext_list, ext_head_list)
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]["extension"], "python")

    def test_get_dictionary_structure_by_separator_list(self):
        markdown = """```bash\necho hello\n```\n```bash\necho world\n```"""
        blocks = get_dictionary_structure_by_separator_list(markdown)
        self.assertIsInstance(blocks, list)
        self.assertTrue(any("hello" in block for block in blocks))

    def test_get_dictionary_structure_from_headers_content(self):
        # Prepare a markdown file
        md_path = os.path.join(self.test_dir, "headers_content.md")
        with open(md_path, "w") as f:
            f.write("# A\ndesc A\n## B\ndesc B\n")
        structure = get_dictionary_structure_from_headers_content(md_path)
        self.assertIsInstance(structure, dict)
        self.assertIn("A", structure)

    def test_get_header_list(self):
        markdown_text = "# A\n## B"
        headers = get_header_list(markdown_text)
        self.assertIn("A", headers)
        self.assertIn("B", headers)

    def test_get_url_list(self):
        markdown_text = "[OpenAI](https://openai.com)"
        urls = get_url_list(markdown_text)
        self.assertIn("https://openai.com", urls)

if __name__ == "__main__":
    unittest.main()
