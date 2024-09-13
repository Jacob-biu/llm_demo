from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import send_from_directory
import shutil


import os

app = Flask(__name__)
CORS(app)

# 设置文件上传保存路径
UPLOAD_FOLDER = '/home/bxliu/miniconda/LLM/llm_demo_0_2_1/llm_demo/server/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 确保上传文件夹存在
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def get_all_files(directory):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.abspath(os.path.join(root, file))
            file_list.append(file_path)
    return file_list

@app.route('/get_files', methods=['POST'])
def get_file_paths():
    data = request.json
    dataset = data.get('dataset')
    if not dataset:
        return jsonify({'error': 'No dataset provided'}), 400
    
    directory = os.path.join(app.config['UPLOAD_FOLDER'], dataset)
    if not os.path.exists(directory):
        return jsonify({'error': 'Directory does not exist'}), 404
    
    try:
        files = get_all_files(directory)
        return jsonify({'files': files})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 上传文件 API
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or 'datasetName' not in request.form:
        return jsonify({'error': 'File and dataset name are required'}), 400

    file = request.files['file']
    dataset_name = request.form['datasetName']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # 创建数据集对应的文件夹
    dataset_folder = os.path.join(app.config['UPLOAD_FOLDER'], dataset_name)
    if not os.path.exists(dataset_folder):
        os.makedirs(dataset_folder)

    # 保存文件到数据集文件夹中
    file_path = os.path.join(dataset_folder, file.filename)
    file.save(file_path)
    
    # 获取文件的绝对路径
    absolute_file_path = os.path.abspath(file_path)
    return jsonify({'message': 'File uploaded successfully', 'file_path': absolute_file_path})

# 获取文件列表 API
@app.route('/files', methods=['GET'])
def list_files():
    dataset_name = request.args.get('datasetName')  # 从查询参数中获取 datasetName
    if not dataset_name:
        return jsonify({'error': 'Dataset name is required'}), 400

    dataset_folder = os.path.join(UPLOAD_FOLDER, dataset_name)

    files = []

    if not os.path.exists(dataset_folder):
        os.makedirs(dataset_folder)  # 创建文件夹


    try:
        # 获取指定文件夹下的文件信息
        for file_name in os.listdir(dataset_folder):
            file_path = os.path.join(dataset_folder, file_name)
            file_info = {
                'name': file_name,
                'uploadDate': os.path.getctime(file_path),
                'enabled': True,
                'parseStatus': '未解析'
            }
            files.append(file_info)

        return jsonify(files), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 删除文件 API
@app.route('/delete/<dataset_name>/<file_name>', methods=['DELETE'])
def delete_file(dataset_name, file_name):
  try:
    dataset_folder = os.path.join(UPLOAD_FOLDER, dataset_name)
    file_path = os.path.join(dataset_folder, file_name)

    if not os.path.exists(file_path):
      return jsonify({'error': 'File not found'}), 404

    # 获取文件的绝对路径
    absolute_file_path = os.path.abspath(file_path)
  
    os.remove(file_path)  # 删除文件
    return jsonify({'message': 'File deleted successfully','file_path': absolute_file_path}), 200
  except Exception as e:
        return jsonify({'error': str(e)}), 500

# 更改文件名 API
@app.route('/rename', methods=['POST'])
def rename_file():
    data = request.get_json()
    dataset_name = data.get('datasetName')
    old_filename = data.get('oldFilename')
    new_filename = data.get('newFilename')

    if not dataset_name or not old_filename or not new_filename:
        return jsonify({'error': 'Dataset name, old filename, and new filename are required'}), 400

    dataset_folder = os.path.join(UPLOAD_FOLDER, dataset_name)
    old_file_path = os.path.join(dataset_folder, old_filename)
    new_file_path = os.path.join(dataset_folder, new_filename)

    try:
        if not os.path.exists(old_file_path):
            return jsonify({'error': 'File not found'}), 404

        # 更改文件名
        os.rename(old_file_path, new_file_path)
        return jsonify({'message': 'File renamed successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/download/<dataset_name>/<filename>', methods=['GET'])
def download_file(dataset_name,filename):
    try:
        dataset_folder = os.path.join(UPLOAD_FOLDER, dataset_name)
        file_path = os.path.join(dataset_folder, filename)

        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        return send_from_directory(directory=dataset_folder, path=filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 删除数据集文件夹 API
@app.route('/delete_dataset/<dataset_name>', methods=['DELETE'])
def delete_dataset(dataset_name):
    dataset_folder = os.path.join(UPLOAD_FOLDER, dataset_name)

    try:
        if not os.path.exists(dataset_folder):
            return jsonify({'error': 'Dataset not found'}), 404

        # 删除整个文件夹及其内容
        shutil.rmtree(dataset_folder)
        return jsonify({'message': 'Dataset deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# 递归获取文件树结构
@app.route('/allFiles', methods=['GET'])
def get_files():
    def list_files(dir_path):
        file_list = []
        for item in os.listdir(dir_path):
            item_path = os.path.join(dir_path, item)
            if os.path.isdir(item_path):
                # 如果是文件夹，递归获取子文件
                file_list.append({
                    'name': item,
                    'children': list_files(item_path)
                })
            else:
                # 如果是文件，返回文件路径
                file_list.append({
                    'name': item,
                    'filePath': os.path.relpath(item_path, UPLOAD_FOLDER)
                })
        return file_list

    file_tree = list_files(UPLOAD_FOLDER)
    return jsonify(file_tree)

# 提供静态文件预览
@app.route('/allFiles/<path:filename>', methods=['GET'])
def serve_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)