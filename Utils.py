import requests

def readjson(url, jsonConv=True, delete_function=False, tries=5):

    for i in range(5):
        response = requests.get(url, {})
        status = response.status_code

        if status == 200:
            return response.json()

    print("Error in accessing api:", status, "(after", tries, "tries)")