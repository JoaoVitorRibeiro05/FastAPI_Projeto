import requests

headers = {
    "Authorization" : "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI5IiwiZXhwIjoxNzc3MzE0ODEzfQ.OD8S9A2KWasBPfca_Zp2xwJraOoAkfdfONILHqgiuV0"
}

r = requests.get("http://127.0.0.1:8000/auth/refresh",headers=headers)
print(r.status_code)
print(r.json())
