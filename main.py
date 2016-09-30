from flask import Flask
from cStringIO import StringIO
from PIL import Image, ImageDraw
from json import load
from random import choice

app = Flask(__name__)

def flow(string):
    flowstack = [""]
    curlen = 0
    for chunk in string.split():
        if curlen + len(chunk) >= 29:
            flowstack.append("\n")
            curlen = 0
        flowstack.append(chunk)
        curlen += len(chunk)
    return " ".join(flowstack)


@app.route("/")
def root():
    strings = load(open("memes.json"))
    string = flow(choice(strings))

    image = Image.open("base.png")

    d = ImageDraw.Draw(image)
    d.multiline_text((35,335), string, fill=(255,0,0))

    outfile = StringIO()
    image.save(outfile, "png")

    return outfile.getvalue(), 200, [("Content-Type", "image/png")]

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
