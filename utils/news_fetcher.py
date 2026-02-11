import requests
import time
from functools import lru_cache

class NewsFetcher:
    def __init__(self):
        self.base_url = "https://hacker-news.firebaseio.com/v0"
        self._cache = {
            'news': {'data': [], 'timestamp': 0},
            'jobs': {'data': [], 'timestamp': 0}
        }
        self.CACHE_DURATION = 300  # 5 minutes

    def get_latest_data(self):
        """Get latest news and jobs with caching"""
        return {
            'news': self._get_category('topstories', 'news'),
            'jobs': self._get_category('jobstories', 'jobs')
        }

    def _get_category(self, endpoint, cache_key):
        """Fetch data from HN API with caching"""
        now = time.time()
        if now - self._cache[cache_key]['timestamp'] < self.CACHE_DURATION and self._cache[cache_key]['data']:
            return self._cache[cache_key]['data']

        try:
            # Get list of IDs
            response = requests.get(f"{self.base_url}/{endpoint}.json")
            ids = response.json()[:6]  # Get top 6 items

            items = []
            for item_id in ids:
                item_details = self._get_item_details(item_id)
                if item_details:
                    items.append(item_details)

            self._cache[cache_key] = {
                'data': items,
                'timestamp': now
            }
            return items
        except Exception as e:
            print(f"Error fetching {cache_key}: {e}")
            return self._cache[cache_key]['data']  # Return stale data if fetch fails

    def _get_item_details(self, item_id):
        try:
            response = requests.get(f"{self.base_url}/item/{item_id}.json")
            data = response.json()
            return {
                'title': data.get('title'),
                'url': data.get('url', f"https://news.ycombinator.com/item?id={item_id}"),
                'time': data.get('time'),
                'score': data.get('score', 0),
                'by': data.get('by')
            }
        except:
            return None
