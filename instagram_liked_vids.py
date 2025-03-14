class InstagramLikedVideos:
    def __init__(self, username=None, password=None):
        if username is None or password is None:
            load_dotenv()
            self.username = os.getenv('INSTAGRAM_USERNAME')
            self.password = os.getenv('INSTAGRAM_PASSWORD')
        else:
            self.username = username
            self.password = password
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