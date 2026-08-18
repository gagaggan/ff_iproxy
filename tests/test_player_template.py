import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PlayerTemplateTest(unittest.TestCase):
    def test_mpegts_player_uses_live_buffering(self):
        template = (ROOT / 'templates' / 'ff_iproxy_player.html').read_text(encoding='utf-8')

        self.assertIn('mpegts.js@1.8.2', template)
        self.assertIn("type: 'mse'", template)
        self.assertIn('enableStashBuffer: true', template)
        self.assertIn('stashInitialSize: 8 * 1024 * 1024', template)
        self.assertIn('lazyLoad: false', template)
        self.assertIn('enableWorkerForMSE: true', template)
        self.assertIn('new URL(', template)

    def test_stream_action_opens_mpegts_player_page(self):
        template = (ROOT / 'templates' / 'ff_iproxy_list.html').read_text(encoding='utf-8')

        self.assertIn("'play_mpegts_btn'", template)
        self.assertIn('item.mpegts_player_url', template)


if __name__ == '__main__':
    unittest.main()
