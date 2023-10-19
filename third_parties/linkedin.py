import os
import requests
import json
import pathlib

linkedin_file = pathlib.Path(__file__).parent / "edens_linkedin.json"

def scrape_linkedin_profile(linkedin_profile_url: str):
    """scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile"""

    use_linkedin = os.getenv("USE_LINKEDIN", default="False")
    data = (
        _file_scrape_linkedin_profile(linkedin_file)
        if use_linkedin == "False"
        else _real_scrape_linkedin_profile(linkedin_profile_url)
    )

    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", " ", None)
        and k not in ["people_also_viewed", "certifications"]
    }

    if groups_dict := data.get("groups"):
        for group_dict in groups_dict:
            group_dict.pop("profile_pic_url")

    return data


def _real_scrape_linkedin_profile(linkedin_profile_url: str) -> dict:
    api_key = os.getenv("PROXYCURL_API_KEY")
    headers = {"Authorization": "Bearer " + api_key}
    api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
    params = {"url": linkedin_profile_url}
    response = requests.get(api_endpoint, params=params, headers=headers)

    return response.json()


def _file_scrape_linkedin_profile(linkedin_file: pathlib.Path) -> dict:
    with linkedin_file.open("r") as f:
        return json.load(f)
