import facebook
from app.services.facebook_client import FacebookClient

def test_facebook_connection():
    """Test connection to Facebook API"""
    print("Testing Facebook client connection...")
    try:
        client = FacebookClient()
        me = client.graph.get_object('me')
        print(f"Connected as: {me}")
        return True
    except Exception as e:
        print(f"Error connecting to Facebook: {e}")
        return False

if __name__ == "__main__":
    test_facebook_connection()
