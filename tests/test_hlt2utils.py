import unittest
from hlt2utils.replays import Replay
import os


RESOURCE_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'resources'
)


class TestReplay(unittest.TestCase):

    def test_can_load_compressed_filepath(self):
        compressed_path = os.path.join(
            RESOURCE_PATH, 'compressed_replay.json.zst'
        )

        Replay(filepath=compressed_path)

    def test_can_load_decompressed_filepath(self):
        decompressed_path = os.path.join(
            RESOURCE_PATH, 'decompressed_replay.json'
        )

        Replay(filepath=decompressed_path)

    def test_can_get_winner(self):
        decompressed_path = os.path.join(
            RESOURCE_PATH, 'decompressed_replay.json'
        )
        replay = Replay(filepath=decompressed_path)

        replay.winner
