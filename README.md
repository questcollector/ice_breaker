# Ice Breaker

project for study of Udemy course `Develop LLM powered applications with LangChain`

source: https://github.com/emarco177/ice_breaker.git

# Environment variables

these environment variables below is needed for execution

- `OPENAI_API_KEY`
- `PROXYCURL_API_KEY`
- `SERPAPI_API_KEY`
- `TWITTER_API_KEY`
- `TWITTER_API_SECRET`
- `TWITTER_ACCESS_TOKEN`
- `TWITTER_ACCESS_SECRET`

# Execution

[ice_breaker.py](ice_breaker.py)

# third parties package

package for purpose of:

- scrape Linkedin profile
- scrape Twitter tweets

uses Proxycurl API

# agents package

provides Langchain Agent to lookup Linkedin profile url with given search keyword

# tools package

provides SerpAPIWrapper to implement agent's function