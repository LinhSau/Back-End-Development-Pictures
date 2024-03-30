from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    list_url = []
    if data:
        for pic in data:
            url = pic.get('pic_url')
            list_url.append(url)
    return jsonify(list_url), 200
######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    if not id:
        return 404
    if id:
        for pic in data:
            if id == pic['id']:
                return jsonify(pic)
    return jsonify({"error": "Picture not found"}), 404
    
######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    new_pic = request.json
    if new_pic:
        for pic in data:
            if new_pic['id'] == pic['id']:
                return {"Message": f"picture with id {new_pic['id']} already present"}, 302
        data.append(new_pic)
        return {'id': new_pic['id']}, 201
    return {"message": "Internal server error"}, 204

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    upd_pic = request.json
    if upd_pic:
        for index, pic in enumerate(data):
            if id == pic['id']:
                data[index] = upd_pic
                return {"Message": "success"}, 200
        return {"message": "picture not found"}, 404
    return {"message": "Internal server error"}, 500

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    if id:
        for index, pic in enumerate(data):
            if id == pic['id']:
                data.remove(pic)
                print(len(data))
                return {"Message": "success"}, 204
        return {"message": "picture not found"}, 404

