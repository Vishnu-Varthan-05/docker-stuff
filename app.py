from flask import Flask, jsonify, request
import docker

app = Flask(__name__)
client = docker.from_env()  

@app.route("/containers", methods=["GET"])
def list_containers():
    containers = client.containers.list(all=True)
    container_data = [{"id": c.id, "name": c.name, "status": c.status} for c in containers]
    return jsonify(container_data)

@app.route("/containers/start/<container_id>", methods=["POST"])
def start_container(container_id):
    try:
        container = client.containers.get(container_id)
        container.start()
        return jsonify({"message": f"Container {container_id} started"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/containers/stop/<container_id>", methods=["POST"])
def stop_container(container_id):
    try:
        container = client.containers.get(container_id)
        container.stop()
        return jsonify({"message": f"Container {container_id} stopped"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/images", methods=["GET"])
def list_images():
    images = client.images.list()
    image_data = [{"id": img.id, "tags": img.tags} for img in images]
    return jsonify(image_data)

@app.route("/images/pull", methods=["POST"])
def pull_image():
    data = request.get_json()
    image_name = data.get("image")
    try:
        client.images.pull(image_name)
        return jsonify({"message": f"Image {image_name} pulled successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "_main_":
    app.run(debug=True, port=5000)