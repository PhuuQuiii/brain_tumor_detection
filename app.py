from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import numpy as np
import os
from Predict import LoadModel, LoadImage, Prediction


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'



# Hàm dự đoán kết quả từ ảnh
def predict_tumor(model_path, img_path):
    model = LoadModel(model_path)

    img_array = LoadImage(img_path)
    results = Prediction(img_array, model)

    # Kết quả cuối cùng là loại u não có phần trăm lớn nhất
    final_prediction = max(results, key=results.get)
    
    return results, final_prediction

# Route cho trang upload ảnh
@app.route('/')
def upload_image():
    return render_template('upload.html')

# Route xử lý ảnh và dự đoán
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(request.url)

    if file:
        # Lưu tệp ảnh vào thư mục static/uploads
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], "tumor.png")
        file.save(file_path)

        filename = "tumor.png"
        
        # Trả về kết quả dự đoán giả
        results, final_prediction = predict_tumor(model_path="./models/BrainTumor_3.h5", img_path=file_path)

        for data in results:
            print(f"{data}: {results[data] * 100}%")

        results_percent = {key: value * 100 for key, value in results.items()}
        
        # Sử dụng tên file để hiển thị ảnh đúng cách
        return render_template('result.html', image_name=filename, results=results_percent, final_prediction=final_prediction)


if __name__ == "__main__":
    app.run(debug=True)
