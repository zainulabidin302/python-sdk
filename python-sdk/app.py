from flask import Flask, jsonify, request
from facepp import API, File
import base64
from flask_cors import CORS
import apikey
from time import sleep

app = (Flask(__name__))
CORS(app)


api = API(apikey.API_KEY, apikey.API_SECRET)


from pprint import pformat
from time import sleep
def print_result(hit, result):
    def encode(obj):
        if type(obj) is unicode:
            return obj.encode('utf-8')
        if type(obj) is dict:
            return {encode(v): encode(k) for (v, k) in obj.iteritems()}
        if type(obj) is list:
            return [encode(i) for i in obj]
        return obj
    print hit
    result = encode(result)
    print '\n'.join("  " + i for i in pformat(result, width=75).split('\n'))



@app.route("/")
def index() :
    data = { "user": 1}
    return jsonify(data)

@app.route("/upload", methods=['POST'] )
def upload() :

    Face = {}
    res = api.detect(image_base64=request.get_json()['image'])
    print_result("person_one", res)
    Face['person_one'] = res["faces"][0]["face_token"]
    sleep(5)

    api.faceset.addface(outer_id='test', face_tokens=Face.itervalues())
    data = jsonify('done')

    return data


@app.route("/compare", methods=['POST'])
def compare():
    Face = {}
    d = request.get_json()
    ret = api.detect(image_base64=d['image'])
    fsid = d['faceset_id']

    if (len(ret['faces']) < 1):
        return jsonify('no face detected!')
    sleep(5)

    search_result = api.search(face_token=ret["faces"][0]["face_token"], outer_id='test')

    print(search_result)

    data = jsonify('done')

    return data


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")