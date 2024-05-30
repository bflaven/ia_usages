# w2_prompts_seo_dev.md

## prompt_1
As an advanced programmer in Python, write a script to request an api endpoint "https://flaven.fr/wp-json/wp/v2/posts?_fields=author,id,excerpt,title,link,content&per_page=5". This endpoint ouputs json format like below then select the values for: "link","title", "excerpt" and also "content" and "id".


```json
[
    {
        "id": 12815,
        "link": "https://flaven.fr/2024/05/unraveling-the-cost-of-ai-the-hidden-expenses-of-api-keys-and-pay-as-you-go-pricing-in-ai-based-products/",
        "title": {
          "rendered": "Unraveling the Cost of AI: The Hidden Expenses of API Keys and Pay-as-You-Go Pricing in AI-Based Products"
        },
        "content": {
          "rendered": "<p>&#8220;After all, we are not communist&#8221; says Emilio &#8220;The Wolf&#8221; Barzini in the Godafather* and indeed despite the virtuous storytelling...."
        },
        "excerpt": {
          "rendered": "<p>&#8220;After all, we are not communist&#8221; says Emilio &#8220;The Wolf&#8221; Barzini in the Godafather* and indeed despite the virtuous storytelling, IA is here to make&hellip; </p>\n<p class=\"text-center\"><a href=\"https://flaven.fr/2024/05/unraveling-the-cost-of-ai-the-hidden-expenses-of-api-keys-and-pay-as-you-go-pricing-in-ai-based-products/\" class=\"more-link\">Continue reading &rarr; <span class=\"screen-reader-text\">Unraveling the Cost of AI: The Hidden Expenses of API Keys and Pay-as-You-Go Pricing in AI-Based Products</span></a></p>\n",
          "protected": false
        },
        "author": 1
      },
    {},
    {},
    {},
    {}
],

```



## ChatGPT_1

To fetch data from the API endpoint and extract the desired fields using Python, you can use the `requests` library to make the API call and then process the JSON response. Below is a script that accomplishes this:

```python
import requests

# API endpoint
url = "https://flaven.fr/wp-json/wp/v2/posts?_fields=author,id,excerpt,title,link,content&per_page=5"

# Make the API request
response = requests.get(url)
data = response.json()

# Extract the required fields
for post in data:
    post_id = post.get("id")
    link = post.get("link")
    title = post.get("title", {}).get("rendered")
    excerpt = post.get("excerpt", {}).get("rendered")
    content = post.get("content", {}).get("rendered")
    
    # Print the extracted fields
    print(f"ID: {post_id}")
    print(f"Link: {link}")
    print(f"Title: {title}")
    print(f"Excerpt: {excerpt}")
    print(f"Content: {content}")
    print("\n" + "-"*80 + "\n")
```

### Explanation:
1. **API Request**: The script sends a GET request to the specified API endpoint.
2. **Parse JSON Response**: The JSON response is parsed into a Python list of dictionaries.
3. **Extract Fields**: The script iterates over the list and extracts the `id`, `link`, `title`, `excerpt`, and `content` fields from each post.
4. **Print Extracted Fields**: The extracted fields are printed out.

### Libraries Used:
- `requests`: To make the HTTP request to the API endpoint and fetch the response.

This script will output the details for each post in a formatted manner. Make sure you have the `requests` library installed. You can install it using pip if you don't have it:

```sh
pip install requests
```

This will give you a clean and structured output of the desired fields from the API response.
