from flask import Flask, render_template,request,redirect,url_for
from youtube_transcript_api import YouTubeTranscriptApi
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
stopwords = list(STOP_WORDS)

# Load the English model in spaCy
nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)


# @app.route('/')      
# def index():
#     return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])    
def index():
    result = None
    if request.method == 'POST':
        user_input = request.form['user_in']
        lang =  request.form['lang']
        # print(lang)
        input = u_in(user_input)
        out=results(input, lang)
        return render_template('index.html',output=out)
        # return redirect(url_for('process_input',input_data=user_input))
        # result = process_input(user_input)
    else:
        return render_template('index.html')

def results(user_in, language):
    transcript_list = YouTubeTranscriptApi.list_transcripts(user_in)
    # transcript = transcript_list.find_transcript(['de', 'en'])
    transcript = transcript_list.find_transcript([language])
    # translated_transcript = transcript.translate('hi')
    # var = translated_transcript.fetch()
    var = transcript.fetch()
    final = returnText(var)
    summ = summarizeText(final)
    # print(len(final))
    # doc = nlp(final)
    # sentences = [sentence.text for sentence in doc.sents]
    # processed_text = " ".join(sentences)
    # parser = PlaintextParser.from_string(processed_text, Tokenizer("english"))
    # summarizer = LsaSummarizer()

    # # Summarize the text
    # summary = summarizer(parser.document, 2)  # Summarize to 2 sentences

    # # Convert the summary to a string
    # summary_text = " ".join([str(sentence) for sentence in summary])
    # print(len(summary_text))
    # summarizer = LsaSummarizer()
    # summary = summarizer(parser.document, 4)
    # sentence_text = " ".join(summary[0].words)  // Not Working as aspected
    return summ
    # return transcript.fetch()  

def returnText(ls):
    n= len(ls)
    res = ""
    for i in range(0,n):
       res =  res + ls[i]['text']+ " "
    return res

def summarizeText(document):

    lengthText = len(document)
    print("Before:", lengthText)
    num = int(calculate_ratio(lengthText,(166,5)))
    print("ratio:",num)
    nlp = spacy.load('en_core_web_sm')
    docx = nlp(document)
    mytokens = [token.text for token in docx]

    # Build Word Frequency
    # word.text is tokenization in spacy
    word_frequencies = {}
    for word in docx:
        if word.text not in stopwords:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    # print(word_frequencies)


    maximum_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():  
            word_frequencies[word] = (word_frequencies[word]/maximum_frequency)

    sentence_list = [ sentence for sentence in docx.sents ]

    # Sentence Score via comparrng each word with sentence
    sentence_scores = {}  
    for sent in sentence_list:  
            for word in sent:
                if word.text.lower() in word_frequencies.keys():
                    if len(sent.text.split(' ')) < num:
                        if sent not in sentence_scores.keys():
                            sentence_scores[sent] = word_frequencies[word.text.lower()]
                        else:
                            sentence_scores[sent] += word_frequencies[word.text.lower()]

    from heapq import nlargest

    summarized_sentences = nlargest(7, sentence_scores, key=sentence_scores.get)
    # print(summarized_sentences)
    final_sentences = [ w.text for w in summarized_sentences ]
    summary = ' '.join(final_sentences)
    print("After: ",len(summary))
    return summary

def calculate_ratio(a, ratio):
    # Calculate the ratio
    ratio_b = a * ratio[1] / ratio[0]
    
    return ratio_b



def u_in(str):
    ln= len(str)
    fn = ""
    for i in range(0,ln):
        if(str[i]=='=' and str[i-1]=='v'):
            for j in range(i+1,ln):
                fn = fn+str[j]
    return fn

@app.route('/out')
def out():
     return render_template('out.html')


if __name__ == '__main__':
    app.run(debug=True)
