import requests

def torrent_search(torrent_name):
    base_url = f"https://api.sumanjay.cf/torrent/?query={torrent_name}"
    request = requests.get(base_url)
    if (request.status_code == 200):
        response = request.json()
        return response
    return None