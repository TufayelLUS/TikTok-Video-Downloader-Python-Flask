from flask import Flask, url_for, redirect, render_template, request, send_file
import requests
import re
import os
import random
import string


app = Flask(__name__)
if not os.path.exists("downloads"):
    os.mkdir("downloads")


def createRandomString():
    randStr = ""
    strSet = string.digits + string.ascii_letters
    for i in range(10):
        randStr += random.choice(strSet)
    return randStr


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/download/')
def download():
    if request.args.get('link') is not None:
        link = request.args.get('link')
        if link == "":
            return redirect("/")
    else:
        return redirect("/")
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
    }
    s = requests.Session()
    resp = s.get(link, headers=headers).text
    video_link = re.findall(
        r'property="og:video:secure_url" content="(.*?)"', resp)[0]
    video_link = video_link.replace('&amp;', '&')
    headers = {
        'Range': 'bytes=0-',
        'Referer': 'https://www.tiktok.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
    }
    content = s.get(video_link, headers=headers).content
    rand_name = createRandomString()
    open('downloads/{}.mp4'.format(rand_name), mode='wb+').write(content)
    return send_file('downloads/{}.mp4'.format(rand_name), as_attachment=True)


if __name__ == "__main__":
    app.run()
