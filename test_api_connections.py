import facebook
from app.services.facebook_client import FacebookClient

def test_facebook_api_connections():
    """Test various Facebook API connections to identify available endpoints"""
    print("Testing Facebook API connections...")
    
    try:
        client = FacebookClient()
        
        # Get page info
        print("\nTesting page info:")
        page = client.graph.get_object('me')
        print(f"Page info: {page}")
        
        # Test individual connections
        print("\nTesting feed:")
        try:
            feed = client.graph.get_connections('me', 'feed', limit=5)
            print(f"Feed: {feed}")
        except Exception as e:
            print(f"Feed error: {e}")
        
        print("\nTesting tagged:")
        try:
            tagged = client.graph.get_connections('me', 'tagged', limit=5)
            print(f"Tagged: {tagged}")
        except Exception as e:
            print(f"Tagged error: {e}")
        
        print("\nTesting mentions:")
        try:
            mentions = client.graph.get_connections('me', 'mentions', limit=5)
            print(f"Mentions: {mentions}")
        except Exception as e:
            print(f"Mentions error: {e}")
        
        print("\nTesting followers/fans:")
        try:
            followers = client.graph.get_connections('me', 'followers', limit=5)
            print(f"Followers: {followers}")
        except Exception as e:
            print(f"Followers error: {e}")
        
        try:
            fans = client.graph.get_connections('me', 'fans', limit=5)
            print(f"Fans: {fans}")
        except Exception as e:
            print(f"Fans error: {e}")
        
        # Test page insights
        print("\nTesting page_fans:")
        try:
            page_fans = client.graph.get_connections('me', 'insights/page_fans')
            print(f"Page fans: {page_fans}")
        except Exception as e:
            print(f"Page fans error: {e}")
        
        # Test conversations
        print("\nTesting conversations:")
        try:
            conversations = client.graph.get_connections('me', 'conversations', limit=5)
            print(f"Conversations: {conversations}")
        except Exception as e:
            print(f"Conversations error: {e}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_facebook_api_connections()
