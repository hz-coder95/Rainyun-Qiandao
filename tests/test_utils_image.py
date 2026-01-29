import importlib.util
import unittest

NUMPY_AVAILABLE = importlib.util.find_spec("numpy") is not None
CV2_AVAILABLE = importlib.util.find_spec("cv2") is not None

if NUMPY_AVAILABLE and CV2_AVAILABLE:
    import cv2
    import numpy as np

    from rainyun.utils.image import decode_image_bytes, split_sprite_image


@unittest.skipUnless(NUMPY_AVAILABLE and CV2_AVAILABLE, "numpy/cv2 未安装，跳过图像工具测试")
class ImageUtilsTests(unittest.TestCase):
    def test_decode_image_bytes(self):
        image = np.zeros((10, 10, 3), dtype=np.uint8)
        success, encoded = cv2.imencode(".jpg", image)
        self.assertTrue(success)
        decoded = decode_image_bytes(encoded.tobytes(), "test")
        self.assertEqual(decoded.shape[0], 10)
        self.assertEqual(decoded.shape[1], 10)

    def test_split_sprite_image(self):
        sprite = np.zeros((5, 10, 3), dtype=np.uint8)
        parts = split_sprite_image(sprite)
        self.assertEqual(len(parts), 3)
        self.assertEqual(parts[0].shape[1], 3)
        self.assertEqual(parts[1].shape[1], 3)
        self.assertEqual(parts[2].shape[1], 4)


if __name__ == "__main__":
    unittest.main()
