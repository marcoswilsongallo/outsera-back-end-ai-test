from typing import List, Dict, Any
from itertools import combinations
from infrastructure.database import DataBaseMovies
from infrastructure.IntervalTimeAwards import intervalOfTimeAwards


class GoldenRaspberryAwards:
    def __init__(self):
        self.db = DataBaseMovies()

    def wostmovies(self) -> List[Dict[str, Any]]:
        try:
            return self.db.get_all_movies()
        except Exception as e:
            raise e

    def input_movie(self, year: int, title: str, studios: str, producers: str, winner: str = "no") -> bool:
        try:
            return self.db.insert_movie(year, title, studios, producers, winner)
        except Exception:
            return False

    def update_movie(self, movie_id: int, data: Dict[str, Any]) -> bool:
        try:
            return self.db.update_movie(movie_id, data)
        except Exception:
            return False

    def delete_movie(self, movie_id: int) -> bool:
        try:
            return self.db.delete_movie(movie_id)
        except Exception:
            return False

    def IntervalTwoAwards(self) -> List[Dict[str, Any]]:
        try:
            winners = self.db.get_winner_movies()

            # Formata a lista de tuplas (producer, year) lidando com múltiplos produtores
            tuples_list = []
            for item in winners:
                producers_str = item["producers"].replace(" and ", ", ")
                producers_list = [p.strip() for p in producers_str.split(",") if p.strip()]
                for prod in producers_list:
                    tuples_list.append((prod, item["year"]))

            # Ordena por year e producers
            tuples_list.sort(key=lambda x: (x[1], x[0]))

            # Agrupa anos únicos por produtor
            producer_years: Dict[str, List[int]] = {}
            for prod, year in tuples_list:
                if prod not in producer_years:
                    producer_years[prod] = []
                if year not in producer_years[prod]:
                    producer_years[prod].append(year)

            # Filtra nomes com mais de um ano diferente e calcula intervalos consecutivos
            result_json = []
            converter = intervalOfTimeAwards("", 0, 0, 0)

            for prod, years in producer_years.items():
                if len(years) > 1:
                    sorted_years = sorted(years)
                    for i in range(len(sorted_years) - 1):
                        prev = sorted_years[i]
                        follow = sorted_years[i + 1]
                        interval = follow - prev
                        json_data = converter.ToJson(
                            producer=prod,
                            interval=interval,
                            previousWin=prev,
                            followingWin=follow
                        )
                        result_json.append(json_data)

            return result_json
        except Exception as e:
            raise e

    def ProducerLongestIntervalTwoAwards(self, interval_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        try:
            if not interval_list:
                return []
            max_interval = max(item["interval"] for item in interval_list)
            print(interval_list)
            print([item for item in interval_list if item["interval"] == max_interval])
            return [item for item in interval_list if item["interval"] == max_interval]
        except Exception as e:
            raise e

    def ProducerShortestIntervalTwoAwards(self, interval_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        try:
            if not interval_list:
                return []
            min_interval = min(item["interval"] for item in interval_list)
            print(interval_list)
            print([item for item in interval_list if item["interval"] == min_interval])
            return [item for item in interval_list if item["interval"] == min_interval]
        except Exception as e:
            raise e