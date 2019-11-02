# from pyquery import PyQuery
import requests

if __name__ == '__main__':
    response = requests.get("http://218.94.78.75:20001/sjzx/")
    print(response.text)
