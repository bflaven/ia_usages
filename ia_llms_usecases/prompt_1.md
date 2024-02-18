# prompt_api_1.md

## prompt
As an advanced programmer in Python, write an script named "grab_title_url.py" that will: 
First, go through a list of URLs 
Second, using beautiful soup python library, for each URL, grab the text in between the tag <title>...</title> present on the source code of the URL. Store the value in a variable {title_text}

Third, for each URL, print the value {URL} and the {title_text} in  the chunk of HTML. Give at the end the full code HTML so the user can cut and paste the all code created.
<li>{title_text}<br><a href="{URL}" target="_blank" rel="noopener">{URL}</a></li>

## output

import requests
from bs4 import BeautifulSoup

# List of URLs
urls = [
    "https://example.com",
    "https://www.python.org",
    # Add more URLs as needed
]

# Store the HTML code
html_code = ""

# Iterate through each URL
for url in urls:
    try:
        # Fetch the HTML content of the URL
        response = requests.get(url)
        html_content = response.text

        # Parse HTML using Beautiful Soup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the title tag
        title_tag = soup.title

        # Extract text from the title tag
        title_text = title_tag.text if title_tag else "Title Not Found"

        # Print the URL and the title text
        print(f"<li>{title_text}<br><a href=\"{url}\" target=\"_blank\" rel=\"noopener\">{url}</a></li>")

        # Append to the HTML code
        html_code += f"<li>{title_text}<br><a href=\"{url}\" target=\"_blank\" rel=\"noopener\">{url}</a></li>"

    except Exception as e:
        print(f"Error processing {url}: {str(e)}")

# Print the full HTML code
print("\nFull HTML Code:")
print(html_code)
