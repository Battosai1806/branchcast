import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from feasibility import diagram


class DiagramTests(unittest.TestCase):
    def test_conversion_posts_image_and_returns_shapes(self):
        shape = {"type": "rectangle", "label": "Start", "x": 10, "y": 20, "width": 30, "height": 15}
        response = {"output": [{"content": [{"type": "output_text", "text": json.dumps({"shapes": [shape]})}]}]}
        with tempfile.TemporaryDirectory() as tmp:
            image = Path(tmp) / "test.png"
            image.write_bytes(b"image bytes")
            with patch("urllib.request.urlopen", return_value=io.BytesIO(json.dumps(response).encode())) as urlopen:
                self.assertEqual(diagram.convert(image, "test-key"), {"shapes": [shape]})
                request = urlopen.call_args.args[0]
                body = json.loads(request.data)
                self.assertEqual(body["input"][0]["content"][1]["type"], "input_image")
                self.assertTrue(body["text"]["format"]["strict"])

    def test_rejects_invalid_geometry(self):
        with self.assertRaises(ValueError):
            diagram.validate({"shapes": [{"type": "rectangle", "label": "x", "x": -1, "y": 0, "width": 1, "height": 1}]})

    def test_rejects_non_image(self):
        with self.assertRaises(ValueError):
            diagram.convert("not-an-image.txt", "key")

if __name__ == "__main__":
    unittest.main()
