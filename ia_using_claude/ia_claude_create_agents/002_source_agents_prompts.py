

# https://github.com/blahmin/SEO-Blog-Agentic-AI/blob/main/backend/gpt_blog_maker.py



import os
from openai import OpenAI
import requests
import base64
import tempfile

# Get unsplash api to use photo function
UNSPLASH_ACCESS_KEY = "UNSPLASH_ACCESS_KEY"
UNSPLASH_SECRET_KEY = "UNSPLASH_SECRET_KEY"

# Get OpenAI API key
client = OpenAI(api_key="OPENAI_API_KEY")

# To get the wordpress upload feature, add your wordpress url, username and password
WP_URL = "Wordpress URL"
WP_USER = "username"
WP_APP_PASSWORD = "password"

# Length guidelines
LENGTH_GUIDELINES = {
    "short": {
        "word_count": "500-750 words",
        "sections": "2-3 main sections",
        "detail_level": "Concise and focused, covering key points only"
    },
    "medium": {
        "word_count": "1000-1500 words",
        "sections": "3-4 main sections",
        "detail_level": "Balanced depth with supporting details"
    },
    "long": {
        "word_count": "2000-2500 words",
        "sections": "5-6 main sections",
        "detail_level": "In-depth coverage with comprehensive explanations"
    }
}

SEO_GPT_PROMPT = (
    "You are an SEO expert. Your job is to generate SEO-optimized blog ideas, outlines, and tags. "
    "Focus on maximizing search visibility and aligning with the specified genre."
)

REVIEWER_GPT_PROMPT = (
    "You are a blog idea reviewer. Your job is to select the best blog idea from the provided list "
    "and explain your reasoning."
)

OUTLINE_GPT_PROMPT = """You are a professional blog planner. Your job is to create a detailed and SEO-optimized blog outline for the selected idea.
The outline should be appropriate for the specified length: {length_type}
Target word count: {word_count}
Number of sections: {sections}
Level of detail: {detail_level}"""

WRITER_GPT_PROMPT = """You are a professional blog writer. Your job is to write engaging, high-quality content based on the provided outline, using the specified writing style. 

IMPORTANT FORMATTING INSTRUCTIONS:
1. Write in clean HTML format using proper <h2>, <h3>, and <p> tags
2. Do NOT use any markdown syntax or code blocks (```)
3. Do NOT add extra spaces between sections
4. Keep the formatting minimal and clean
5. Sections should flow naturally with a single line break between them
6. Start each main section with an <h2> tag and subsections with <h3> tags
7. Wrap regular text in <p> tags
8. Do not include any raw HTML tags in the text content

LENGTH REQUIREMENTS:
- Target word count: {word_count}
- Level of detail: {detail_level}

Write the complete article in a single response, following the outline structure but maintaining natural flow between sections."""


def get_blog_length():
    while True:
        length = input("\nHow long would you like the blog to be? (short/medium/long): ").lower().strip()
        if length in LENGTH_GUIDELINES:
            return length
        print("Invalid input. Please enter 'short', 'medium', or 'long'.")


