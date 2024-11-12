import spacy
import pytextrank
import json


def get_top_ranked_phrases(text):
    nlp = spacy.load("en_core_web_sm")

    nlp.add_pipe("textrank")
    doc = nlp(text)

    top_phrases = []

    for phrase in doc._.phrases:
        top_phrases.append({
            "text": phrase.text,
            "rank": phrase.rank,
            "count": phrase.count,
            "chunks": phrase.chunks
        })

    return top_phrases


# walkability_vs_car_usage_text = "'Person A: Living in a walkable neighborhood has completely changed the way I go about my daily life. I no longer rely on my car for everything. I can easily walk to the grocery store, visit the nearby park, or have a cup of coffee at the charming café just around the corner. The convenience and health benefits are incredible.Person B: I can see the appeal, but let's not forget that car usage is still essential in certain situations. As a mom with young children, it's not always practical for me to walk long distances or carry heavy groceries. However, I believe walkable neighborhoods can provide solutions. Imagine having a community greenhouse where we can grow fresh produce together or a nearby maker space for creative activities. These amenities would enhance the sense of community and reduce our reliance on cars.Person C: I couldn't agree more. Prioritizing walkability brings numerous benefits. By embracing alternative modes of transportation like walking, cycling, or public transit, we can reduce traffic congestion, decrease pollution levels, and improve our overall well-being. It's time to reimagine our cities with pedestrian-friendly infrastructure, green spaces, and accessible amenities. Walkability isn't just about getting from point A to point B; it's about creating vibrant, sustainable, and people-centric communities. Person A: Exactly! As a software architect, I've seen how walkability fosters a sense of community and encourages spontaneous interactions. It's like being part of a living, breathing social network, where I can exchange ideas with fellow pedestrians and feel more connected to my surroundings. The benefits go beyond mere convenience. Person B: While I appreciate the concept, I have to admit that relying solely on walkability isn't always practical for me. There are days when I have early morning meetings or need to travel across town for work-related commitments. However, I do support initiatives that promote alternative transportation, such as designated bike lanes or efficient public transit systems. Finding a balance between walkability and car usage is crucial for individuals with demanding schedules. Person C: That's a valid point. Achieving a balance is key. Walkable neighborhoods can still coexist with other transportation options. It's about offering choices and creating a framework where people can rely less on cars for their day-to-day activities. By incorporating thoughtful design and infrastructure, we can make our communities more sustainable and livable for everyone.'"
walkability_vs_car_usage_text = """
The share price of a small Chinese company in financial difficulties has skyrocketed in recent days. The company's only real asset is its name: Wisesoft, which in Chinese sounds like the phrase 'Trump wins big'. Chinese investors are prone to buying shares solely on the basis of a company name.

    Former US president Donald Trump’s influence looms large, and not just in the United States. In China, his name has prompted some people to make a quirky bet on the stock market.

    The share price of a small company that makes air traffic control software, Wisesoft, doubled over the past month on the Shenzhen Stock Exchange, a gain at odds with the company’s lacklustre financial results. It recorded a loss of Є3.5 million, (27.04 million yuan), for the first nine months of 2024.

    Wisesoft's attraction for local investors is in its name, phonetically close to the expression “Trump wins big”, notes Bloomberg News.
"""

top_phrases = get_top_ranked_phrases(walkability_vs_car_usage_text)


for phrase in top_phrases:
    print(phrase["text"], phrase["rank"], phrase["count"], phrase["chunks"])