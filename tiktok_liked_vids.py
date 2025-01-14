import requests
import json
import os
from dotenv import load_dotenv


class TikTokScraper:
    def __init__(self):
        load_dotenv()
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json",
            # Add any necessary cookies or auth tokens here
            "Cookie": os.getenv('TIKTOK_COOKIES', '')
        }

    def get_liked_videos(self, user_id, max_count=30):
        url = "https://www.tiktok.com/@carfit.app"
        params = {
            "count": 30,
            "cursor": 0,
            "user_id": user_id,
            "aid": "1988",
            "app_language": "en",
            "device_platform": "web_pc",
        }

        videos = []
        while len(videos) < max_count:
            try:
                response = self.session.get(url, headers=self.headers, params=params)
                print("Response Attributes:")
                for attr in dir(response):
                    if not attr.startswith('_'):  # Skip private attributes
                        print(f"{attr}")
                data = response.json()
                
                if not data.get('itemList'):
                    break

                for item in data['itemList']:
                    videos.append({
                        'id': item.get('id'),
                        'desc': item.get('desc'),
                        'video_url': item.get('video', {}).get('playAddr'),
                        'author': item.get('author', {}).get('uniqueId'),
                        'stats': {
                            'likes': item.get('stats', {}).get('diggCount'),
                            'shares': item.get('stats', {}).get('shareCount'),
                            'comments': item.get('stats', {}).get('commentCount')
                        }
                    })

                    if len(videos) >= max_count:
                        break

                # Update cursor for next page
                params['cursor'] = data.get('cursor')
                
                if not data.get('hasMore'):
                    break

            except Exception as e:
                print(f"Error fetching videos: {str(e)}")
                break

        return videos[:max_count]

def main():
    scraper = TikTokScraper()
    # Replace with actual user ID
    user_id = "YOUR_USER_ID"
    videos = scraper.get_liked_videos(user_id, max_count=20)
    
    # Save results
    with open("liked_videos.json", "w") as f:
        json.dump(videos, f, indent=2)

if __name__ == "__main__":
    main()

