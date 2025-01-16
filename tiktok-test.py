import requests
import json



class TikTokScraper:
    def __init__(self):
        self.base_url = "https://www.tiktok.com"
        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.9",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate", 
            "sec-fetch-site": "none",
            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
        }
        self.session = requests.Session()
        
    def get_user_info(self, username):
        """Get user profile information"""
        url = f"{self.base_url}/@{username}"
        params = {
            "WebIdLastTime": "1705376499",
            "aid": "1988",
            "app_language": "en",
            "app_name": "tiktok_web",
            "browser_language": "en-US",
            "browser_platform": "Win32",
            "device_platform": "web_pc",
            "focus_state": True,
            "from_page": "user",
            "history_len": 4,
            "is_fullscreen": False,
            "is_page_visible": True,
            "os": "windows",
            "region": "US",
            "screen_height": 1080,
            "screen_width": 1920,
        }
        
        response = self.session.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            return response.json()
        return None
        
    def get_user_videos(self, username, max_count=30):
        """Get user's video list"""
        url = f"https://www.tiktok.com/api/user/videos"
        params = {
            "WebIdLastTime": "1705376499",
            "aid": "1988",
            "app_language": "en",
            "app_name": "tiktok_web",
            "browser_language": "en-US",
            "count": max_count,
            "cursor": 0,
            "device_platform": "web_pc",
            "focus_state": True,
            "from_page": "user",
            "history_len": 4,
            "is_fullscreen": False,
            "is_page_visible": True,
            "os": "windows",
            "region": "US",
            "screen_height": 1080,
            "screen_width": 1920,
            "username": username
        }
        
        response = self.session.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            return response.json()
        return None

    def get_liked_videos(self, user_id, max_count=30):
        """Get user's liked videos"""
        url = f"https://www.tiktok.com/api/favorite/item_list/"
        params = {
            "WebIdLastTime": "1705376499",
            "aid": "1988",
            "app_language": "en",
            "app_name": "tiktok_web",
            "browser_language": "en-US",
            "count": max_count,
            "cursor": 0,
            "device_platform": "web_pc",
            "focus_state": True,
            "from_page": "user",
            "history_len": 4,
            "is_fullscreen": False,
            "is_page_visible": True,
            "os": "windows",
            "region": "US",
            "screen_height": 1080,
            "screen_width": 1920,
            "user_id": user_id
        }
        
        response = self.session.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            videos = []
            
            if data.get('itemList'):
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
            return videos
        return None

def main():
    scraper = TikTokScraper()
    
    # Example usage
    username = "example_user"
    user_id = "123456789"  # Replace with actual user ID
    
    # Get liked videos
    liked_videos = scraper.get_liked_videos(user_id)
    if liked_videos:
        print(json.dumps(liked_videos, indent=2))
    else:
        print("Failed to fetch liked videos")

if __name__ == "__main__":
    main()