import urllib.parse


MULTICAST_SOCKET_BUFFER = 33554432
MULTICAST_FIFO_PACKETS = 262144
MULTICAST_THREAD_QUEUE = 8192
RTP_REORDER_PACKETS = 8192
RTP_MAX_DELAY_MICROSECONDS = 5000000


def build_buffered_multicast_input(source):
    """Return an FFmpeg input URL and input options for UDP/RTP streams."""
    source = str(source or '').strip()
    parsed = urllib.parse.urlparse(source)
    if parsed.scheme.lower() not in ('udp', 'rtp'):
        return source, []

    query = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
    query.setdefault('fifo_size', [str(MULTICAST_FIFO_PACKETS)])
    query.setdefault('overrun_nonfatal', ['1'])
    query.setdefault('buffer_size', [str(MULTICAST_SOCKET_BUFFER)])
    try:
        socket_buffer = max(65536, int(query['buffer_size'][-1]))
    except (TypeError, ValueError):
        socket_buffer = MULTICAST_SOCKET_BUFFER
        query['buffer_size'] = [str(socket_buffer)]
    input_url = urllib.parse.urlunparse(
        parsed._replace(query=urllib.parse.urlencode(query, doseq=True))
    )
    options = [
        '-thread_queue_size', str(MULTICAST_THREAD_QUEUE),
        '-buffer_size', str(socket_buffer),
    ]
    if parsed.scheme.lower() == 'rtp':
        options.extend([
            '-reorder_queue_size', str(RTP_REORDER_PACKETS),
            '-max_delay', str(RTP_MAX_DELAY_MICROSECONDS),
        ])
    return input_url, options
