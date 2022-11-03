import requests as rq


def get_access_token():
    request = rq.Request()

    request.data = {"refreshToken": "HP4v6PasVpPt6RG5Dm4ufeyBVRJPi6T3gaKyKrRCXvFxjI9ytN"}
    media_type = {"content-type": "application/json"}
    response = rq.post("https://solvdinternal.zebrunner.com/api/iam/v1/auth/refresh",
                       json={"refreshToken": "HP4v6PasVpPt6RG5Dm4ufeyBVRJPi6T3gaKyKrRCXvFxjI9ytN"},
                       headers=media_type)

    json_response = response.json()

    access_token = json_response["authToken"]

    print(f'Access token: {access_token}')


if __name__ == "__main__":
    get_access_token()
