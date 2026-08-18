import unittest

from multicast_input import build_buffered_multicast_input


class MulticastInputTest(unittest.TestCase):
    def test_adds_rtp_socket_and_reorder_buffers(self):
        url, options = build_buffered_multicast_input('rtp://239.192.81.39:49220')

        self.assertIn('fifo_size=262144', url)
        self.assertIn('overrun_nonfatal=1', url)
        self.assertIn('buffer_size=33554432', url)
        self.assertEqual(options[options.index('-thread_queue_size') + 1], '8192')
        self.assertEqual(options[options.index('-reorder_queue_size') + 1], '8192')
        self.assertEqual(options[options.index('-max_delay') + 1], '5000000')

    def test_preserves_existing_multicast_query_values(self):
        url, options = build_buffered_multicast_input(
            'udp://239.1.2.3:49220?localaddr=192.168.29.230&buffer_size=1048576'
        )

        self.assertIn('localaddr=192.168.29.230', url)
        self.assertIn('buffer_size=1048576', url)
        self.assertEqual(options[options.index('-buffer_size') + 1], '1048576')
        self.assertNotIn('reorder_queue_size', options)

    def test_leaves_http_input_unchanged(self):
        source = 'https://example.com/live.ts?token=value'
        self.assertEqual(build_buffered_multicast_input(source), (source, []))


if __name__ == '__main__':
    unittest.main()
