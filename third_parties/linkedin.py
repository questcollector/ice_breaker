import os
import requests


def scrape_linkedin_profile(linkedin_profile_url: str):
    """scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile"""

    use_gist = os.getenv("USE_GIST", default="True")
    response = (
        _gist_scrape_linkedin_profile()
        if use_gist == "True"
        else _real_scrape_linkedin_profile(linkedin_profile_url)
    )

    data = response.json()
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


def _real_scrape_linkedin_profile(linkedin_profile_url: str):
    api_key = os.getenv("PROXYCURL_API_KEY")
    headers = {"Authorization": "Bearer " + api_key}
    api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
    params = {"url": linkedin_profile_url}
    response = requests.get(api_endpoint, params=params, headers=headers)

    return response


def _gist_scrape_linkedin_profile():
    gist_profile_url = "https://gist.githubusercontent.com/emarco177/0d6a3f93dd06634d95e46a2782ed7490/raw/fad4d7a87e3e934ad52ba2a968bad9eb45128665/eden-marco.json"
    response = requests.get(gist_profile_url)
    return response
