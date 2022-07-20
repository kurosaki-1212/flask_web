import cv2


# モザイクをかける関数
def mozaiku(img, rect, size):
    # モザイクをかける領域を取得
    (x1, y1, x2, y2) = rect
    w = x2 - x1
    h = y2 - y1
    i_rect = img[y1:y2, x1:x2]

    # モザイク処理のため、一度縮小して拡大する
    i_small = cv2.resize(i_rect, (size, size))
    i_moz = cv2.resize(i_small, (w, h), interpolation=cv2.INTER_AREA)

    # 画像にモザイク画像を重ねる
    img2 = img.copy()
    img2[y1:y2, x1:x2] = i_moz
    return img2
    

# 画像の前処理をする関数
def face_mozaiku(image):
    # ファイルが見つからない時の例外処理を行う
    try:
        # カスケードファイル「static/haarcascade_frontalface_default.xml」を指定
        cascade_file = 'static/haarcascade_frontalface_default.xml'
        # 分類機を作成
        cascade = cv2.CascadeClassifier(cascade_file)
    except Exception as e:
        print(e)

    # 画像の読み込む
    img = cv2.imread(image)

    # 例外処理としてエラーが発生した際に値を返す
    try:
        # グレイスケール（白黒）に変換
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    except:
        print('エラーが発生しました')
        print('ファイル名に日本語は入っていませんか？')
        print('画像を参照していますか？')
        print('指定のファイルの中の画像を参照していますか？')
        return '', '', 'ダウンロードできませんでした'

    # 顔検出を実行
    face_list = cascade.detectMultiScale(img_gray, minSize=(150, 150))

    # 顔を検出できなかった場合そのまま出力する
    try:
        # face_listの長さが0なら終了
        if len(face_list) == 0:
            print('失敗')
            quit()
    except:
        print('顔を検出できませんでした。')
        print('そのまま出力します。')

    # 認識した部分の画像にモザイクをかける
    for (x, y, w, h) in face_list:
        img = mozaiku(img, (x, y, x+w, y+h), 10)

    #画像を出力
    mozaiku_path = 'static/image/{}_mozaiku.jpg'.format(image[13:-4])
    mozaiku_name = '{}_mozaiku.jpg'.format(image[13:-4])
    # 画像を保存する
    cv2.imwrite("static/image/" + mozaiku_name, img)
    success = 'ダウンロードしました'

    # 「ファイルがある場所」と「ファイル名」と「ダウンロード成功の文字」を返す
    return mozaiku_path, mozaiku_name, success
