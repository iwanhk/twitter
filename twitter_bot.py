import os
import requests
import tweepy
from openai import OpenAI

# ===== 配置 =====
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

TWITTER_API_KEY = os.environ["TWITTER_API_KEY"]
TWITTER_API_SECRET = os.environ["TWITTER_API_SECRET"]
TWITTER_ACCESS_TOKEN = os.environ["TWITTER_ACCESS_TOKEN"]
TWITTER_ACCESS_SECRET = os.environ["TWITTER_ACCESS_SECRET"]

# ===== Twitter 认证 =====
auth = tweepy.OAuth1UserHandler(
    TWITTER_API_KEY,
    TWITTER_API_SECRET,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_SECRET
)
twitter = tweepy.API(auth)

# ===== OpenAI 客户端 =====
client = OpenAI(api_key=OPENAI_API_KEY)

# ===== 获取新闻（示例：CoinDesk RSS）=====
def fetch_news():
    url = "https://www.coindesk.com/arc/outboundfeeds/rss/"
    r = requests.get(url, timeout=10)
    return r.text[:3000]

# ===== 生成推文 =====
def generate_tweet(news):
    prompt = f"""
    Create one concise Twitter post about blockchain and Hong Kong RWA.
    Use professional tone. Max 280 chars.
    Add hashtags: #Blockchain #HongKong #RWA

    News:
    {news}
    """
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return resp.choices[0].message.content.strip()

# ===== 生成图片 =====
def generate_image():
    img = client.images.generate(
        prompt="Hong Kong blockchain RWA tokenization, professional fintech illustration",
        size="1024x1024"
    )
    return img.data[0].url

# ===== 发布推文 =====
def post(tweet, image_url):
    img_data = requests.get(image_url).content
    with open("img.jpg", "wb") as f:
        f.write(img_data)

    media = twitter.media_upload("img.jpg")
    twitter.update_status(tweet, media_ids=[media.media_id])

# ===== 主流程 =====
def main():
    news = fetch_news()
    tweet = generate_tweet(news)
    image_url = generate_image()
    post(tweet, image_url)

if __name__ == "__main__":
    main()
