from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List
from app.services.facebook_client import FacebookClient
from app.models.schemas import (
    PostResponse, CommentResponse, LikeResponse, 
    FollowResponse, MentionResponse, ConversationResponse, ErrorResponse
)
from loguru import logger

router = APIRouter()

def get_facebook_client():
    """Dependency to get Facebook client instance"""
    try:
        return FacebookClient()
    except Exception as e:
        logger.error(f"Failed to initialize Facebook client: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Facebook client initialization error: {str(e)}")

@router.get("/page-info", responses={500: {"model": ErrorResponse}})
async def get_page_info(
    page_id: str = "me",
    client: FacebookClient = Depends(get_facebook_client)
):
    """
    Get detailed information about a Facebook page.
    
    - **page_id**: ID of the Facebook page (defaults to authenticated user's page)
    """
    try:
        page_info = client.get_page_info(page_id=page_id)
        return page_info
    except Exception as e:
        logger.error(f"Error retrieving page info: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving page info: {str(e)}")

@router.get("/posts", response_model=PostResponse, responses={500: {"model": ErrorResponse}})
async def get_posts(
    page_id: str = "me",
    limit: int = Query(10, ge=1, le=100),
    client: FacebookClient = Depends(get_facebook_client)
):
    """
    Get posts from a Facebook page.
    
    - **page_id**: ID of the Facebook page (defaults to authenticated user's page)
    - **limit**: Maximum number of posts to retrieve (1-100)
    """
    try:
        posts = client.get_page_posts(page_id=page_id, limit=limit)
        return posts
    except Exception as e:
        logger.error(f"Error retrieving posts: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving posts: {str(e)}")

@router.get("/posts/{post_id}", responses={500: {"model": ErrorResponse}})
async def get_post_details(
    post_id: str,
    client: FacebookClient = Depends(get_facebook_client)
):
    """
    Get details of a specific post.
    
    - **post_id**: ID of the Facebook post
    """
    try:
        post = client.get_post_details(post_id=post_id)
        return post
    except Exception as e:
        logger.error(f"Error retrieving post details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving post details: {str(e)}")

@router.get("/posts/{post_id}/comments", response_model=CommentResponse, responses={500: {"model": ErrorResponse}})
async def get_post_comments(
    post_id: str,
    limit: int = Query(25, ge=1, le=100),
    client: FacebookClient = Depends(get_facebook_client)
):
    """
    Get comments on a specific post with detailed user information.
    
    - **post_id**: ID of the Facebook post
    - **limit**: Maximum number of comments to retrieve (1-100)
    """
    try:
        comments = client.get_post_comments(post_id=post_id, limit=limit)
        
        # Add post_id to each comment for reference
        if "data" in comments:
            for comment in comments["data"]:
                comment["post_id"] = post_id
                
        return comments
    except Exception as e:
        logger.error(f"Error retrieving comments: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving comments: {str(e)}")

@router.get("/posts/{post_id}/likes", response_model=LikeResponse, responses={500: {"model": ErrorResponse}})
async def get_post_likes(
    post_id: str,
    limit: int = Query(25, ge=1, le=100),
    client: FacebookClient = Depends(get_facebook_client)
):
    """
    Get likes on a specific post with detailed user information.
    
    - **post_id**: ID of the Facebook post
    - **limit**: Maximum number of likes to retrieve (1-100)
    """
    try:
        likes = client.get_post_likes(post_id=post_id, limit=limit)
        
        # Add post_id to each like for reference
        if "data" in likes:
            for like in likes["data"]:
                like["post_id"] = post_id
                
        return likes
    except Exception as e:
        logger.error(f"Error retrieving likes: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving likes: {str(e)}")

@router.get("/fans", responses={500: {"model": ErrorResponse}})
async def get_page_fans(
    page_id: str = "me",
    limit: int = Query(25, ge=1, le=100),
    client: FacebookClient = Depends(get_facebook_client)
):
    """
    Get fans/followers count for a Facebook page.
    
    - **page_id**: ID of the Facebook page (defaults to authenticated user's page)
    - **limit**: Maximum number of data points to retrieve (1-100)
    """
    try:
        fans = client.get_page_fans(page_id=page_id, limit=limit)
        return fans
    except Exception as e:
        logger.error(f"Error retrieving fans: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving fans: {str(e)}")

