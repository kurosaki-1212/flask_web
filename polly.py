import boto3
import contextlib
import os


# 音声を再生する関数
def polly(text, voice):
    # import時に実行されないように関数化しておく
    # また、textは引数で受け取れるように変更する
    polly = boto3.client('polly')
    # 読み込めない文字が出てきた際の例外処理
    try:
        result = polly.synthesize_speech(
            Text=text, OutputFormat='mp3', VoiceId=voice)
    except Exception as e:
        print(e)
    path = 'polly_synth.mp3'

    # 音声ストリームの再生
    # 再生できなかった際の例外処理
    try:
        with contextlib.closing(result['AudioStream']) as stream:
            # 作成した音声出力ファイルを開く
            with open(path, 'wb') as file:
                file.write(stream.read())
    except Exception as e:
        print(e)

    # mp3を再生する
    os.startfile(path)
