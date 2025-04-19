# server.py
import sys
import os
import json
import httpx
from typing import Dict, List, Optional, Any, Union
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Twitter MCP")

# Environment variables for Twitter configuration
TWITTER_BASE_URL = os.environ.get("TWITTER_BASE_URL", "https://api.twitter.com/2")
TWITTER_API_KEY = os.environ.get("TWITTER_API_KEY")
TWITTER_API_SECRET = os.environ.get("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.environ.get("TWITTER_ACCESS_SECRET")
TWITTER_BEARER_TOKEN = os.environ.get("TWITTER_BEARER_TOKEN")

# Check if environment variables are set
if not TWITTER_BEARER_TOKEN and not all([TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET]):
    print("Warning: Twitter environment variables not fully configured. Set TWITTER_BEARER_TOKEN or all of TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET.", file=sys.stderr)

# Helper function for API requests
async def make_twitter_request(method: str, endpoint: str, data: Dict = None, params: Dict = None) -> Dict:
    """
    Make a request to the Twitter API.
    
    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        endpoint: API endpoint (without base URL)
        data: Data to send (for POST/PUT)
        params: Query parameters (for GET)
    
    Returns:
        Response from Twitter API as dictionary
    """
    url = f"{TWITTER_BASE_URL}{endpoint}"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # Use Bearer token if available, otherwise use OAuth 1.0a credentials
    if TWITTER_BEARER_TOKEN:
        headers["Authorization"] = f"Bearer {TWITTER_BEARER_TOKEN}"
    
    async with httpx.AsyncClient() as client:
        try:
            if method.upper() == "GET":
                response = await client.get(url, headers=headers, params=params)
            elif method.upper() == "POST":
                response = await client.post(url, headers=headers, json=data)
            elif method.upper() == "PUT":
                response = await client.put(url, headers=headers, json=data)
            elif method.upper() == "DELETE":
                response = await client.delete(url, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {
                "error": True,
                "status_code": e.response.status_code,
                "message": e.response.text
            }
        except Exception as e:
            return {
                "error": True,
                "message": str(e)
            }

# === TOOLS ===

@mcp.tool()
async def get_user(username: str) -> str:
    """
    Get details of a specific Twitter user.
    
    Args:
        username: The Twitter username (without @)
    """
    params = {
        "user.fields": "description,profile_image_url,public_metrics,verified,location,created_at"
    }
    
    result = await make_twitter_request("GET", f"/users/by/username/{username}", params=params)
    
    if "error" in result:
        return f"Error retrieving user: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    user_data = result.get("data", {})
    formatted_result = {
        "username": f"@{username}",
        "name": user_data.get("name", "Unknown"),
        "id": user_data.get("id", "Unknown"),
        "description": user_data.get("description", ""),
        "location": user_data.get("location", ""),
        "verified": user_data.get("verified", False),
        "created_at": user_data.get("created_at", ""),
        "profile_image": user_data.get("profile_image_url", ""),
        "metrics": user_data.get("public_metrics", {})
    }
    
    return json.dumps(formatted_result, indent=2)

@mcp.tool()
async def get_tweet(tweet_id: str) -> str:
    """
    Get details of a specific tweet.
    
    Args:
        tweet_id: The Twitter tweet ID
    """
    params = {
        "tweet.fields": "created_at,author_id,public_metrics,entities,attachments,context_annotations,conversation_id,source"
    }
    
    result = await make_twitter_request("GET", f"/tweets/{tweet_id}", params=params)
    
    if "error" in result:
        return f"Error retrieving tweet: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.tool()
async def search_tweets(query: str, max_results: int = 10) -> str:
    """
    Search for tweets matching a query.
    
    Args:
        query: The search query
        max_results: Maximum number of results to return (default: 10, max: 100)
    """
    # Ensure max_results is within valid range
    max_results = min(max(1, max_results), 100)
    
    params = {
        "query": query,
        "max_results": max_results,
        "tweet.fields": "created_at,author_id,public_metrics",
        "expansions": "author_id",
        "user.fields": "username,name,profile_image_url"
    }
    
    result = await make_twitter_request("GET", "/tweets/search/recent", params=params)
    
    if "error" in result:
        return f"Error searching tweets: {result.get('message', 'Unknown error')}"
    
    # Process and format the results for better readability
    formatted_tweets = []
    
    tweets = result.get("data", [])
    users = {user["id"]: user for user in result.get("includes", {}).get("users", [])}
    
    for tweet in tweets:
        user = users.get(tweet.get("author_id", ""), {})
        formatted_tweet = {
            "id": tweet.get("id", ""),
            "text": tweet.get("text", ""),
            "created_at": tweet.get("created_at", ""),
            "metrics": tweet.get("public_metrics", {}),
            "author": {
                "username": f"@{user.get('username', 'unknown')}",
                "name": user.get("name", "Unknown"),
                "profile_image": user.get("profile_image_url", "")
            }
        }
        formatted_tweets.append(formatted_tweet)
    
    return json.dumps({"tweets": formatted_tweets}, indent=2)

@mcp.tool()
async def get_user_tweets(username: str, max_results: int = 10) -> str:
    """
    Get recent tweets from a specific user.
    
    Args:
        username: The Twitter username (without @)
        max_results: Maximum number of tweets to return (default: 10, max: 100)
    """
    # First get the user ID
    user_result = await make_twitter_request("GET", f"/users/by/username/{username}")
    
    if "error" in user_result:
        return f"Error finding user: {user_result.get('message', 'Unknown error')}"
    
    user_id = user_result.get("data", {}).get("id")
    if not user_id:
        return f"Could not find user ID for @{username}"
    
    # Ensure max_results is within valid range
    max_results = min(max(1, max_results), 100)
    
    params = {
        "max_results": max_results,
        "tweet.fields": "created_at,public_metrics",
        "exclude": "retweets,replies"
    }
    
    result = await make_twitter_request("GET", f"/users/{user_id}/tweets", params=params)
    
    if "error" in result:
        return f"Error retrieving tweets: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    tweets = result.get("data", [])
    formatted_tweets = []
    
    for tweet in tweets:
        formatted_tweet = {
            "id": tweet.get("id", ""),
            "text": tweet.get("text", ""),
            "created_at": tweet.get("created_at", ""),
            "metrics": tweet.get("public_metrics", {})
        }
        formatted_tweets.append(formatted_tweet)
    
    return json.dumps({"user": f"@{username}", "tweets": formatted_tweets}, indent=2)

@mcp.tool()
async def get_trending_topics(woeid: int = 1) -> str:
    """
    Get trending topics on Twitter.
    
    Args:
        woeid: The "Where On Earth ID" to get trends for (default: 1 - worldwide)
    """
    # Note: Twitter API v2 doesn't have direct trends endpoint, so we'll use v1.1
    v1_url = "https://api.twitter.com/1.1"
    
    headers = {"Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"}
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{v1_url}/trends/place.json?id={woeid}", headers=headers)
            response.raise_for_status()
            trends_data = response.json()
            
            if not trends_data or len(trends_data) == 0:
                return "No trending topics found"
            
            trends = trends_data[0].get("trends", [])
            formatted_trends = []
            
            for trend in trends:
                formatted_trend = {
                    "name": trend.get("name", ""),
                    "url": trend.get("url", ""),
                    "tweet_volume": trend.get("tweet_volume", "N/A")
                }
                formatted_trends.append(formatted_trend)
            
            return json.dumps({"trends": formatted_trends}, indent=2)
        
        except Exception as e:
            return f"Error retrieving trending topics: {str(e)}"

@mcp.tool()
async def post_tweet(text: str) -> str:
    """
    Post a new tweet.
    
    Args:
        text: The tweet text (max 280 characters)
    """
    # Check if text is within the character limit
    if len(text) > 280:
        return "Error: Tweet exceeds 280 character limit"
    
    # Check if we have the necessary authentication
    if not all([TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET]):
        return "Error: OAuth 1.0a credentials required for posting tweets. Please set TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, and TWITTER_ACCESS_SECRET."
    
    data = {
        "text": text
    }
    
    result = await make_twitter_request("POST", "/tweets", data=data)
    
    if "error" in result:
        return f"Error posting tweet: {result.get('message', 'Unknown error')}"
    
    return f"Tweet posted successfully! Tweet ID: {result.get('data', {}).get('id', 'unknown')}"

# === RESOURCES ===

@mcp.resource("twitter://user/{username}")
async def get_user_resource(username: str) -> str:
    """Get details about a Twitter user."""
    params = {
        "user.fields": "description,profile_image_url,public_metrics,verified,location,created_at,url"
    }
    
    result = await make_twitter_request("GET", f"/users/by/username/{username}", params=params)
    
    if "error" in result:
        return f"Error retrieving user: {result.get('message', 'Unknown error')}"
    
    return json.dumps(result, indent=2)

@mcp.resource("twitter://tweets/user/{username}")
async def get_user_tweets_resource(username: str) -> str:
    """Get recent tweets from a specific user."""
    # First get the user ID
    user_result = await make_twitter_request("GET", f"/users/by/username/{username}")
    
    if "error" in user_result:
        return f"Error finding user: {user_result.get('message', 'Unknown error')}"
    
    user_id = user_result.get("data", {}).get("id")
    if not user_id:
        return f"Could not find user ID for @{username}"
    
    params = {
        "max_results": 10,
        "tweet.fields": "created_at,public_metrics",
        "exclude": "retweets,replies"
    }
    
    result = await make_twitter_request("GET", f"/users/{user_id}/tweets", params=params)
    
    if "error" in result:
        return f"Error retrieving tweets: {result.get('message', 'Unknown error')}"
    
    return json.dumps(result, indent=2)

@mcp.resource("twitter://trends")
async def get_trends_resource() -> str:
    """Get current trending topics on Twitter."""
    # Note: Twitter API v2 doesn't have direct trends endpoint, so we'll use v1.1
    v1_url = "https://api.twitter.com/1.1"
    
    headers = {"Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"}
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{v1_url}/trends/place.json?id=1", headers=headers)
            response.raise_for_status()
            trends_data = response.json()
            
            return json.dumps(trends_data, indent=2)
        
        except Exception as e:
            return f"Error retrieving trending topics: {str(e)}"

# === PROMPTS ===

@mcp.prompt("draft_tweet")
def draft_tweet_prompt(topic: str = None, tone: str = None):
    """
    A prompt template for drafting a tweet.
    
    Args:
        topic: Topic to tweet about
        tone: Tone of the tweet (e.g., casual, professional, humorous)
    """
    if all([topic, tone]):
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"Please help me draft a tweet about {topic} with a {tone} tone. Keep it within 280 characters."
                    }
                }
            ]
        }
    elif topic:
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"Please help me draft a tweet about {topic}. Keep it within 280 characters."
                    }
                }
            ]
        }
    else:
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": "I need to draft a tweet. Please help me brainstorm some ideas and create a draft within 280 characters."
                    }
                }
            ]
        }

