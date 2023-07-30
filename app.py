from flask import Flask, render_template, request
from logic import generate_pdf

app = Flask(__name__, template_folder='flask_templates')


@app.route('/generate', methods=['POST'])
def generate():
    # ! TODO: add validation to the request, handle errors 
    text = request.json['text']
    
    # ? can be one of 'pdf', 'html'
    return_type = request.json['return_type']

    pdf = generate_pdf(text)

    if return_type == 'pdf':
        return pdf
    elif return_type == 'html':
        return render_template('index.html', text=text ,pdf=pdf)
    else:
        return 'Invalid return type'


# index route
@app.route('/', methods=['GET'])
def index():
    render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
