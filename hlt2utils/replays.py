import json
import zstd
from collections import defaultdict, Counter
from .error import Error


class InitializationError(Error):
    pass


def load_replay(path):
    with open(path, 'rb') as f:
        file_bytes = f.read()
    try:
        file_bytes = zstd.loads(file_bytes)
    except ValueError:
        # file was already decompressed
        pass
    game_json = file_bytes.decode()

    return json.loads(game_json)


class Replay(object):

    def __init__(self, filepath=None, replay=None):
        if filepath is None and game_data is None:
            raise InitializationError("filepath or game_data must be set")
        if filepath is not None:
            replay = load_replay(filepath)
        self.replay_dict = replay

    def dump(filepath, compress=True):
        json_text = json.dumps(self.replay_dict)
        if compress:
            with open(filepath, 'wb') as f:
                f.write(zstd.dumps(bytes(json_text, 'utf-8')))
        else:
            with open(filepath, 'w') as f:
                json.dump(self.replay_dict, f)

    @property
    def frames(self):
        return [Frame(frame) for frame in self.replay_dict['frames']]

    @property
    def winner(self):
        end_frame = self.frames[-1]
        ship_counts = end_frame.player_ship_count
        remaining_players = [
            player for player, count in ship_counts.items() if count > 0
        ]
        if len(remaining_players) == 1:
            return remaining_players[0]
        planet_counts = end_frame.player_planet_count
        if len(planet_counts) == 1:
            return list(planet_counts.keys())[0]
        ships_produced = self.ships_produced
        leaders = [
            owner for owner, score in ships_produced.items()
            if score == max(ships_produced.values())
        ]
        if len(leaders) == 1:
            return leaders[0]
        return None

    def ships_produced(self, up_to=None):
        totals = Counter()
        if up_to is None:
            up_to = self.replay_dict['num_frames']
        for frame in self.frames[:upto + 1]:
            totals += Counter(get_ships_produced_in_frame(frame))
        return dict(totals)



class Frame(object):

    def __init__(self, frame_dict):
        self.frame_dict = frame_dict

    @property
    def player_planet_count(self):
        planet_counts = defaultdict(int)
        for planet in self.frame_dict['planets'].values():
            if planet['owner'] is not None:
                planet_counts[planet['owner']] += 1
        return dict(planet_counts)

    @property
    def player_ship_count(self):
        return {
            key: len(value) for key, value in self.frame_dict['ships'].items()
        }

    @property
    def ships_produced(self):
        if 'events' not in self.frame_dict:
            return {}
        produced_count = defaultdict(int)
        for event in self.frame_dict['events']:
            if (
                (event['entity']['type'] != 'ship')
                or (event['event'] != 'spawned')
            ):
                continue
            produced_count[event['entity']['owner']] += 1
        return dict(produced_count)
