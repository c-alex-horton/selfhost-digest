import requests_cache
from app.config import ua

cache_session = requests_cache.CachedSession(
    ".geocode", expire_after=None, headers={"User-Agent": ua}
)


def get_lat_and_lon(location_string):
    params = {"q": location_string, "limit": 1}

    response = cache_session.get("https://photon.komoot.io/api/?", params=params)
    if getattr(response, "from_cache", False):
        print("✅ Served from cache")
    else:
        print("⚠️  Hit the API")

    resp_json = response.json()
    print(resp_json["features"][0]["geometry"]["coordinates"])

    coords = resp_json["features"][0]["geometry"]["coordinates"]

    return {"lat": coords[1], "lon": coords[0]}
