import os
from flask import Flask, render_template, request, redirect, url_for, flash
from deepface import DeepFace

app = Flask(__name__)
app.secret_key = "your_secret_key"

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
REFERENCE_IMAGE = 'path_to_reference_image'  # Path to the reference image

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register_face():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # You can save the face data to a database or perform other registration tasks here
        flash('Face registered successfully')
        return redirect(url_for('index'))
    else:
        flash('Invalid file type. Allowed file types are .jpg, .jpeg, and .png')
        return redirect(request.url)

@app.route('/recognize', methods=['POST'])
def recognize_face():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        try:
            # Load the reference face data
            reference_img = DeepFace.loadBase64(reference_path)

            # Load the query face
            query_img = DeepFace.loadBase64("replace_with_the_actual_base64_data_of_the_uploaded_image")  # Load the uploaded image here

            result = DeepFace.verify(reference_img, query_img, model_name='Facenet')

            if result['verified']:
                flash('Face recognized successfully')
            else:
                flash('Face not recognized')
            
            return redirect(url_for('index'))
        except Exception as e:
            print(str(e))
            flash('Error processing the image. Please try again.')
            return redirect(request.url)
    else:
        flash('Invalid file type. Allowed file types are .jpg, .jpeg, and .png')
        return redirect(request.url)

if __name__ == '__main__':
    app.run(debug=True)
