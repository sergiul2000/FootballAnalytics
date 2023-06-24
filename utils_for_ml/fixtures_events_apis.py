import requests


def matches_request():
    # API endpoint and your API key
    url = "https://api.football-data.org/v2/matches"
    api_key = "70a3bac1ea0f42029603f7e27703e9b8"

    # Request headers with API key
    headers = {"X-Auth-Token": api_key}

    # Optional parameters for filtering the matches
    params = {
        "competitions": "CL",  # Example: Premier League
        "dateFrom": "2022-04-12",
        "dateTo": "2022-04-22",
    }

    # Send GET request to the API
    response = requests.get(url, headers=headers, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()
        print(data)
        # Process the retrieved data as per your requirement
        matches = data["matches"]
        for match in matches:
            home_team = match["homeTeam"]["name"]
            home_score = match["score"]["fullTime"]["homeTeam"]
            away_team = match["awayTeam"]["name"]
            away_score = match["score"]["fullTime"]["awayTeam"]
            # Extract and utilize other match statistics as needed
            print(f"{home_team} vs {away_team}")
            print(f"{home_score} : {away_score}")
    else:
        # Print the error message if the request was not successful
        print(f"Error: {response.status_code} - {response.text}")


def fixtures_request():
    url = "https://footapi7.p.rapidapi.com/api/tournament/7/season/36886/best-teams"

    headers = {
        "X-RapidAPI-Key": "afb77be441mshc08c86048a6308cp11514cjsn638bcee1febb",
        "X-RapidAPI-Host": "footapi7.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers)

    # print(response.json())
    data = response.json()
    # results = data["results"]
    # for result in results:
    #     print(result)
    #     print()


def main():
    fixtures_request()


if __name__ == "__main__":
    main()
