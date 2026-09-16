from dataclasses import dataclass

@dataclass
class intervalOfTimeAwards:
    producer: str
    interval: int
    previousWin: int
    followingWin: int

    def ToJson(self, producer: str, interval: int, previousWin: int, followingWin: int) -> dict:
        return {
            "producer": producer,
            "interval": interval,
            "previousWin": previousWin,
            "followingWin": followingWin
        }