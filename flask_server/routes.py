from flask import Flask, request, jsonify
from flask_server.src.manager import Manager
from flask_server.src.images import ImageData
from flask_server.src import Path

manager = Manager()
manager.initialize()
app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

# ------------------   IMAGE BANK OPERATIONS -------------------------


@app.route('/images', methods=['LIST'])
def get_image_list():
    image_list = manager.image_bank.compile_image_list()
    return jsonify({"cards": image_list}), 200


@app.route('/images', methods=['POST'])
def import_image():
    data = request.get_json()
    image_uuid, image_data = manager.image_bank.import_image(Path(data['image_path']), data['image_name'])
    return jsonify({"uuid": str(image_uuid), "image_data": image_data.__dict__}), 201


@app.route('/images/<uuid>', methods=['DELETE'])
def delete_image(uuid):
    manager.image_bank.delete_image(uuid)
    return jsonify(message=f"image {uuid} deleted"), 204


@app.route('/images/<uuid>/data', methods=['PUT'])
def update_image_data(uuid):
    data = request.get_json()
    image_data = ImageData(data["name"], data["data"])
    manager.image_bank.write_image_metadata(uuid, image_data)
    return jsonify({"message": f"Metadata for image {uuid} updated successfully"}), 200


@app.route('/images/<uuid>/data', methods=['GET'])
def get_image_data(uuid):
    image_data = manager.image_bank.read_image_metadata(uuid)
    return jsonify({"data": image_data.__dict__}), 200


@app.route('/registry', methods=['LIST'])
def get_project_list():
    projects = manager.registry.get_project_names()
    return jsonify({"projects": projects}), 200


@app.route('/registry', methods=['POST'])
def create_project():
    data = request.get_json()
    project_name = data.get("project_name")

    if not project_name:
        return jsonify({"error": "Project name is required"}), 400

    manager.registry.create_project(project_name)
    manager.load_project(project_name)
    return jsonify({"message": f"Project '{project_name}' created successfully"}), 201


@app.route('/registry/<project_name>', methods=['POST'])
def open_project(project_name):
    manager.load_project(project_name)
    return jsonify({"message": f"Project '{project_name}' open successfully"}), 200


@app.route('/project', methods=['GET'])
def get_active_branch():
    active_branch = manager.project.get_active_branch()
    return jsonify({"active_branch": active_branch}), 200


@app.route('/project', methods=['LIST'])
def get_branch_list():
    branches = manager.project.get_branches()
    return jsonify({'branch_list': branches}), 200


@app.route('/project', methods=['PUT'])
def create_branch():
    data = request.get_json()
    manager.project.create_branch(data['branch_name'], data['message'])
    return jsonify(message=f"branch {data['branch_name']} created"), 201


@app.route('/project', methods=['SAVE'])
def save():
    data = request.get_json()
    manager.project.save_changes(data["message"])
    return jsonify(message=f"file saved"), 201


@app.route('/project', methods=['RESET'])
def reset():
    manager.project.rollback()
    return jsonify(message=f"all changed discarded"), 205


@app.route('/project/<branch>', methods=['LIST'])
def get_commit_list(branch):
    commits = manager.project.get_commit_list(branch)
    return jsonify({'branches': commits}), 201


@app.route('/project/<branch>', methods=['LOAD_BRANCH'])
def load(branch):
    manager.project.load_branch(branch)
    return jsonify(message=f"Branch {branch} loaded"), 200


@app.route('/project/<commit>', methods=['LOAD_COMMIT'])
def load_commit(commit):
    manager.project.load_commit(commit)
    return jsonify(manager=f"Commit {commit} loaded"), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000, host="localhost")
