import unittest
from app import app, find_relay_line, find_feihua_line, get_pinyin

class PoetryGameTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.used = ["白日依山尽", "黄河入海流"]  # Simulate used lines

    def test_get_pinyin(self):
        self.assertEqual(get_pinyin("白"), "bai")
        self.assertEqual(get_pinyin("山"), "shan")

    def test_feihua_keyword_found(self):
        keyword = "花"
        line = find_feihua_line(keyword, self.used)
        if line:
            self.assertIn(keyword, line)

    def test_feihua_keyword_not_found(self):
        line = find_feihua_line("不存在的关键词", self.used)
        self.assertIsNone(line)

    def test_relay_match_pinyin(self):
        # Use a character that is likely to have matches in the corpus
        last_char = "山"
        line = find_relay_line(last_char, self.used)
        if line:
            self.assertEqual(get_pinyin(line[0]), get_pinyin(last_char))

    def test_relay_no_match(self):
        line = find_relay_line("龘", self.used)  # rare char
        self.assertIsNone(line)

    def test_post_relay(self):
        response = self.client.post("/get_line", json={
            "mode": "relay",
            "prev": "白日依山尽",
            "keyword": "",
            "used": self.used
        })
        json_data = response.get_json()
        self.assertIn("line", json_data)
        self.assertIsInstance(json_data["line"], str)

    def test_post_feihua(self):
        response = self.client.post("/get_line", json={
            "mode": "feihua",
            "prev": "",
            "keyword": "风",
            "used": self.used
        })
        json_data = response.get_json()
        self.assertIn("line", json_data)
        self.assertIsInstance(json_data["line"], str)

if __name__ == '__main__':
    unittest.main()
