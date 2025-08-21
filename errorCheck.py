import requests

from vars import URL

if __name__ == '__main__':
    response = requests.get(URL)
    print(response.status_code)