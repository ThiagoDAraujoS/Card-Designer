from flask import Flask, request, jsonify
from flask_server.src.manager import Manager
from flask_server.src.images import ImageData
from flask_server.src import Path

manager = Manager()
app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route("/install", methods=['GET'])
def install():
    manager.install()
    manager.initialize_components()
    return jsonify(message="application installed"), 200


@app.route("/initialize", methods=["GET"])
def initialize():
    manager.initialize_components()
    return jsonify(message="components initialized"), 200


@app.route('/projects', methods=['GET'])
def project_names():
    return manager.registry.get_project_names(), 200


# IMAGE BANK OPERATIONS
@app.route('/image-bank/reload', methods=['GET'])
def get_image_list():
    image_list = manager.image_bank.compile_image_list()
    return jsonify({"cards": image_list})


@app.route('/image-bank/import', methods=['POST'])
def import_image():
    data = request.get_json()
    image_uuid, image_data = manager.image_bank.import_image(Path(data['image_path']), data['image_name'])
    return jsonify({"uuid": str(image_uuid), "image_data": image_data.__dict__})


@app.route('/image-bank/card/<uuid>', methods=['PUT'])
def update_image_metadata(uuid):
    data = request.get_json()
    image_data = ImageData(data["name"], data["data"])
    manager.image_bank.write_image_metadata(uuid, image_data)
    return jsonify({"message": f"Metadata for image {uuid} updated successfully"})


@app.route('/image-bank/metadata/<uuid>', methods=['GET'])
def get_image_metadata(uuid):
    image_data = manager.image_bank.read_image_metadata(uuid)
    return jsonify(image_data.__dict__)


@app.route('/image-bank/metadata/<uuid>', methods=['DELETE'])
def delete_image(uuid):
    manager.image_bank.delete_image(uuid)
    return jsonify(message="image deleted"), 200

# -------- Registry ------------


@app.route('/registry/projects', methods=['POST'])
def create_project():
    data = request.get_json()
    project_name = data.get("project_name")
    if not project_name:
        return jsonify({"error": "Project name is required"}), 400

    manager.registry.create_project(project_name)
    manager.load_project(project_name)
    return jsonify({"message": f"Project '{project_name}' created successfully"}), 201


@app.route('/registry/projects/<project_name>', methods=['GET'])
def open_project(project_name):
    manager.load_project(project_name)
    return jsonify({"message": f"Project '{project_name}' open successfully"}), 201


# @app.route('/registry/projects/folder', methods=['GET'])
# def open_projects_folder():
#     project_folder = manager.registry.path
#     return jsonify({"projects_folder": str(project_folder)})


@app.route('/registry/projects', methods=['GET'])
def get_project_list():
    projects = manager.registry.get_project_names()
    return jsonify({"projects": projects})

# ------------------ Card Set -------------------

# Save changes

# Create new save file

# get save files

# discard changes

# load save file

# load save state

# create card

# Update card

# fetch card

# get card list

# get changed cards list




if __name__ == '__main__':
    app.run(debug=True, port=5000, host="localhost")
