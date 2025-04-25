import requests
import json
import sys
from loguru import logger

# Configure logger
logger.remove()
logger.add(sys.stdout, format="{time} | {level} | {message}")
logger.add("logs/api_test.log", rotation="10 MB", level="INFO")

# Base URL for the API
BASE_URL = "http://localhost:8000/api/v1/facebook"

def test_endpoint(endpoint, params=None, expected_status=200):
    """Test an API endpoint and log the result"""
    url = f"{BASE_URL}/{endpoint}"
    logger.info(f"Testing endpoint: {url}")
    
    try:
        response = requests.get(url, params=params)
        status_code = response.status_code
        
        if status_code == expected_status:
            logger.info(f"✅ Success: {endpoint} - Status: {status_code}")
            try:
                data = response.json()
                if "data" in data:
                    logger.info(f"   Data count: {len(data['data'])}")
                return data
            except:
                logger.info(f"   Response: {response.text[:100]}...")
                return response.text
        else:
            logger.error(f"❌ Failed: {endpoint} - Status: {status_code}")
            logger.error(f"   Response: {response.text}")
            return None
    except Exception as e:
        logger.error(f"❌ Error testing {endpoint}: {str(e)}")
        return None

def run_tests():
    """Run tests for all API endpoints"""
    logger.info("Starting API endpoint tests")
    
    # Test page info endpoint
    page_info = test_endpoint("page-info")
    
    # Test posts endpoint
    posts = test_endpoint("posts", {"limit": 5})
    
    # If we have posts, test post-specific endpoints
    post_id = None
    if posts and "data" in posts and len(posts["data"]) > 0:
        post_id = posts["data"][0]["id"]
        logger.info(f"Using post ID for further tests: {post_id}")
        
        # Test post details
        test_endpoint(f"posts/{post_id}")
        
        # Test post comments
        test_endpoint(f"posts/{post_id}/comments")
        
        # Test post likes
        test_endpoint(f"posts/{post_id}/likes")
    
    # Test fans endpoint
    test_endpoint("fans")
    
    # Test mentions endpoint
    test_endpoint("mentions")
    
    # Test conversations endpoint
    conversations = test_endpoint("conversations", {"limit": 5})
    
    # If we have conversations, test conversation-specific endpoints
    if conversations and "data" in conversations and len(conversations["data"]) > 0:
        conversation_id = conversations["data"][0]["id"]
        logger.info(f"Using conversation ID for further tests: {conversation_id}")
        
        # Test conversation details
        test_endpoint(f"conversations/{conversation_id}")
    
    # Test insights endpoint
    test_endpoint("insights", {"metrics": ["page_impressions", "page_fans"]})
    
    # Test search endpoint
    if post_id:
        # Extract a word from the first post to search for
        post_message = posts["data"][0].get("message", "")
        if post_message:
            search_term = post_message.split()[0] if len(post_message.split()) > 0 else ""
            if search_term:
                logger.info(f"Searching for term: {search_term}")
                test_endpoint("search", {"query": search_term})
    
    logger.info("API endpoint tests completed")

if __name__ == "__main__":
    run_tests()
