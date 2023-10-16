from flask import Flask, render_template, jsonify, request
from datetime import datetime
import ssl
from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@cluster0.gz7pp7h.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp', ssl_cert_reqs=ssl.CERT_NONE)
db = client.dbsparta
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/diary", methods=["POST"])
def diary_post():
    count = db.diary.count_documents({})
    num = count + 1

    title_receive = request.form['title_give']
    story_receive = request.form['story_give']
    current_time = datetime.now()
    timeprint = current_time.strftime('%Y.%m.%d')
    timefile = current_time.strftime('%Y-%m-%d-%H-%M-%S')

    img_receive = request.files['img_give']
    extension = img_receive.filename.split('.')[-1]
    filename = f'file-{timefile}.{extension}'
    save_to = f'static/{filename}'
    img_receive.save(save_to)

    user_img_receive = request.files['user_img_give']
    user_extension = user_img_receive.filename.split('.')[-1]
    user_filename = f'user-{timefile}.{user_extension}'
    user_save_to = f'static/{user_filename}'
    user_img_receive.save(user_save_to)

    doc = {
        'num':num,
        'image':filename,
        'profilepic':user_filename,
        'title':title_receive,
        'story':story_receive,
        'timestamp': timeprint
    }

    db.diary.insert_one(doc)
    return jsonify({'msg':'Thanks for the Story!'})

@app.route("/diary", methods=["GET"])
def movie_get():
    articles = list(db.diary.find({}, {'_id': False}))
    return jsonify({'articles': articles})


if __name__ == '__main__':  
    app.run('0.0.0.0',port=5000,debug=True)