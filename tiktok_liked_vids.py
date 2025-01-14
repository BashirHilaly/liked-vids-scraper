from TikTokApi import TikTokApi
import os
from dotenv import load_dotenv
import asyncio

class TikTokLikedVideos:
    def __init__(self):
        load_dotenv()
        self.username = os.getenv('TIKTOK_USERNAME')
        self.password = os.getenv('TIKTOK_PASSWORD')
        # Some implementations might need a session id or cookies instead
        self.ms_token = os.getenv('TIKTOK_MS_TOKEN')
        self.api = None

    async def user_example():
        async with TikTokApi() as api:
            await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
            user = api.user("therock")
            user_data = await user.info()
            print(user_data)

            async for video in user.videos(count=30):
                print(video)
                print(video.as_dict)

            async for playlist in user.playlists():
                print(playlist)

        
    def login(self):
        try:
            # Initialize with session id
            self.api = TikTokApi()
            self.api.session_id = self.session_id
            print("Successfully initialized TikTok API!")
        except Exception as e:
            print(f"Failed to initialize TikTok API: {str(e)}")
            
    async def get_liked_media(self):
        try:
            # Get user's liked videos using the current API method
            async with self.api.create_user(username=self.username) as user:
                user_data = await user.info()
                liked_videos = await user.favorites(count=50)
                
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
