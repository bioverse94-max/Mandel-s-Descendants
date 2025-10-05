import requests
import os

# Hugging Face API configuration
HF_API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

def get_hf_token():
    """Get Hugging Face API token from environment variable."""
    return os.getenv("HF_API_TOKEN", None)

def summarize_text(text: str, max_len: int = 120, min_len: int = 30) -> str:
    """
    Summarize text using Hugging Face Inference API.
    No local model download required - uses cloud API.
    
    Args:
        text: Text to summarize
        max_len: Maximum length of summary
        min_len: Minimum length of summary
    
    Returns:
        Summarized text or truncated text if API fails
    """
    if not text or not text.strip():
        return "No content available to summarize."
    
    # Only summarize if text is long enough
    if len(text) < 100:
        return text
    
    # Get API token
    hf_token = get_hf_token()
    
    if not hf_token:
        print("⚠️ Warning: HF_API_TOKEN not set. Using fallback truncation.")
        print("   Get a free token at: https://huggingface.co/settings/tokens")
        return text[:500] + "..." if len(text) > 500 else text
    
    try:
        headers = {
            "Authorization": f"Bearer {hf_token}",
            "Content-Type": "application/json"
        }
        
        # Prepare payload (truncate input to API limits)
        payload = {
            "inputs": text[:1024],  # HF API has input length limits
            "parameters": {
                "max_length": max_len,
                "min_length": min_len,
                "do_sample": False
            },
            "options": {
                "wait_for_model": True  # Wait if model is loading
            }
        }
        
        # Make API request
        response = requests.post(
            HF_API_URL, 
            headers=headers, 
            json=payload, 
            timeout=30
        )
        
        # Handle successful response
        if response.status_code == 200:
            result = response.json()
            
            # Parse response (HF API returns a list)
            if isinstance(result, list) and len(result) > 0:
                summary = result[0].get("summary_text", "")
                if summary:
                    return summary
            
            # Fallback if parsing fails
            return text[:500] + "..." if len(text) > 500 else text
        
        # Handle model loading (503 status)
        elif response.status_code == 503:
            error_data = response.json()
            estimated_time = error_data.get("estimated_time", 20)
            print(f"⏳ Model is loading on HF servers (~{estimated_time}s). Using fallback.")
            return text[:500] + "..." if len(text) > 500 else text
        
        # Handle rate limiting
        elif response.status_code == 429:
            print("⚠️ Rate limit reached. Using fallback truncation.")
            return text[:500] + "..." if len(text) > 500 else text
        
        # Handle other errors
        else:
            print(f"⚠️ HF API error {response.status_code}: {response.text}")
            return text[:500] + "..." if len(text) > 500 else text
            
    except requests.exceptions.Timeout:
        print("⚠️ HF API request timed out. Using fallback.")
        return text[:500] + "..." if len(text) > 500 else text
    
    except Exception as e:
        print(f"❌ Summarization failed: {e}")
        return text[:500] + "..." if len(text) > 500 else text