def seo_gpt(task, genre=None):
    if task == "ideas":
        prompt = f"{SEO_GPT_PROMPT}\n\nGenerate 3 SEO-optimized blog ideas for the genre: {genre}."
    else:
        raise ValueError("Invalid task specified for SEO GPT.")

    response = client.chat.completions.create(
        model="gpt-4o-mini",  
        messages=[
            {"role": "system", "content": SEO_GPT_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


def reviewer_gpt(ideas):
    prompt = f"{REVIEWER_GPT_PROMPT}\n\nHere are 3 blog ideas: {ideas}. Select the best one and explain your reasoning."

    response = client.chat.completions.create(
        model="gpt-4o-mini",  
        messages=[
            {"role": "system", "content": REVIEWER_GPT_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )

    content = response.choices[0].message.content
    title = content.split('\n')[0]
    title = ':'.join(title.split(':')[1:]) if ':' in title else title
    return title.strip()


def outline_gpt(idea, length_type):
    guidelines = LENGTH_GUIDELINES[length_type]
    prompt_template = OUTLINE_GPT_PROMPT.format(
        length_type=length_type,
        word_count=guidelines["word_count"],
        sections=guidelines["sections"],
        detail_level=guidelines["detail_level"]
    )

    prompt = f"{prompt_template}\n\nCreate an SEO-optimized blog outline for the following idea: {idea}."

    response = client.chat.completions.create(
        model="gpt-4o-mini",  
        messages=[
            {"role": "system", "content": prompt_template},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


def writer_gpt(outline, writing_style=None, length_type="medium"):
    guidelines = LENGTH_GUIDELINES[length_type]
    prompt_template = WRITER_GPT_PROMPT.format(
        word_count=guidelines["word_count"],
        detail_level=guidelines["detail_level"]
    )

    prompt = (
        f"{prompt_template}\n\nWrite a complete blog post following this outline:\n{outline}\n"
        f"Writing style: {writing_style}\n\n"
        "Remember: Use clean HTML formatting without markdown or code blocks."
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",  
        messages=[
            {"role": "system", "content": prompt_template},
            {"role": "user", "content": prompt}
        ]
    )

    content = response.choices[0].message.content
    return content.replace("```html", "").replace("```", "").strip()

def get_random_unsplash_photo(query):
    """
    Fetches a random Unsplash image relevant to the given query (genre),
    with orientation=landscape to ensure horizontal images.
    Returns (image_url, photographer_name, photographer_link).
    """
    url = (
        f"https://api.unsplash.com/photos/random"
        f"?query={query}"
        f"&orientation=landscape"
        f"&client_id={UNSPLASH_ACCESS_KEY}"
    )
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        image_url = data["urls"]["full"]
        photographer_name = data["user"]["name"]
        photographer_link = data["user"]["links"]["html"]
        return (image_url, photographer_name, photographer_link)
    except Exception as e:
        print("Error fetching random Unsplash photo:", e)
        return (None, None, None)

# SET FEATURED IMAGE ON WORDPRESS
# - Uses multipart/form-data
# - Sets alt_text with link to the image & photographer name
def set_wp_featured_image(post_id, image_url, photographer_name, photographer_link):
    """
    Downloads the image locally, uploads to WP as media (multipart/form-data),
    sets that media as the Featured Image for the given post_id,
    then:
      - updates alt_text to include the image link & photographer name
      - appends a credit link to the bottom of the post content
    """
    WP_API_BASE = "https://YOUR_WORDPRESS_SITE/wp-json/wp/v2"

    auth_str = f"{WP_USER}:{WP_APP_PASSWORD}"
    auth_bytes = auth_str.encode('utf-8')
    auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')
    headers = {
        "Authorization": f"Basic {auth_base64}"
    }

    temp_file_path = None
    try:
        r = requests.get(image_url, stream=True)
        r.raise_for_status()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    tmp.write(chunk)
            temp_file_path = tmp.name
    except Exception as e:
        print("Error downloading Unsplash image:", e)
        return

    media_id = None
    if temp_file_path:
        file_name = os.path.basename(temp_file_path)
        media_endpoint = f"{WP_API_BASE}/media"
        try:
            with open(temp_file_path, "rb") as img_file:
                files = {
                    "file": (file_name, img_file, "image/jpeg")
                }
                upload_resp = requests.post(
                    media_endpoint,
                    headers=headers,
                    files=files
                )
            upload_resp.raise_for_status()
            media_data = upload_resp.json()
            media_id = media_data.get("id")
        except Exception as e:
            print("Error uploading image to WordPress:", e)
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)


    if media_id:
        media_patch_endpoint = f"{WP_API_BASE}/media/{media_id}"
        alt_text_content = f"{image_url} by {photographer_name}" if photographer_name else image_url
        alt_text_payload = {
            "alt_text": alt_text_content
        }
        try:
            patch_alt_resp = requests.post(
                media_patch_endpoint,
                headers={**headers, "Content-Type": "application/json"},
                json=alt_text_payload
            )
            patch_alt_resp.raise_for_status()
        except Exception as e:
            print("Error setting alt text on media:", e)

    if media_id:
        post_endpoint = f"{WP_API_BASE}/posts/{post_id}"
        post_payload = {
            "featured_media": media_id
        }
        try:
            update_resp = requests.post(
                post_endpoint,
                headers={**headers, "Content-Type": "application/json"},
                json=post_payload
            )
            update_resp.raise_for_status()
        except Exception as e:
            print("Error setting featured media:", e)
            return

        try:
            updated_post = update_resp.json()
            existing_content = updated_post.get("content", {}).get("rendered", "")

            credit_html = (
                f'<p style="font-size:small;">Photo by '
                f'<a href="{photographer_link}" target="_blank" rel="noopener">'
                f'{photographer_name}</a> on '
                f'<a href="https://unsplash.com" target="_blank" rel="noopener">Unsplash</a>.</p>'
            )
            new_content = existing_content + credit_html

            patch_resp = requests.post(
                post_endpoint,
                headers={**headers, "Content-Type": "application/json"},
                json={"content": new_content}
            )
            patch_resp.raise_for_status()
            print("Featured image set, alt text added, and credit appended.")
        except Exception as e:
            print("Error adding credit to post:", e)


def publish_to_wordpress(title, content):
    auth_str = f"{WP_USER}:{WP_APP_PASSWORD}"
    auth_bytes = auth_str.encode('utf-8')
    auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')

    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/json"
    }

    while True:
        status = input("Do you want to publish the post or save it as a draft? (publish/draft): ").strip().lower()
        if status in ['publish', 'draft']:
            break
        print("Invalid input. Please enter either 'publish' or 'draft'.")

    post_data = {
        "title": title,
        "content": content,
        "status": status
    }

    try:
        response = requests.post(WP_URL, json=post_data, headers=headers)
        response.raise_for_status()
        post_json = response.json()
        post_id = post_json.get("id")
        print(f"Post successfully {'published' if status == 'publish' else 'saved as draft'} to WordPress! Post ID: {post_id}")
        return post_id  
    except requests.exceptions.RequestException as e:
        print(f"Failed to save post. Error: {str(e)}")
        if hasattr(response, 'text'):
            print("Response Content:", response.text)
        return None


if __name__ == "__main__":
    try:
        genre = input("Enter the genre for the blog ideas: ")
        length_type = get_blog_length()

        print(f"\nGenerating {length_type} blog post...")
        print(f"Target length: {LENGTH_GUIDELINES[length_type]['word_count']}")

        print("\nGenerating blog ideas...")
        blog_ideas = seo_gpt(task="ideas", genre=genre)
        print("\nGenerated ideas:", blog_ideas)

        print("\nSelecting the best idea...")
        title = reviewer_gpt(ideas=blog_ideas)
        print("\nSelected title:", title)

        print("\nGenerating outline...")
        blog_outline = outline_gpt(idea=title, length_type=length_type)
        print("\nGenerated outline:", blog_outline)

        print("\nWriting complete blog post...")
        writing_style = "Professional, engaging, and informative"
        final_blog_content = writer_gpt(
            outline=blog_outline,
            writing_style=writing_style,
            length_type=length_type
        )

        print("\nFinal Blog Preview:")
        print("-" * 50)
        print(f"Title: {title}")
        print("-" * 50)
        print(final_blog_content)
        print("-" * 50)

        if input("\nWould you like to upload this to WordPress? (yes/no): ").lower().strip() == 'yes':
            new_post_id = publish_to_wordpress(title=title, content=final_blog_content)
            if new_post_id:
                image_url, photographer_name, photographer_link = get_random_unsplash_photo(genre)
                if image_url:
                    set_wp_featured_image(new_post_id, image_url, photographer_name, photographer_link)
                else:
                    print("Could not retrieve a random Unsplash photo.")
        else:
            print("Upload cancelled.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


