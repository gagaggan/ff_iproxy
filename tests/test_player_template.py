import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PlayerTemplateTest(unittest.TestCase):
    def test_mpegts_player_uses_live_buffering(self):
        template = (ROOT / 'templates' / 'ff_iproxy_player.html').read_text(encoding='utf-8')

        self.assertIn('mpegts.js@1.8.2', template)
        self.assertIn("type: 'mse'", template)
        self.assertIn('enableStashBuffer: true', template)
        self.assertIn('stashInitialSize: 4 * 1024 * 1024', template)
        self.assertIn('lazyLoad: false', template)
        self.assertIn('enableWorkerForMSE: true', template)
        self.assertIn('liveBufferLatencyChasing: false', template)
        self.assertNotIn('liveBufferLatencyMaxLatency', template)
        self.assertIn('scheduleRecovery', template)
        self.assertIn('recoveryAttempts >= 3', template)
        self.assertIn("mpegtsPlayer.unload();", template)
        self.assertIn('new URL(', template)

    def test_stream_action_opens_mpegts_player_page(self):
        template = (ROOT / 'templates' / 'ff_iproxy_list.html').read_text(encoding='utf-8')

        self.assertIn("'play_mpegts_btn'", template)
        self.assertIn('item.mpegts_player_url', template)

    def test_uxn_channel_uses_rtp(self):
        channels = json.loads((ROOT / 'resources' / 'channels.json').read_text(encoding='utf-8'))
        uxn = channels['ch120']

        self.assertEqual(uxn['type'], 'rtp')
        self.assertEqual(uxn['url'], 'rtp://239.192.81.38:49220')

    def test_fmp4_hls_support_is_wired(self):
        stream_source = (ROOT / 'stream_service.py').read_text(encoding='utf-8')
        route_source = (ROOT / 'logic.py').read_text(encoding='utf-8')

        self.assertIn("('mpegts', 'fmp4')", stream_source)
        self.assertIn("'-hls_segment_type', 'fmp4'", stream_source)
        self.assertIn("'-hls_fmp4_init_filename', 'init.mp4'", stream_source)
        self.assertIn("'-tag:v', 'hvc1'", stream_source)
        self.assertIn("f'segment_%05d.{extension}'", stream_source)
        self.assertIn("glob('*.m4s')", stream_source)
        self.assertIn("line.endswith(('.ts', '.m4s'))", route_source)
        self.assertIn("line.startswith('#EXT-X-MAP:')", route_source)
        self.assertIn("'.m4s': 'video/iso.segment'", route_source)
        self.assertIn("'.mp4': 'video/mp4'", route_source)


if __name__ == '__main__':
    unittest.main()
