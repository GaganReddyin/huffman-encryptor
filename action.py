import os, time, glob
from flask import Flask, redirect, url_for, request, render_template, send_file

app = Flask(__name__)

global filename
global filetype

@app.route('/')
def home():

    #delete old files
    filelist = glob.glob('uploads/*')

    for f in filelist:
        os.remove(f)

    filelist = glob.glob('downloads/*')

    for f in filelist:
        os.remove(f)
        
    return render_template("home.html")

app.config["FILE_UPLOADS"] = "/uploads"


@app.route("/encrypt", methods=["GET", "POST"])
def encrypt():
    if request.method == "GET":
        return render_template("encrypt.html", check = 0)

    else:
        up_file = request.files["file"]

        if len(up_file.filename) > 0:
            global filename
            global ftype
            filename = up_file.filename
            print(up_file.filename)
            up_file.save(os.path.join(app.config["FILE_UPLOADS"], filename))
            os.system('python h.py uploads/{}'.format(filename))
            filename = filename[:filename.index(".",1)]
            ftype = "-encrypted.huf"
            while True:
                if 'uploads/{}-encrypted.huf'.format(filename) in glob.glob('uploads/*-encrypted.huf'):
                    os.system('mv uploads/{}-encrypted.huf downloads/'.format(filename))
                    break

            return render_template("encrypt.html", check = 1)

        else:
            print("ERROR")
            return render_template("encrypt.html", check = -1)




@app.route("/decrypt", methods=["GET", "POST"])
def decrypt():

    if request.method == "GET":
        return render_template("decrypt.html", check = 0)

    else:
        up_file = request.files["file"]
        key_file = request.files["key"]
        print("Hello")
        print(key_file.name)

        if len(up_file.filename) > 0:
            global filename
            global ftype
            filename = up_file.filename
            print(up_file.filename)
            up_file.save(os.path.join(app.config["FILE_UPLOADS"], filename))
            key_file.save((os.path.join(app.config["FILE_UPLOADS"], "key.txt")))
            os.system('python outputDecode.py uploads/{}'.format(filename))

            keyfilename = "uploads/key.txt"
            f = open(keyfilename, 'r')
            ftype = (f.readline()).strip()
            filename = filename[:filename.index("-",1)]

            ftype = "-decrypted." + ftype
            # f = open('uploads/{}'.format(filename), 'rb')
            # ftype = "-decrypted." + (f.read(int(f.read(1)))).decode("utf-8")
            # filename = filename[:filename.index("-",1)]
            print("ftype")
            print(filename)
            print(ftype)

            # while True:
            #     if 'downloads/{}{}'.format(filename, ftype) in glob.glob('downloads/*-decrypted.*'):
            #         print("inside loop")
            #         # os.system('mv uploads/{}{} downloads/'.format(filename, ftype))
                    
            #         break

            return render_template("decrypt.html", check = 1)
        else:
            print("ERROR")
            return render_template("decrypt.html", check = -1)



@app.route("/download")
def download_file():
    global filename
    global ftype
    path = "downloads/" + filename + ftype
    return send_file(path, as_attachment = True)

@app.route("/downloadKey")
def downloadKey_file():
    path = "downloads/" + "key.txt"
    return send_file(path, as_attachment = True)


# Restart application whenever changes are made
if __name__ == '__main__':
   app.run(debug = True)
