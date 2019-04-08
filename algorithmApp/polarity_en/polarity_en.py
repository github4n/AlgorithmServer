# import textblob
from textblob import TextBlob
import nltk
#要在语料库里提前把这个语料库下载下来,百度nltk
# nltk.download('punkt')

# import polyglot
# from pattern.en import sentiment
# from utils import file_path
# import os

def polarity_en(article):
    blob = TextBlob(article)

    # print(blob.sentiment)
    # print(blob.sentences)

    score = []

    for i in blob.sentences:
        # print(i.sentiment.polarity)
        if i.sentiment.polarity>=0.3:
            score.append(1)
        elif i.sentiment.polarity<=-0.3:
            score.append(3)
        else:
            score.append(2)

    # print(score)
    if score.count(1)==0:
        if score.count(3)/len(score)>0.1:
            res=3
        else:
            res=2
    elif score.count(3)==0:
        if score.count(1)/len(score)>0.1:
            res=1
        else:
            res=2
    else:
        if (score.count(1)-score.count(3)) / len(score) > 0.1:
            res = 1
        elif (score.count(3)-score.count(1)) / len(score) > 0.1:
            res= 3
        else:
            res=2


    # print(res)

    return res



if __name__ == "__main__":

    news1 = """ATHENS, Jan. 5 (Xinhua) -- An elderly woman died and two men went missing on Saturday as cold front "Sophia" continued sweeping across Greece, national news agency AMNA reported.

Firemen retrieved the dead body of a 66-year-old woman from a car in a stream at Keratea town, 30 kilometers southeast of Athens, the Fire Brigade said. Her husband, 67, and a neighbor, 64, have been missing since Thursday. They were all passengers in the car when a heavy storm hit the area.

The weather system which has gripped Greece from Tuesday brought snowfall and downpour in many parts of the country, mostly in central and northern provinces, shutting down regional roads.

The Fire Brigade had to intervene from Jan. 3 to transfer to hospitals 28 patients nationwide, as well as move to safe sites 45 travelers who had been stranded in vehicles across the country, according to an e-mailed press release on Saturday.

Ferry services were disrupted, as winds up to 9 on the Beaufort scale were blowing at sea, while hundreds of travelers suffered from flight delays and cancellations, the civil aviation authority said.

Two hundred passengers of a flight which had departed from London on Friday evening were expected to arrive in Greece on Saturday evening by air or bus from Romania. The Ryanair aircraft was diverted to Timisoara airport, as it could not land at Thessaloniki Airport in northern Greece due to adverse weather conditions.

On Saturday, in many parts of the country the thermometer showed temperatures close to zero degrees Celsius, while the lowest (-12.5C) was recorded at Florina town in northern Greece."""
    print(polarity_en(news1))

