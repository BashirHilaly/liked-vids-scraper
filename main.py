from instagram_private_api import Client, ClientCompatPatch
import json
import os
from dotenv import load_dotenv
from instagram_liked_vids import InstagramLikedVideos
from tiktok_liked_vids import TikTokLikedVideos
import asyncio

# Update the main block to use share URLs
if __name__ == "__main__":
    username = input("Enter your Instagram username: ")
    password = input("Enter your Instagram password: ")
    scraper = InstagramLikedVideos(username, password)
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
    