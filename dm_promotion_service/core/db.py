import requests

URL = "https://script.google.com/macros/s/AKfycbwmU2M8Ez9a1IXBfW9yhOsQsW8eT4JNaXoYyQs2KUYPPA6QhCxLIR5YEpoikxTMPUlH/exec"

payload = {
    "user_id": "123456",
}

r = requests.post(URL, json=payload)
print(r.json())

