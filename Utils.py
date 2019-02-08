import requests

def readjson(url, jsonConv=True, delete_function=False):
    response = requests.get(url, {})
    status = response.status_code

    if status == 200:
        result = response.json()
    else:
        print("Error in accessing api: ", status)
        return
    return result