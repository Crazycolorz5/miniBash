from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
from flask_cors import CORS
from subprocess import run
from os import chdir

# timeout for bash commands in seconds
timeout = 10

def runCommand(cmd: str) -> tuple[str, str]:
    res = run(cmd.split(), timeout=timeout, capture_output=True)
    print("Running: " + cmd)
    return str(res.stdout, encoding='utf-8'), str(res.stderr, encoding='utf-8')

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5174"}})

@app.route("/ls", methods=['GET'])
def ls():
    stdout, stderr = runCommand("ls")
    return {"stdout": stdout, "stderr": stderr}

@app.route("/pwd", methods=['GET'])
def pwd():
    stdout, stderr = runCommand("pwd")
    return {"stdout": stdout, "stderr": stderr}

def cd(d):
    try:
        chdir(d)
        return {"stdout": "", "stderr": ""}
    except:
        return {"stdout": "", "stderr": "cd: " + d + ": No such file or directory"}

@app.route("/cd", methods=['POST'])
def cdapi():
    try:
        s = request.get_json()["dir"]
        print("Running: cd " + s)
        assert isinstance(s, str)
        return cd(s)
    except:
        return {"stdout": "", "stderr": "cd: No directory provided"}

@app.route("/upload", methods=['POST'])
def upload():
    try:
        file = request.files['file']
        if file and file.filename:
            print("Running: file upload: " + file.filename)
            file.save(secure_filename(file.filename))
            return {"stdout": "File uploaded successfully!", "stderr": ''}
        else: raise Exception
    except:
        return {"stdout": "", "stderr": "Error in file upload."}