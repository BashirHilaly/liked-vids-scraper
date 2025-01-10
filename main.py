from instagram_private_api import Client, ClientCompatPatch
import json
import os
from dotenv import load_dotenv

class InstagramLikedVideos:
    def __init__(self):
        load_dotenv()
        self.username = os.getenv('INSTAGRAM_USERNAME')
        self.password = os.getenv('INSTAGRAM_PASSWORD')
        self.api = None
        
    def login(self):
        try:
            self.api = Client(self.username, self.password)
            print("Successfully logged in!")
        except Exception as e:
            print(f"Failed to login: {str(e)}")
            
    def get_liked_media(self, max_count=50):
        if not self.api:
            print("Please login first!")
            return []
            
        try:
            liked_media = []
            results = self.api.feed_liked()
            
            # Debug the API response
            print("API Response:", json.dumps(results, indent=2))
            
            if not results or 'items' not in results:
                print("No items found in the API response")
                return []
            
            items = results.get('items', [])
            
            for item in items:
                if not item:
                    continue
                    
                media_type = item.get('media_type')
                if media_type == 2:  # Type 2 represents video
                    try:
                        code = item.get('code')  # This is the shortcode used in Instagram URLs
                        video_data = {
                            'id': item.get('id', 'No ID'),
                            'caption': item.get('caption', {}).get('text', 'No caption'),
                            'share_url': f'https://www.instagram.com/p/{code}/',
                            'thumbnail': None
                        }
                        
                        # Safely get thumbnail
                        image_versions = item.get('image_versions2', {}).get('candidates', [])
                        if image_versions and len(image_versions) > 0:
                            video_data['thumbnail'] = image_versions[0].get('url')
                        
                        liked_media.append(video_data)
                    except Exception as e:
                        print(f"Error processing video item: {str(e)}")
                        continue
                    
                if len(liked_media) >= max_count:
                    break
                    
            return liked_media
            
        except Exception as e:
            print(f"Error fetching liked media: {str(e)}")
            return []

# Update the main block to use share URLs
if __name__ == "__main__":
    scraper = InstagramLikedVideos()
    scraper.login()
    liked_videos = scraper.get_liked_media()

    # Write video links to a file
    with open('liked_videos.txt', 'w', encoding='utf-8') as f:
        for video in liked_videos:
            f.write(f"Share URL: {video['share_url']}\n")
            f.write(f"Caption: {video['caption'][:100]}...\n")
            f.write('-' * 50 + '\n')
    
    # Print results
    for video in liked_videos:
        print(f"Video ID: {video['id']}")
        print(f"Caption: {video['caption'][:100]}...")
        print(f"Share URL: {video['share_url']}")
        print("-" * 50)