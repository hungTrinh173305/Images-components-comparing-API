import os
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import cv2
import numpy as np

UPLOAD_FOLDER = 'static/uploads/'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_image():
    if 'files[]' not in request.files:
        flash('No file part')
        return redirect(request.url)
    files = request.files.getlist('files[]')
    file_names = []
    img_to_compare_names = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_names.append(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img_to_compare_names.append('static/uploads/'+file.filename)
    img1 = cv2.imread(img_to_compare_names[0])
    img2 = cv2.imread(img_to_compare_names[1])
    width, height = 500, 500  # set the desired width and height
    img1 = cv2.resize(img1, (width, height))
    img2 = cv2.resize(img2, (width, height))
    # convert the images to grayscale
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # compute the absolute difference between the images
    diff = cv2.absdiff(gray1, gray2)

    # threshold the difference image to binary
    thresh_value = 50
    _, thresh = cv2.threshold(diff, thresh_value, 255, cv2.THRESH_BINARY)

    # find contours in the thresholded image
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # draw rectangles around the contours
    for contour in contours:
        if cv2.contourArea(contour) < 25:
            continue
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(img1, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.rectangle(img2, (x, y), (x + w, y + h), (255, 0, 0), 2)

    Hori = np.concatenate((img1, img2), axis=1)

    path_of_res = 'static/results'
    dir_list = os.listdir(path_of_res)
    if len(dir_list) == 0:
        new_name_res = "result1.jpg"
    elif len(dir_list) == 1:
        new_name_res = "result2.jpg"
    else:
        new_name_res = "result"+str(len(dir_list)+1)+'.jpg'

    cv2.imwrite("static/results/"+new_name_res, Hori)
    print(file_names)
    return render_template('upload.html', filenames=[new_name_res])


@app.route('/display/<filename>')
def display_result(filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='results/' + filename), code=301)


if __name__ == "__main__":
    app.run()