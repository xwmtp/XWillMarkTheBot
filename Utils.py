import requests

def readjson(url, tries=5):

    for i in range(1):
        response = requests.get(url)

        status = response.status_code

        if status == 200:
            return response.json()
        if status == 404:
            return

    print("Error in accessing api:", status, "(after", tries, "tries)")

    # https://www.speedrun.com/api/v1/games/j1l9qz1g/categories