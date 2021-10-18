import re
import pandas as pd
from cltk.tokenize.word import WordTokenizer
from cltk.stop.classical_hindi.stops import STOPS_LIST
import demoji
from polyglot.detect import Detector

hindi_tweets_data=pd.read_csv('/Users/stutipathak/Networks/hindi/hindi_total.csv')

tweet_only=pd.DataFrame(hindi_tweets_data["tweet"])
tweet_only_list=tweet_only.values.tolist()

tokenizer = WordTokenizer('sanskrit')

stopwords=["मैं","मुझको","मेरा","अपने आप को","हमने",'हमारा','अपना','हम','आप','आपका','तुम्हारा','अपने आप','स्वयं','वह','इसे','उसके',
          'खुद को','कि वह','उसकी','उसका','खुद ही','यह','इसके','उन्होने','अपने','क्या','जो','किसे','किसको','कि','ये','हूँ','होता है',
          'रहे','थी','थे','होना','गया','किया जा रहा है','किया है','है','पडा','होने','करना','करता है','किया','रही','एक','लेकिन','अगर','या',
          'क्यूंकि','जैसा','जब तक','जबकि','की','पर','द्वारा','के लिए','साथ','के बारे में','खिलाफ','बीच','में','के माध्यम से','दौरान','से पहले',
          'के बाद','ऊपर','नीचे','को','से','तक','से नीचे','करने में','निकल','बंद','से अधिक','तहत','दुबारा','आगे','फिर','एक बार','यहाँ',
          'वहाँ','कब','कहाँ','क्यों','कैसे','सारे','किसी','दोनो','प्रत्येक','ज्यादा','अधिकांश,अन्य','में कुछ','ऐसा','में कोई','मात्र','खुद','समान',
          'इसलिए','बहुत','सकता','जायेंगे','जरा','चाहिए','अभी','और','कर दिया','रखें','का','हैं','इस','होता','करने','ने','बनी','तो','ही',
          'हो','इसका','था','हुआ','वाले','बाद','लिए','सकते','इसमें','दो','वे','करते','कहा','वर्ग','कई','करें','होती','अपनी','उनके','यदि',
          'हुई','जा','कहते','जब','होते','कोई','हुए','व','जैसे','सभी','करता','उनकी','तरह','उस','आदि','इसकी','उनका','इसी','पे','तथा',
          'भी','परंतु','इन','कम','दूर','पूरे','गये','तुम','मै','यहां','हुये','कभी','अथवा','गयी','प्रति','जाता','इन्हें','गई','अब','जिसमें',
          'लिया','बड़ा','जाती','तब','उसे','जाते','लेकर','बड़े','दूसरे','जाने','बाहर','स्थान','उन्हें','गए','ऐसे','जिससे','समय','दोनों','किए',
          'रहती','इनके','इनका','इनकी','सकती','आज','कल','जिन्हें','जिन्हों','तिन्हें','तिन्हों','किन्हों','किन्हें','इत्यादि','इन्हों','उन्हों','बिलकुल',
          'निहायत','इन्हीं','उन्हीं','जितना','दूसरा','कितना','साबुत','वग़ैरह','कौनसा','लिये','दिया','जिसे','तिसे','काफ़ी','पहले','बाला','मानो',
          'अंदर','भीतर','पूरा','सारा','उनको','वहीं','जहाँ','जीधर','के','एवं','कुछ','कुल','रहा','जिस','जिन','तिस','तिन','कौन','किस',
          'संग','यही','बही','उसी','मगर','कर','मे','एस','उन','है','सो','है','अत','हैं','है','है।','हैं।','।','आए','जी','आया','दी','आ',
          'आने','होगा','सामने','नही','जारी','वो','ली','मिले','और','सबसे','बताया','पहुंची','जाए','वालों','ले','इससे','जाएं','देख','लो',
          'कितनी','बचने','निकली','चलना','जानने','देखो','होंगे','बड़ी','पहुंचा','मिला','फैला','रहते','हा','पूर्ण','इसका','ऑफ','जैसा','टाइम्स',
          'क्योंकि','जैसे','अन्य','बातों','कीजिये','यदि','पहल','रहते','उतपन्न','ठीक','बढ','चलते','जैसी','करो','शुरू','रहेगा','अधिक','देखिए',
          'करे','देखें','घेर','कराना','करवाओ','जैसी','बचने','आधार','सही','चुकी','करे','भेजा','रखा','की','पूरी','चलते','चुका','से','में','ने',
          'रहें','की','लिए','जानेंगे','आदमी','मार','आए','चाहते','लगेगा','वक़्त','थोड़ी','प्रभारी','स्पष्ट','दम','पढे','आहट','छोड़','सभी','महिला',
          'बयान','प्रचार','गए','करनी','पढ़','चलकर','सकेगा','लेकिन','आपके', 'तरीका','लुढ़का','गई','कितने','भेज','हमे','नही','देता','माध्यम',
          'अन्यथा','होगा','आवश्यक','साफ','ऐसी','साबित','डा','हमें','लगे','विज','बाकी','कुछ','नौ','रहे','बेशर्मी','मिल', 'सबको','केवल',
          'कहां','धन्यवाद','क','उच्चस्तरीय','सारी','रोना','समझे','माना','शब्द','फरवरी','जल्दी','तौर','बनाये','कार्य','नगर','भाग','पेट','करेंगे',
          'यहीं','पिया','विभिन्न','दस','बल','रे','थोड़ा','से','में','ने','रहें','की','लिए','जानेंगे']+STOPS_LIST

k=[]
for i in stopwords:
    k.append(" " + i + " ")

tokenized_list_from_devanagri_to_hindi_only=[]
index=[]
mentions=[]
username=[]
for i in range(len(tweet_only_list)):

    tweet = tweet_only_list[i]
    tweet = " " + str(tweet) + " "

    tweet = re.sub('http\S+\s*', '', tweet)
    tweet = re.sub('RT|cc', '', tweet)
    tweet = re.sub('#\S+', '', tweet)
    tweet = re.sub('@\S+', '', tweet)
    tweet = re.sub('[%s]' % re.escape("""⁦!"#–$‘%’&«'()।*+,-./:;<=>?@[\]^_`{|}~''"""), '', tweet)

    for d in k:
        tweet = re.sub(d, ' ', tweet)

    tweet = re.sub(' है', ' ', tweet)
    tweet = re.sub(' ं ', ' ', tweet)
    tweet = re.sub("["u"A-Z"u"a-z"u"0-9"u"०-९""]+", '', tweet)
    tweet = demoji.replace(tweet)
    tweet = re.sub('…', '', tweet)
    tweet = re.sub('\s+', ' ', tweet)

    try:
        detector = Detector(tweet)
        if detector.language.code == 'hi':
            tokenized_list_from_devanagri_to_hindi_only.append(tokenizer.tokenize(tweet))
            index.append(i)
            mentions.append(hindi_tweets_data.mentions[i])
            username.append(hindi_tweets_data.username[i])

    except Exception:
        pass

# creating dataset for rumour networks
a={'index_in_whole_data':index,'only_hindi_tokenized':tokenized_list_from_devanagri_to_hindi_only,'mentions':mentions,'username':username}
only_hindi_tokenized=pd.DataFrame(data=a)
only_hindi_tokenized.to_csv('/Users/stutipathak/Networks/hindi/only_hindi_tokenized.csv')
print(only_hindi_tokenized[0:5])
