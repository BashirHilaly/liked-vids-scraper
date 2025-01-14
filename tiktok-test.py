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
        response = self.session.get(url, headers=self.headers)
        
        # Extract user data from response
        if response.status_code == 200:
            # Parse the HTML to extract user info
            # This would require analyzing the response structure
            pass
            
        return None
        
    def get_user_videos(self, username, max_count=30):
        """Get user's video list"""
        url = f"https://www.tiktok.com/api/user/videos"
        params = {
            "username": username,
            "count": max_count,
            "cursor": 0
        }
        
        response = self.session.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            return response.json()
        return None

    def download_video(self, video_id):
        """Download a specific video"""
        url = f"https://www.tiktok.com/api/video/detail/?itemId={video_id}"
        response = self.session.get(url, headers=self.headers)
        
        if response.status_code == 200:
            video_data = response.json()
            # Extract video URL and download
            video_url = video_data.get("itemInfo", {}).get("itemStruct", {}).get("video", {}).get("downloadAddr")
            if video_url:
                video_response = self.session.get(video_url, headers=self.headers)
                if video_response.status_code == 200:
                    return video_response.content
        return None

def main():
    scraper = TikTokScraper()
    
    # Example usage
    username = "example_user"
    user_info = scraper.get_user_info(username)
    videos = scraper.get_user_videos(username)
    
    if videos:
        print(videos)
        # for video in videos:
        #     video_id = video.get("id")
        #     video_data = scraper.download_video(video_id)
        #     if video_data:
        #         with open(f"video_{video_id}.mp4", "wb") as f:
        #             f.write(video_data)

if __name__ == "__main__":
    main()