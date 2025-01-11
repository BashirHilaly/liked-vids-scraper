from TikTokApi import TikTokApi
import os
from dotenv import load_dotenv

class TikTokLikedVideos:
    def __init__(self):
        load_dotenv()
        self.username = os.getenv('TIKTOK_USERNAME')
        self.password = os.getenv('TIKTOK_PASSWORD')
        # Some implementations might need a session id or cookies instead
        self.session_id = os.getenv('TIKTOK_SESSION_ID')
        self.api = None
        
    def login(self):
        try:
            # Initialize with session id
            self.api = TikTokApi()
            self.api.session_id = self.session_id
            print("Successfully initialized TikTok API!")
        except Exception as e:
            print(f"Failed to initialize TikTok API: {str(e)}")
            
    def get_liked_media(self):
        try:
            # Get user's liked videos using the current API method
            user_data = self.api.user(username=self.username)
            liked_videos = user_data.liked.videos(count=50)
            
            formatted_videos = []
            for video in liked_videos:
                video_info = {
                    'id': video.id,
                    'share_url': f"https://www.tiktok.com/@{video.author.username}/video/{video.id}",
                    'author': video.author.username,
                    'caption': video.desc
                }
                formatted_videos.append(video_info)
            
            return formatted_videos
        except Exception as e:
            print(f"Error fetching liked media: {str(e)}")
            return []
