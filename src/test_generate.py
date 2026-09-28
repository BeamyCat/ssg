import unittest
from generate import extract_title


class TestUtilGenerate(unittest.TestCase):
    def test_extract_title(self):
        md = "# This is the title"
        self.assertEqual(extract_title(md), "This is the title")
    
    def test_extract_title2(self):
        md = """
# BeamyCat

## Main

Per aspera ad astra.
"""
        self.assertEqual(extract_title(md), "BeamyCat")
    
    def test_extract_title3(self):
        md = """
## Why would h2 be here?

# Idk, but this is the title!

### Woah, that's a pretty nice title!
"""
        self.assertEqual(extract_title(md), "Idk, but this is the title!")


if __name__ == "__main__":
    unittest.main()

