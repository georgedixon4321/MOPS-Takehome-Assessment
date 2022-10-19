import json

import requests

endpoints = {
    "agify": "https://api.agify.io?name=",
    "genderize": "https://api.genderize.io?name=",
    "nationalize": "https://api.nationalize.io?name=",
}


def api_request_get(name, endpoint):
    client = requests.Session()
    response = client.get(f"{endpoint}{name}")
    response.raise_for_status()
    return json.loads(response.content.decode("utf-8"))


def get_age_from_agify_api(name):
    agify_api_data = api_request_get(name=name, endpoint=endpoints["agify"])
    return agify_api_data["age"]


def get_gender_from_genderize_api(name):
    genderize_api_data = api_request_get(name=name, endpoint=endpoints["genderize"])
    return genderize_api_data["gender"]


def get_most_likely_nationality_from_nationalize_api(name):
    nationalize_api_data = api_request_get(name=name, endpoint=endpoints["nationalize"])
    # print(f"All data: {nationalize_api_data['country']}")
    mostLikelyNationality = max(
        nationalize_api_data["country"], key=lambda x: x["probability"]
    )
    # print(f"Most likely: {mostLikelyNationality}")
    # Needs test for equal max values
    return mostLikelyNationality["country_id"]


def verkada_api_request_post(data):
    client = requests.Session()
    response = client.post(
        "https://rwph529xx9.execute-api.us-west-1.amazonaws.com/prod/pushToSlack",
        json={"data": data},
    )
    response.raise_for_status()
    print(response.content.decode("utf-8"))
    return response.content.decode("utf-8")
