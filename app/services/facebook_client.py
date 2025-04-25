import facebook
from loguru import logger
from app.core.config import FACEBOOK_ACCESS_TOKEN, FACEBOOK_API_VERSION

class FacebookClient:
    """
    Client for interacting with the Facebook Graph API using the facebook-sdk package.
    """
    
    def __init__(self, access_token=None, version=None):
        """
        Initialize the Facebook Graph API client.
        
        Args:
            access_token (str, optional): Facebook access token. Defaults to the one in config.
            version (str, optional): Facebook API version. Defaults to the one in config.
        """
        self.access_token = access_token or FACEBOOK_ACCESS_TOKEN
        self.version = version or FACEBOOK_API_VERSION
        self.graph = facebook.GraphAPI(access_token=self.access_token, version=self.version)
        logger.info(f"Facebook client initialized with API version {self.version}")
    
    def get_page_info(self, page_id="me", fields=None):
        """
        Get detailed information about a Facebook page.
        
        Args:
            page_id (str, optional): ID of the page. Defaults to "me".
            fields (list, optional): List of fields to retrieve. Defaults to None.
            
        Returns:
            dict: Dictionary containing page information.
        """
        if fields is None:
            fields = ["id", "name", "about", "category", "fan_count", "link", "picture", "website"]
        
        try:
            page_info = self.graph.get_object(
                id=page_id,
                fields=",".join(fields)
            )
            logger.info(f"Retrieved page info for {page_id}")
            return page_info
        except facebook.GraphAPIError as e:
            logger.error(f"Error retrieving page info: {str(e)}")
            raise
    
    def get_page_posts(self, page_id="me", limit=10, fields=None):
        """
        Get posts from a Facebook page.
        
        Args:
            page_id (str, optional): ID of the page. Defaults to "me".
            limit (int, optional): Maximum number of posts to retrieve. Defaults to 10.
            fields (list, optional): List of fields to retrieve. Defaults to None.
            
        Returns:
            dict: Dictionary containing posts data.
        """
        if fields is None:
            fields = ["id", "message", "created_time", "permalink_url", "likes.summary(true)", "comments.summary(true)", "shares", "attachments"]
        
        try:
            posts = self.graph.get_connections(
                id=page_id,
                connection_name="posts",
                fields=",".join(fields),
                limit=limit
            )
            logger.info(f"Retrieved {len(posts.get('data', []))} posts from page {page_id}")
            return posts
        except facebook.GraphAPIError as e:
            logger.error(f"Error retrieving posts: {str(e)}")
            raise
    
    def get_post_details(self, post_id, fields=None):
        """
        Get details of a specific post.
        
        Args:
            post_id (str): ID of the post.
            fields (list, optional): List of fields to retrieve. Defaults to None.
            
        Returns:
            dict: Dictionary containing post details.
        """
        if fields is None:
            fields = ["id", "message", "created_time", "permalink_url", "likes.summary(true)", "comments.summary(true)", "shares", "attachments"]
        
        try:
            post = self.graph.get_object(
                id=post_id,
                fields=",".join(fields)
            )
            logger.info(f"Retrieved details for post {post_id}")
            return post
        except facebook.GraphAPIError as e:
            logger.error(f"Error retrieving post details: {str(e)}")
            raise
    
    def get_post_comments(self, post_id, limit=25, fields=None):
        """
        Get comments on a specific post with detailed user information.
        
        Args:
            post_id (str): ID of the post.
            limit (int, optional): Maximum number of comments to retrieve. Defaults to 25.
            fields (list, optional): List of fields to retrieve. Defaults to None.
            
        Returns:
            dict: Dictionary containing comments data with user details.
        """
        if fields is None:
            fields = ["id", "message", "created_time", "from{id,name,picture,link}", "like_count"]
        
        try:
            comments = self.graph.get_connections(
                id=post_id,
                connection_name="comments",
                fields=",".join(fields),
                limit=limit
            )
            logger.info(f"Retrieved {len(comments.get('data', []))} comments for post {post_id}")
            
            # Process user details for each comment
            if "data" in comments:
                for comment in comments["data"]:
                    # Ensure 'from' field is properly formatted
                    if "from" in comment and isinstance(comment["from"], dict):
                        user = comment["from"]
                        # Add additional user details if available
                        if "id" in user:
                            try:
                                # Try to get additional user details if permissions allow
                                user_details = self.graph.get_object(
                                    id=user["id"],
                                    fields="id,name,picture.type(large),link,email"
                                )
                                # Update user info with additional details
                                comment["from"].update(user_details)
                            except Exception as e:
                                # If we can't get additional details, continue with what we have
                                logger.warning(f"Could not get additional details for user {user.get('id')}: {str(e)}")
            
            return comments
        except facebook.GraphAPIError as e:
            logger.error(f"Error retrieving comments: {str(e)}")
            raise
    
    def get_post_likes(self, post_id, limit=25, fields=None):
        """
        Get likes on a specific post with detailed user information.
        
        Args:
            post_id (str): ID of the post.
            limit (int, optional): Maximum number of likes to retrieve. Defaults to 25.
            fields (list, optional): List of fields to retrieve. Defaults to None.
            
        Returns:
            dict: Dictionary containing likes data with user details.
        """
        if fields is None:
            fields = ["id", "name", "picture", "link"]
        
        try:
            likes = self.graph.get_connections(
                id=post_id,
                connection_name="likes",
                fields=",".join(fields),
                limit=limit
            )
            logger.info(f"Retrieved {len(likes.get('data', []))} likes for post {post_id}")
            
            # Process user details for each like
            if "data" in likes:
                for like in likes["data"]:
                    # Try to get additional user details if permissions allow
                    if "id" in like:
                        try:
                            user_details = self.graph.get_object(
                                id=like["id"],
                                fields="id,name,picture.type(large),link,email"
                            )
                            # Update user info with additional details
                            like.update(user_details)
                        except Exception as e:
                            # If we can't get additional details, continue with what we have
                            logger.warning(f"Could not get additional details for user {like.get('id')}: {str(e)}")
            
            return likes
        except facebook.GraphAPIError as e:
            logger.error(f"Error retrieving likes: {str(e)}")
            raise
    
    def get_page_fans(self, page_id="me", limit=25):
        """
        Get fans/followers count for a Facebook page using insights.
        
        Args:
            page_id (str, optional): ID of the page. Defaults to "me".
            limit (int, optional): Maximum number of data points to retrieve. Defaults to 25.
            
        Returns:
            dict: Dictionary containing page fans data.
        """
        try:
            # Use insights/page_fans to get follower count data
            fans = self.graph.get_connections(
                id=page_id,
                connection_name="insights",
                metric="page_fans",
                limit=limit
            )
            logger.info(f"Retrieved page fans data for page {page_id}")
            return fans
        except facebook.GraphAPIError as e:
            logger.error(f"Error retrieving page fans: {str(e)}")
            raise
    
    def get_page_mentions(self, page_id="me", limit=25, fields=None):
        """
        Get tagged posts/mentions of a Facebook page.
        
        Args:
            page_id (str, optional): ID of the page. Defaults to "me".
            limit (int, optional): Maximum number of mentions to retrieve. Defaults to 25.
            fields (list, optional): List of fields to retrieve. Defaults to None.
            
        Returns:
            dict: Dictionary containing tagged posts data.
        """
        if fields is None:
            fields = ["id", "message", "created_time", "from", "story"]
        
        try:
            # Use tagged connection to get posts where the page is tagged
            tagged = self.graph.get_connections(
                id=page_id,
                connection_name="tagged",
                fields=",".join(fields),
                limit=limit
            )
            logger.info(f"Retrieved {len(tagged.get('data', []))} tagged posts for page {page_id}")
            return tagged
        except facebook.GraphAPIError as e:
            logger.error(f"Error retrieving tagged posts: {str(e)}")
            raise
            
    def get_page_conversations(self, page_id="me", limit=25, fields=None):
        """
        Get conversations for a Facebook page.
        
        Args:
            page_id (str, optional): ID of the page. Defaults to "me".
            limit (int, optional): Maximum number of conversations to retrieve. Defaults to 25.
            fields (list, optional): List of fields to retrieve. Defaults to None.
            
        Returns:
            dict: Dictionary containing conversations data.
        """
        if fields is None:
            fields = ["id", "link", "updated_time", "messages.limit(10){message,from,created_time}"]
        
        try:
            conversations = self.graph.get_connections(
                id=page_id,
                connection_name="conversations",
                fields=",".join(fields),
                limit=limit
            )
            logger.info(f"Retrieved {len(conversations.get('data', []))} conversations for page {page_id}")
            return conversations
        except facebook.GraphAPIError as e:
            logger.error(f"Error retrieving conversations: {str(e)}")
            raise
            
    def get_page_insights(self, page_id="me", metrics=None, period="day", limit=25):
        """
        Get insights/analytics for a Facebook page.
        
        Args:
            page_id (str, optional): ID of the page. Defaults to "me".
            metrics (list, optional): List of metrics to retrieve. Defaults to None.
            period (str, optional): Time period for metrics. Defaults to "day".
            limit (int, optional): Maximum number of data points to retrieve. Defaults to 25.
            
        Returns:
            dict: Dictionary containing page insights data.
        """
        if metrics is None:
            metrics = [
                "page_impressions", 
                "page_engaged_users", 
                "page_post_engagements", 
                "page_fans",
                "page_views_total"
            ]
        
        try:
            insights = self.graph.get_connections(
                id=page_id,
                connection_name="insights",
                metric=",".join(metrics),
                period=period,
                limit=limit
            )
            logger.info(f"Retrieved page insights for page {page_id}")
            return insights
        except facebook.GraphAPIError as e:
            logger.error(f"Error retrieving page insights: {str(e)}")
            raise
            
    def search_page_feed(self, page_id="me", query=None, limit=25, fields=None):
        """
        Search for posts in a page's feed.
        
        Args:
            page_id (str, optional): ID of the page. Defaults to "me".
            query (str, optional): Search query. Defaults to None.
            limit (int, optional): Maximum number of results to retrieve. Defaults to 25.
            fields (list, optional): List of fields to retrieve. Defaults to None.
            
        Returns:
            dict: Dictionary containing search results.
        """
        if fields is None:
            fields = ["id", "message", "created_time", "from", "permalink_url"]
        
        try:
            # If query is provided, use it to filter posts
            if query:
                # First get all posts
                posts = self.get_page_posts(page_id=page_id, limit=limit*2, fields=fields)
                
                # Then filter locally by query
                if "data" in posts:
                    filtered_posts = []
                    for post in posts["data"]:
                        if "message" in post and query.lower() in post["message"].lower():
                            filtered_posts.append(post)
                    
                    # Limit results
                    filtered_posts = filtered_posts[:limit]
                    
                    # Create a new response with filtered data
                    result = {
                        "data": filtered_posts,
                        "paging": posts.get("paging", {})
                    }
                    
                    logger.info(f"Found {len(filtered_posts)} posts matching query '{query}'")
                    return result
                return posts
            else:
                # If no query, just return posts
                return self.get_page_posts(page_id=page_id, limit=limit, fields=fields)
        except facebook.GraphAPIError as e:
            logger.error(f"Error searching page feed: {str(e)}")
            raise
