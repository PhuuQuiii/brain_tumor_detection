from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import numpy as np
import os
import tensorflow as tf

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Load mô hình u não đã được huấn luyện sẵn
# model = tf.keras.models.load_model('E:/brain_tumor_detection/models/')

# Tạm thời bỏ qua phần xử lý bằng mô hình, dùng dữ liệu giả để kiểm tra giao diện
def predict_tumor(img_path):
    # Trả về kết quả dự đoán giả
    results = {
        'No Tumor': 70.0,
        'Glioma': 10.0,
        'Meningioma': 15.0,
        'Pituitary': 5.0
    }
    
    # Kết quả giả: loại có phần trăm lớn nhất
    final_prediction = max(results, key=results.get)
    
    return results, final_prediction

# # Hàm dự đoán kết quả từ ảnh
# def predict_tumor(img_path):
#     img = Image.open(img_path).resize((150, 150))  # Giả sử model nhận ảnh 150x150
#     img_array = np.array(img) / 255.0  # Chuẩn hóa ảnh
#     img_array = np.expand_dims(img_array, axis=0)  # Thêm batch dimension
    
#     predictions = model.predict(img_array)[0]  # Lấy kết quả dự đoán
#     no_tumor_prob = predictions[0]  # Xác suất không có u não
#     glioma_prob = predictions[1]    # Xác suất glioma
#     meningioma_prob = predictions[2] # Xác suất meningioma
#     pituitary_prob = predictions[3]  # Xác suất pituitary

#     results = {
#         'No Tumor': no_tumor_prob * 100,
#         'Glioma': glioma_prob * 100,
#         'Meningioma': meningioma_prob * 100,
#         'Pituitary': pituitary_prob * 100
#     }

#     # Kết quả cuối cùng là loại u não có phần trăm lớn nhất
#     final_prediction = max(results, key=results.get)
    
#     return results, final_prediction

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
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Trả về kết quả dự đoán giả
        results, final_prediction = predict_tumor(file_path)
        
        # Sử dụng tên file để hiển thị ảnh đúng cách
        return render_template('result.html', image_name=filename, results=results, final_prediction=final_prediction)


if __name__ == "__main__":
    app.run(debug=True)