@mcp.prompt("analyze_trends")
def analyze_trends_prompt(trend: str = None):
    """
    A prompt template for analyzing Twitter trends.
    
    Args:
        trend: Specific trend to analyze
    """
    if trend:
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"Please analyze the Twitter trend '{trend}'. What might be driving this trend? What conversations are happening around it? How might it evolve?"
                    }
                }
            ]
        }
    else:
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": "Please help me understand what's trending on Twitter right now and why these topics might be gaining traction."
                    }
                }
            ]
        }

@mcp.prompt("engagement_strategy")
def engagement_strategy_prompt(audience: str = None, goal: str = None):
    """
    A prompt template for developing a Twitter engagement strategy.
    
    Args:
        audience: Target audience for engagement
        goal: Goal of the engagement strategy (e.g., brand awareness, community building)
    """
    if all([audience, goal]):
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"Please help me develop a Twitter engagement strategy for reaching {audience} with the goal of {goal}. Include content ideas, posting schedule, and engagement tactics."
                    }
                }
            ]
        }
    else:
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": "I need to improve my Twitter engagement. Please help me develop a strategy that includes content ideas, posting schedule, and engagement tactics."
                    }
                }
            ]
        }

if __name__ == "__main__":
    print("Starting Twitter MCP server...", file=sys.stderr)
    mcp.run()
