from flask import Flask
from flask import render_template
from werkzeug.utils import secure_filename
from flask import request
from flask_bootstrap import Bootstrap

# 呼び出すファイルをインポート
import polly
import face_mozaiku

# Flaskインスタンスを生成
app = Flask(__name__)
bootstrap = Bootstrap(app)


# 直接アクセスした場合もメニューに強制遷移
@app.route('/')
def index():
    return render_template('sample.html')


# メニュー画面
@app.route('/menu/')
def polly_menu():
    return render_template('sample.html')


# ==================================
# 音声合成サービス
@app.route('/polly')
def polly_top():
    return render_template('polly.html', input_text='', output_text='')

# 音声合成を開始する
@app.route('/polly', methods=['POST'])
def polly_play():
    # リクエストパラメータを読み込む
    in_text = request.form['input_text']
    in_polly = request.form['input_polly']
    # リクエストパラメータが空ならinput_textとoutput_textは空表示のままpolly.htmlを表示する
    if in_text == '':
        return render_template('polly.html', input_text='', output_text='')

    # pollyファイルのpolly関数を呼び出す
    polly.polly(in_text, in_polly)
    return render_template('polly.html', input_text=in_text)
# ==================================


# ==================================
# モザイク処理サービス
@app.route('/mozaiku', methods=['GET', 'POST'])
def face():
    # method が POST か否かを判断
    # POST のとき
    if request.method == 'POST':
        # ファイルのリクエストパラメータを取得
        f = request.files.get('image')
        # ファイル名を取得
        filename = secure_filename(f.filename)
        # ファイルを保存するディレクトリを指定
        filepath = 'static/image/' + filename
        # face_mozaikuファイルのface_mozaiku関数を呼び出す
        mozaiku_path, mozaiku_name, success = face_mozaiku.face_mozaiku(filepath)

    # GET のとき
    else:
        filename = ''
        mozaiku_path = ''
        mozaiku_name = ''
        success = ''

    # htmlに挿入する変数を指定
    return render_template('face_mozaiku.html',
                           filename=filename,
                           image_url=mozaiku_path,
                           image_name=mozaiku_name,
                           success=success)
# ==================================


# プログラムの実行
if __name__ == '__main__':
    app.run(debug=True)
