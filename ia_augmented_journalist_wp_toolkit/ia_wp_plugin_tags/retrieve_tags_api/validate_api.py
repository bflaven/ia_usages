#!/usr/bin/env python3
"""
WordPress API Validation Script
---------------------------------
Quick test to validate API connectivity and check available fields.
Run this before the main extraction to verify your configuration.
"""

import requests
import json
from typing import Dict, Any


def validate_api(api_url: str, timeout: int = 10) -> Dict[str, Any]:
    """
    Validate WordPress API endpoint and return sample data.
    
    Args:
        api_url: WordPress API endpoint URL
        timeout: Request timeout in seconds
    
    Returns:
        Dictionary with validation results
    """
    result = {
        "success": False,
        "api_url": api_url,
        "status_code": None,
        "total_tags": None,
        "total_pages": None,
        "sample_fields": None,
        "error": None
    }
    
    try:
        print(f"🔍 Testing API endpoint: {api_url}")
        print("-" * 70)
        
        # Fetch first page with max results
        params = {"page": 1, "per_page": 1}  # Just get 1 tag to test
        response = requests.get(api_url, params=params, timeout=timeout)
        
        result["status_code"] = response.status_code
        
        if response.status_code != 200:
            result["error"] = f"HTTP {response.status_code}: {response.reason}"
            return result
        
        # Parse response
        tags = response.json()
        
        # Get pagination info from headers
        result["total_tags"] = response.headers.get('X-WP-Total')
        result["total_pages"] = response.headers.get('X-WP-TotalPages')
        
        # Get available fields from first tag
        if tags and len(tags) > 0:
            result["sample_fields"] = list(tags[0].keys())
            result["success"] = True
        else:
            result["error"] = "No tags found in response"
        
    except requests.exceptions.Timeout:
        result["error"] = "Request timeout - server took too long to respond"
    except requests.exceptions.ConnectionError:
        result["error"] = "Connection error - could not reach server"
    except requests.exceptions.RequestException as e:
        result["error"] = f"Request failed: {str(e)}"
    except json.JSONDecodeError:
        result["error"] = "Invalid JSON response from server"
    except Exception as e:
        result["error"] = f"Unexpected error: {str(e)}"
    
    return result


def print_validation_results(result: Dict[str, Any]) -> None:
    """Print validation results in a readable format."""
    
    if result["success"]:
        print("✅ API Validation SUCCESSFUL")
        print("-" * 70)
        print(f"Status Code:    {result['status_code']}")
        print(f"Total Tags:     {result['total_tags']}")
        print(f"Total Pages:    {result['total_pages']}")
        print(f"\nAvailable Fields ({len(result['sample_fields'])}):")
        for field in result['sample_fields']:
            print(f"  • {field}")
        print("-" * 70)
        print("\n💡 You can use these field names in 'fields_to_extract' config")
        print("\nExample configuration:")
        print('  "fields_to_extract": ["id", "name", "slug", "count"]')
        print("-" * 70)
        
    else:
        print("❌ API Validation FAILED")
        print("-" * 70)
        print(f"Error: {result['error']}")
        if result['status_code']:
            print(f"Status Code: {result['status_code']}")
        print("-" * 70)
        print("\n🔧 Troubleshooting tips:")
        print("  1. Check if the URL is correct")
        print("  2. Verify the WordPress site is accessible")
        print("  3. Ensure REST API is enabled on the WordPress site")
        print("  4. Check your internet connection")
        print("-" * 70)


def main():
    """Main execution."""
    print("=" * 70)
    print("WordPress API Validator")
    print("=" * 70)
    print()
    
    # Test the main API endpoint
    api_url = "https://flaven.fr/wp-json/wp/v2/tags"
    result = validate_api(api_url, timeout=10)
    print_validation_results(result)
    
    print()
    
    # Additional quick tests
    if result["success"]:
        estimated_time = int(result["total_pages"]) * 2  # Rough estimate
        print(f"📊 Estimated extraction time: ~{estimated_time} seconds")
        print(f"📦 You will download approximately {result['total_tags']} tags")
        print()
        print("✅ Ready to run the main extraction script!")
    else:
        print("⚠️  Fix the issues above before running the extraction script")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
