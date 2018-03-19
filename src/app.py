import os

from flask import Flask, request, render_template, send_from_directory, redirect, url_for
from google.cloud import storage
from config import *

__author__ = 'Tony DiGangi'

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("upload.html")


@app.route("/upload", methods=["POST"])
def upload():
    """Process the uploaded file and upload it to Google Cloud Storage."""
    uploaded_file = request.files.get('file')

    if not uploaded_file:
        return 'No file uploaded.', 400

    # Create a Cloud Storage client.
    gcs = storage.Client()

    # Get the bucket that the file will be uploaded to.
    bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)
    # Create a new blob and upload the file's content.
    blob = bucket.blob(uploaded_file.filename)

    blob.upload_from_string(
        uploaded_file.read(),
        content_type=uploaded_file.content_type
    )

    filename = uploaded_file.filename
    cdn_path = "http://130.211.5.246/{}".format(filename)

    return render_template("complete_display_image.html", image_name=cdn_path)


@app.route('/gallery')
def get_gallery():
    gcs = storage.Client()
    bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)
    blobs = list(bucket.list_blobs())
    image_names = []
    for filename in blobs:
        cdn_path = "http://130.211.5.246/{}".format(filename.name)
        image_names.append(cdn_path)

    return render_template("gallery.html", image_names=image_names)


if __name__ == "__main__":
    app.run(port=4555, debug=True)
