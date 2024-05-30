# w1_prompts_seo_dev.md

## prompt_1
As an advanced programmer in Python, using Beautifull soup, grab the title tag and the main body of the post, clean the HTML and juste preserve the text,  at this url: "https://flaven.fr/2024/05/unraveling-the-cost-of-ai-the-hidden-expenses-of-api-keys-and-pay-as-you-go-pricing-in-ai-based-products/"

## ChatGPT_1


To extract and clean the text from the article at "https://flaven.fr/2024/05/unraveling-the-cost-of-ai-the-hidden-expenses-of-api-keys-and-pay-as-you-go-pricing-in-ai-based-products/" using Beautiful Soup in Python, you can follow the script below. This script will fetch the webpage, parse the HTML to extract the title and main content, and then clean the HTML tags to retain only the text.

```python
import requests
from bs4 import BeautifulSoup

# URL of the webpage
url = "https://flaven.fr/2024/05/unraveling-the-cost-of-ai-the-hidden-expenses-of-api-keys-and-pay-as-you-go-pricing-in-ai-based-products/"

# Fetch the webpage
response = requests.get(url)
webpage = response.content

# Parse the HTML content
soup = BeautifulSoup(webpage, "html.parser")

# Extract the title
title = soup.find('title').get_text()

# Extract the main body content
# Assuming the main content is within an article tag or a specific div
main_content = soup.find('div', {'class': 'entry-content'})  # Adjust the selector based on actual HTML structure

# Function to clean HTML tags and get text
def clean_html(html_element):
    for script in html_element(["script", "style"]):
        script.extract()  # Remove these tags
    return html_element.get_text()

# Clean the main content
cleaned_content = clean_html(main_content)

print("Title: ", title)
print("Content: ", cleaned_content)
```

### Explanation:
1. **Fetch the Webpage**: Using the `requests` library, the script fetches the HTML content of the webpage.
2. **Parse the HTML**: The HTML content is parsed using `BeautifulSoup`.
3. **Extract the Title**: The script locates the `<title>` tag and extracts its text.
4. **Extract the Main Content**: It finds the main content using a CSS selector (you might need to adjust the selector based on the actual structure of the webpage).
5. **Clean the HTML**: The function `clean_html` removes all `<script>` and `<style>` tags from the HTML and returns only the text content.

This script assumes that the main body of the article is contained within a `div` with the class `entry-content`. You might need to inspect the HTML structure of the page and adjust the selector accordingly.

For more details, you can visit the article directly on Bruno Flaven's website at [flaven.fr](https://flaven.fr/2024/05/unraveling-the-cost-of-ai-the-hidden-expenses-of-api-keys-and-pay-as-you-go-pricing-in-ai-based-products/).