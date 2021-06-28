from mononobe_core.player import Player
from mononobe_core.player.vlc_player import VlcPlayer


class TestPlayer:
    def test_init_vlc(self):
        assert isinstance(Player.init('vlc'), VlcPlayer) is True
