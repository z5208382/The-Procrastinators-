import sys
import os
from flask import Flask, send_from_directory

if len(sys.argv) == 2:
    f = open('prebundle/config.js', 'w')
    f.write('var LOCAL_ENV = true\n')
    f.write('var BACKEND_PORT = ' + str(sys.argv[1]))
    f.close()

app = Flask(__name__, static_folder='prebundle')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        print(app.static_folder, path)
        return send_from_directory(app.static_folder, path)
    else:
        print(app.static_folder, 'index.html')
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(port=0, threaded=True)

