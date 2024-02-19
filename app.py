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
        out=results(user_input)
        return render_template('index.html',output=out)
        # return redirect(url_for('process_input',input_data=user_input))
        # result = process_input(user_input)
    else:
        return render_template('index.html')

def results(user_in):
    transcript_list = YouTubeTranscriptApi.list_transcripts(user_in)
    var='en'
    transcript = transcript_list.find_transcript(['de', 'en'])
    transcript = transcript_list.find_transcript(['en'])
    translated_transcript = transcript.translate('en')
    return translated_transcript.fetch()  
# @app.route('/<p>')
# def process_input(input_data):
#     # Add your logic to process the input data here
#     # For example, you can convert the input to uppercase
#     return f"<h1>{input_data}</h1>"
@app.route('/out')
def out():
    # Add your logic to process the input data here
    # For example, you can convert the input to uppercase
     return render_template('out.html')


if __name__ == '__main__':
    app.run(debug=True)
