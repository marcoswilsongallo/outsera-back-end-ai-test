from flask import Blueprint, jsonify, request
from ratelimit import limits, sleep_and_retry
from Domain.entities import GoldenRaspberryAwards

api = Blueprint("api", __name__)
domain_service = GoldenRaspberryAwards()

# RateLimit: 20 chamadas a cada 10 segundos com retry automatico
FIFTEEN_MINUTES = 10


@api.route("/goldenraspberryawards/wostmovies", methods=["GET"])
@sleep_and_retry
@limits(calls=20, period=10)
def WorstMoviesGoldenRaspberryAwards():
    movies = domain_service.wostmovies()
    return jsonify(movies), 200


@api.route("/goldenraspberryawards/movies", methods=["POST"])
@sleep_and_retry
@limits(calls=20, period=10)
def create_movie():
    data = request.get_json() or {}
    success = domain_service.input_movie(
        year=data.get("year"),
        title=data.get("title"),
        studios=data.get("studios"),
        producers=data.get("producers"),
        winner=data.get("winner", "no")
    )
    if success:
        return jsonify({"message": "Filme inserido com sucesso"}), 201
    return jsonify({"error": "Falha ao inserir filme"}), 400


@api.route("/goldenraspberryawards/movies", methods=["PUT"])
@sleep_and_retry
@limits(calls=20, period=10)
def update_movie():
    data = request.get_json() or {}
    movie_id = data.get("id")
    if not movie_id:
        return jsonify({"error": "ID é obrigatório"}), 400

    success = domain_service.update_movie(movie_id, data)
    if success:
        return jsonify({"message": "Filme atualizado com sucesso"}), 200
    return jsonify({"error": "Falha ao atualizar filme"}), 400


@api.route("/goldenraspberryawards/movies", methods=["DELETE"])
@sleep_and_retry
@limits(calls=20, period=10)
def delete_movie():
    data = request.get_json() or {}
    movie_id = data.get("id")
    if not movie_id:
        return jsonify({"error": "ID é obrigatório"}), 400

    success = domain_service.delete_movie(movie_id)
    if success:
        return jsonify({"message": "Filme removido com sucesso"}), 200
    return jsonify({"error": "Falha ao deletar filme"}), 400


@api.route("/goldenraspberryawards/LongestTwoAwards", methods=["GET"])
@sleep_and_retry
@limits(calls=20, period=10)
def ProducerLongestTwoAwards():
    intervals = domain_service.IntervalTwoAwards()
    longest = domain_service.ProducerLongestIntervalTwoAwards(intervals)
    return jsonify({"min": [], "max": longest}), 200


@api.route("/goldenraspberryawards/shortestTwoAwards", methods=["GET"])
@sleep_and_retry
@limits(calls=20, period=10)
def ProducerShortTwoAwards():
    intervals = domain_service.IntervalTwoAwards()
    shortest = domain_service.ProducerShortestIntervalTwoAwards(intervals)
    return jsonify({"min": shortest, "max": []}), 200