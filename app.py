from flask import Flask, render_template,request,redirect,url_for
from youtube_transcript_api import YouTubeTranscriptApi

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
    translated_transcript = transcript.translate('bg')
    var = translated_transcript.fetch()
    # var = transcript.fetch()
    final = returnText(var)
    return final
    # return transcript.fetch()  

def returnText(ls):
    n= len(ls)
    res = ""
    for i in range(0,n):
       res =  res + ls[i]['text']+ " "
    return res



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
