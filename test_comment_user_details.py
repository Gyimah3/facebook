import requests
import json
import sys
from loguru import logger

# Configure logger
logger.remove()
logger.add(sys.stdout, format="{time} | {level} | {message}")
logger.add("logs/comment_user_test.log", rotation="10 MB", level="INFO")

# Base URL for the API
BASE_URL = "http://localhost:8000/api/v1/facebook"

def test_comment_user_details():
    """Test the enhanced comment user details functionality"""
    logger.info("Starting comment user details test")
    
    # Get posts to find comments
    logger.info("Getting posts to find comments")
    response = requests.get(f"{BASE_URL}/posts", params={"limit": 10})
    
    if response.status_code != 200:
        logger.error(f"Failed to get posts: {response.status_code}")
        logger.error(f"Response: {response.text}")
        return
    
    posts = response.json()
    
    if not posts or "data" not in posts or not posts["data"]:
        logger.error("No posts found")
        return
    
    # Check each post for comments
    for post in posts["data"]:
        post_id = post["id"]
        logger.info(f"Checking comments for post {post_id}")
        
        response = requests.get(f"{BASE_URL}/posts/{post_id}/comments")
        
        if response.status_code != 200:
            logger.error(f"Failed to get comments for post {post_id}: {response.status_code}")
            logger.error(f"Response: {response.text}")
            continue
        
        comments = response.json()
        
        if not comments or "data" not in comments or not comments["data"]:
            logger.info(f"No comments found for post {post_id}")
            continue
        
        # Check each comment for user details
        logger.info(f"Found {len(comments['data'])} comments for post {post_id}")
        
        for comment in comments["data"]:
            comment_id = comment["id"]
            
            # Check if from field exists and has name
            if "from" not in comment:
                logger.error(f"Comment {comment_id} is missing 'from' field")
                continue
                
            if not comment["from"]:
                logger.error(f"Comment {comment_id} has empty 'from' field")
                continue
                
            if "name" not in comment["from"]:
                logger.error(f"Comment {comment_id} is missing user name")
                continue
                
            # Log success with user name
            logger.info(f"✅ Comment {comment_id} has user name: {comment['from']['name']}")
            
            # Check for picture
            if "picture" in comment["from"]:
                logger.info(f"  User has picture: {comment['from']['picture'] is not None}")
            else:
                logger.info(f"  User is missing picture")
    
    logger.info("Comment user details test completed")

if __name__ == "__main__":
    test_comment_user_details()