@router.get("/mentions", response_model=MentionResponse, responses={500: {"model": ErrorResponse}})
async def get_page_mentions(
    page_id: str = "me",
    limit: int = Query(25, ge=1, le=100),
    client: FacebookClient = Depends(get_facebook_client)
):
    """
    Get tagged posts/mentions of a Facebook page.
    
    - **page_id**: ID of the Facebook page (defaults to authenticated user's page)
    - **limit**: Maximum number of mentions to retrieve (1-100)
    """
    try:
        mentions = client.get_page_mentions(page_id=page_id, limit=limit)
        return mentions
    except Exception as e:
        logger.error(f"Error retrieving mentions: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving mentions: {str(e)}")

@router.get("/conversations", response_model=ConversationResponse, responses={500: {"model": ErrorResponse}})
async def get_page_conversations(
    page_id: str = "me",
    limit: int = Query(25, ge=1, le=100),
    client: FacebookClient = Depends(get_facebook_client)
):
    """
    Get conversations for a Facebook page with message history.
    
    - **page_id**: ID of the Facebook page (defaults to authenticated user's page)
    - **limit**: Maximum number of conversations to retrieve (1-100)
    """
    try:
        conversations = client.get_page_conversations(page_id=page_id, limit=limit)
        return conversations
    except Exception as e:
        logger.error(f"Error retrieving conversations: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving conversations: {str(e)}")

@router.get("/conversations/{conversation_id}", responses={500: {"model": ErrorResponse}})
async def get_conversation_details(
    conversation_id: str,
    limit: int = Query(25, ge=1, le=100),
    client: FacebookClient = Depends(get_facebook_client)
):
    """
    Get detailed messages for a specific conversation.
    
    - **conversation_id**: ID of the Facebook conversation
    - **limit**: Maximum number of messages to retrieve (1-100)
    """
    try:
        # Get conversation details with messages
        fields = [
            "id", 
            "link", 
            "updated_time", 
            f"messages.limit({limit}){{message,from{{id,name,picture}},created_time}}"
        ]
        
        conversation = client.graph.get_object(
            id=conversation_id,
            fields=",".join(fields)
        )
        
        logger.info(f"Retrieved details for conversation {conversation_id}")
        return conversation
    except Exception as e:
        logger.error(f"Error retrieving conversation details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving conversation details: {str(e)}")

@router.get("/insights", responses={500: {"model": ErrorResponse}})
async def get_page_insights(
    page_id: str = "me",
    metrics: List[str] = Query(["page_impressions", "page_engaged_users", "page_fans"]),
    period: str = Query("day", regex="^(day|week|month|lifetime)$"),
    limit: int = Query(25, ge=1, le=100),
    client: FacebookClient = Depends(get_facebook_client)
):
    """
    Get insights/analytics for a Facebook page.
    
    - **page_id**: ID of the Facebook page (defaults to authenticated user's page)
    - **metrics**: List of metrics to retrieve
    - **period**: Time period for metrics (day, week, month, lifetime)
    - **limit**: Maximum number of data points to retrieve (1-100)
    """
    try:
        insights = client.get_page_insights(
            page_id=page_id,
            metrics=metrics,
            period=period,
            limit=limit
        )
        return insights
    except Exception as e:
        logger.error(f"Error retrieving page insights: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving page insights: {str(e)}")

@router.get("/search", responses={500: {"model": ErrorResponse}})
async def search_page_feed(
    query: str,
    page_id: str = "me",
    limit: int = Query(25, ge=1, le=100),
    client: FacebookClient = Depends(get_facebook_client)
):
    """
    Search for posts in a page's feed.
    
    - **query**: Search query
    - **page_id**: ID of the Facebook page (defaults to authenticated user's page)
    - **limit**: Maximum number of results to retrieve (1-100)
    """
    try:
        search_results = client.search_page_feed(
            page_id=page_id,
            query=query,
            limit=limit
        )
        return search_results
    except Exception as e:
        logger.error(f"Error searching page feed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error searching page feed: {str(e)}")
