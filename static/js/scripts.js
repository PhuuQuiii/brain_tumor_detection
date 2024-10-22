// Khi nhấn vào dấu + sẽ mở hộp chọn file
document.getElementById("plusIcon").addEventListener("click", function () {
  document.getElementById("fileInput").click();
});

// Hiển thị ảnh khi người dùng chọn file
function previewImage(event) {
  var reader = new FileReader();
  reader.onload = function () {
    var imagePreview = document.getElementById("imagePreview");
    imagePreview.src = reader.result;
    imagePreview.style.display = "block";
    document.getElementById("alert").style.display = "none"; // Ẩn cảnh báo nếu chọn ảnh
  };
  reader.readAsDataURL(event.target.files[0]);
}

// Kiểm tra nếu người dùng chưa chọn ảnh
function validateForm() {
  var fileInput = document.getElementById("fileInput");

  // Kiểm tra nếu không có tệp nào được chọn
  if (fileInput.files.length === 0) {
    document.getElementById("alert").style.display = "block";
    return false; // Ngăn form submit nếu không có file nào
  }

  return true; // Cho phép submit nếu file được chọn
}
