# gathering data from twitter
import snscrape.modules.twitter as twitter
import matplotlib.pyplot as plt
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
from wordcloud import WordCloud
import re
import pandas as pd
tweets=[]
links=[]
names=[]
date=[]
names=[]
trend_name=[]
trends_without_hash=[]
"""  preparing the txt file which contain the trends  """
trends=[]
with open(r"worldwide.txt","r",encoding="utf8")as f:
    for tre in f:
        tre=tre[:-1]
        trends.append(tre)
# print(trends)
# print(len(trends))
"""  removing duplicates from the list  """
trends = list(dict.fromkeys(trends))
print(len(trends))
iteration=1
"""  removing the hashtag from all indecies  """
for trend in trends:
    if trend[0]=="#":
        print(trend)
        trends_without_hash.append(trend[1:-1])
    else:
        trends_without_hash.append(trend)
    
# print(trends_without_hash)
print(len(trends_without_hash))

for trend in trends_without_hash:
    x=len(tweets)
    query="tesla ({}) until:2020-06-30 since:2019-11-01".format(trend)
    print (iteration,"-",query)
    limit=200
    for tweet in twitter.TwitterSearchScraper(query).get_items():
        # if len(tweets)==limit:
        #     break
        # else:                                                                                               
            tweets.append(tweet.content)
            links.append(tweet.url)
            names.append(tweet.user.username)
            date.append(tweet.date)
            trend_name.append(trend)
        # print(tweets)
    iteration+=1
    print("founded tweets",(len(tweets))-x)
    dataframe=pd.DataFrame({'name':names,'content':tweets,'date':date,'URL':links,'trend':trend_name})
    # print (dataframe)
    dataframe.to_csv(r'tweets.csv',mode='a', encoding='utf-8')

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('vader_lexicon')
# Define a list of stop words to remove from the text
stop_words = set(stopwords.words('english'))

# Create a stemmer object to perform stemming
stemmer = PorterStemmer()

# Create a sentiment analyzer object
analyzer = SentimentIntensityAnalyzer()

def preprocess_text(text):
    # Convert the text to lowercase
    text = text.lower()

    # Replace URLs with the word "URL"
    text = re.sub(r'http\S+', '', text)

    # Replace emojis using a pre-defined dictionary
    emoji_dict = {
    '😀': 'smiling face',
    '😂': 'face with tears of joy',
    '😊': 'smiling face with smiling eyes',
    '😍': 'smiling face with heart-eyes',
    '😘': 'face blowing a kiss',
    '👍': 'thumbs up',
    '👎': 'thumbs down',
    '🤔': 'thinking face',
    '😎': 'smiling face with sunglasses',
    '🙌': 'raising hands',
    '🤷': 'shrugging',
    '💩': 'pile of poo'
}
    for emoji, meaning in emoji_dict.items():
      text = text.replace(emoji, f"EMOJI{meaning}")

    # Replace usernames with the word "USER"
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'@[^a-zA-Z0-9]+', ' ', text)

    text = re.sub(r'#','', text)

    text = re.sub(r'RT[\s]+',' ', text)

    # Remove non-alphabetic characters
    text = re.sub(r'[^a-zA-Z0-9]', ' ', text)

    # Remove consecutive letters
    text = re.sub(r'(.)\1{2,}', r'\1\1', text)

    # Tokenize the text into words
    words = word_tokenize(text)

    # Remove short words and stop words
    words = [word for word in words if len(word) > 2 and not word.lower() in stop_words]

    # Perform stemming on the remaining words
    #words = [stemmer.stem(word) for word in words]

    # Join the remaining words back into a string
    text = ' '.join(words)

    return text
dataframe['Tweets_'] = dataframe['content'].apply(preprocess_text)
dataframe

def getSubjectivity(text):
      return TextBlob(text).sentiment.subjectivity

def getPolarity(text):
  return TextBlob(text).sentiment.polarity

dataframe['Subjectivity'] = dataframe['Tweets_'].apply(getSubjectivity)
dataframe['Polarity'] = dataframe['Tweets_'].apply(getPolarity)
dataframe

def getAnalysis(score):
    if score < 0:
        return 'Negative'
    elif score == 0: 
        return 'Netural'
    else:
        return 'Positive'
  
dataframe['Analysis'] = dataframe['Polarity'].apply(getAnalysis)
dataframe

dataframe['Analysis'].value_counts()
plt.title('Sentiment Analysis')
plt.xlabel('Sentiment')

###############################################################################
dataframe
plt.ylabel('Count')
dataframe['Analysis'].value_counts().plot(kind = 'bar')
plt.show()
