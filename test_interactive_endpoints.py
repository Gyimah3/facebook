import requests
import json
import sys
from loguru import logger

# Configure logger
logger.remove()
logger.add(sys.stdout, format="{time} | {level} | {message}")
logger.add("logs/interactive_test.log", rotation="10 MB", level="INFO")

# Base URL for the API
BASE_URL = "http://localhost:8000/api/v1/facebook"

def test_endpoint(endpoint, method="GET", params=None, data=None, expected_status=200):
    """Test an API endpoint and log the result"""
    url = f"{BASE_URL}/{endpoint}"
    logger.info(f"Testing {method} endpoint: {url}")
    
    try:
        if method == "GET":
            response = requests.get(url, params=params)
        elif method == "POST":
            response = requests.post(url, json=data)
        else:
            logger.error(f"Unsupported method: {method}")
            return None
            
        status_code = response.status_code
        
        if status_code == expected_status:
            logger.info(f"✅ Success: {method} {endpoint} - Status: {status_code}")
            try:
                data = response.json()
                logger.info(f"   Response: {json.dumps(data, indent=2)[:200]}...")
                return data
            except:
                logger.info(f"   Response: {response.text[:100]}...")
                return response.text
        else:
            logger.error(f"❌ Failed: {method} {endpoint} - Status: {status_code}")
            logger.error(f"   Response: {response.text}")
            return None
    except Exception as e:
        logger.error(f"❌ Error testing {method} {endpoint}: {str(e)}")
        return None

def run_interactive_tests():
    """Run tests for all interactive API endpoints"""
    logger.info("Starting interactive API endpoint tests")
    
    # Test getting page info
    page_info = test_endpoint("page-info")
    if not page_info:
        logger.error("Failed to get page info, stopping tests")
        return
        
    logger.info(f"Testing with page: {page_info.get('name', 'Unknown')} (ID: {page_info.get('id', 'Unknown')})")
    
    # Test creating a text post
    text_post_data = {
        "message": "This is a test post from the Facebook API client. Testing interactive features."
    }
    text_post_response = test_endpoint("posts", method="POST", data=text_post_data)
    
    # If post creation was successful, get the post ID for further tests
    post_id = None
    if text_post_response and text_post_response.get("success"):
        post_id = text_post_response.get("post_id")
        logger.info(f"Created post with ID: {post_id}")
    
    # Test creating an image post with URL
    image_post_data = {
        "message": "This is a test image post from the Facebook API client.",
        "image_url": "https://images.pexels.com/photos/736230/pexels-photo-736230.jpeg"
    }
    image_post_response = test_endpoint("posts/image", method="POST", data=image_post_data)
    
    # Test getting conversations
    conversations = test_endpoint("conversations", params={"limit": 5})
    
    # If we have conversations, test replying to the first one
    conversation_id = None
    if conversations and "data" in conversations and len(conversations["data"]) > 0:
        conversation_id = conversations["data"][0]["id"]
        logger.info(f"Testing with conversation ID: {conversation_id}")
        
        # Test replying to a conversation
        reply_data = {
            "message": "This is an automated test reply from the Facebook API client."
        }
        reply_response = test_endpoint(f"conversations/{conversation_id}/reply", method="POST", data=reply_data)
    
    # Test getting posts to find comments
    posts = test_endpoint("posts", params={"limit": 10})
    
    # If we have posts, look for comments to test comment interactions
    if posts and "data" in posts and len(posts["data"]) > 0:
        # Try to find a post with comments
        for post in posts["data"]:
            post_id = post["id"]
            comments = test_endpoint(f"posts/{post_id}/comments")
            
            if comments and "data" in comments and len(comments["data"]) > 0:
                comment_id = comments["data"][0]["id"]
                logger.info(f"Testing with comment ID: {comment_id}")
                
                # Test liking a comment
                like_response = test_endpoint(f"comments/{comment_id}/like", method="POST", data={})
                
                # Test replying to a comment
                comment_reply_data = {
                    "message": "This is an automated test reply to a comment from the Facebook API client."
                }
                comment_reply_response = test_endpoint(f"comments/{comment_id}/reply", method="POST", data=comment_reply_data)
                
                # We found and tested a comment, no need to check more posts
                break
    
    logger.info("Interactive API endpoint tests completed")

if __name__ == "__main__":
    run_interactive_tests()
