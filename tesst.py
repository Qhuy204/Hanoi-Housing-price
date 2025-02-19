import joblib
import numpy as np
import pandas as pd
import os

import pandas as pd

# Tạo danh sách các cột
columnsz = [
    "Area", "Bedrooms", "Bathrooms", "Floors", "Width_meters", "Entrancewidth",
    "Commune_An Khánh", "Commune_An Phú", "Commune_An Thượng", "Commune_An Tiến", "Commune_Bamboo Airways Tower", "Commune_Biên Giang", "Commune_Bách Khoa",
    "Commune_Bán Nhà Tại Quyết Tiến Vân Côn", "Commune_Bát Tràng", "Commune_Bình Minh", "Commune_Bình Yên", "Commune_Bích Hòa", "Commune_Bùi Thị Xuân", "Commune_Bưởi",
    "Commune_Bạch Mai", "Commune_Bạch Đằng", "Commune_Bắc Hồng", "Commune_Bắc Phú", "Commune_Bồ Đề", "Commune_Cao Viên", "Commune_Chi Đông", "Commune_Chúc Sơn",
    "Commune_Chương Dương", "Commune_Cát Linh", "Commune_Cát Quế", "Commune_Cầu Diễn", "Commune_Cầu Dền", "Commune_Cống Vị", "Commune_Cổ Bi", "Commune_Cổ Loa",
    "Commune_Cổ Nhuế 1", "Commune_Cổ Nhuế 2", "Commune_Cổ Đông", "Commune_Cửa Nam", "Commune_Cửa Đông", "Commune_Cự Khê", "Commune_Cự Khối", "Commune_Di Trạch",
    "Commune_Duyên Hà", "Commune_Duyên Thái", "Commune_Dương Hà", "Commune_Dương Nội", "Commune_Dương Quang", "Commune_Dương Xá", "Commune_Dịch Vọng", "Commune_Dịch Vọng Hậu",
    "Commune_Gia Thụy", "Commune_Giang Biên", "Commune_Giáp Bát", "Commune_Giảng Võ", "Commune_Hiền Giang", "Commune_Hiền Ninh", "Commune_Hiệp Thuận", "Commune_Hoàng Diệu",
    "Commune_Hoàng Liệt", "Commune_Hoàng Văn Thụ", "Commune_Hà Cầu", "Commune_Hà Hồi", "Commune_Hàng Buồm", "Commune_Hàng Bài", "Commune_Hàng Bột", "Commune_Hàng Gai",
    "Commune_Hàng Mã", "Commune_Hạ Bằng", "Commune_Hạ Đình", "Commune_Hải Bối", "Commune_Hồng Kỳ", "Commune_Hồng Thái", "Commune_Hợp Thanh", "Commune_Hữu Hòa",
    "Commune_Hữu Văn", "Commune_Khánh Hà", "Commune_Khâm Thiên", "Commune_Khương Mai", "Commune_Khương Thượng", "Commune_Khương Trung", "Commune_Khương Đình", "Commune_Kim Chung",
    "Commune_Kim Giang", "Commune_Kim Lan", "Commune_Kim Liên", "Commune_Kim Mã", "Commune_Kim Nỗ", "Commune_Kim Sơn", "Commune_Kiêu Kỵ", "Commune_Kiến Hưng", "Commune_La Khê",
    "Commune_La Phù", "Commune_Liên Mạc", "Commune_Liên Ninh", "Commune_Liễu Giai", "Commune_Liệp Tuyết", "Commune_Long Biên", "Commune_Láng Hạ", "Commune_Láng Thượng",
    "Commune_Lê Đại Hành", "Commune_Lý Thái Tổ", "Commune_Lĩnh Nam", "Commune_Lại Yên", "Commune_Lệ Chi", "Commune_Mai Dịch", "Commune_Mai Lâm", "Commune_Mai Đình",
    "Commune_Mai Động", "Commune_Minh Khai", "Commune_Minh Phú", "Commune_Minh Trí", "Commune_Minh Đức", "Commune_Mê Linh", "Commune_Mễ Trì", "Commune_Mỗ Lao",
    "Commune_Mỹ Đình 1", "Commune_Mỹ Đình 2", "Commune_Nam Hồng", "Commune_Nam Phương Tiến", "Commune_Nam Đồng", "Commune_Nghĩa Tân", "Commune_Nghĩa Đô", "Commune_Nguyên Khê",
    "Commune_Nguyễn Du", "Commune_Nguyễn Huy Tưởng", "Commune_Nguyễn Trung Trực", "Commune_Nguyễn Trãi", "Commune_Nguyễn Tuân", "Commune_Ngã Tư Sở", "Commune_Ngô Thì Nhậm",
    "Commune_Ngũ Hiệp", "Commune_Ngọc Hà", "Commune_Ngọc Hồi", "Commune_Ngọc Khánh", "Commune_Ngọc Liệp", "Commune_Ngọc Lâm", "Commune_Ngọc Thụy", "Commune_Ngụy Như Kon Tum",
    "Commune_Nhân Chính", "Commune_Nhật Tân", "Commune_Nhị Khê", "Commune_Ninh Sở", "Commune_Phan Chu Trinh", "Commune_Phù Linh", "Commune_Phù Lỗ", "Commune_Phùng",
    "Commune_Phú Cát", "Commune_Phú Diễn", "Commune_Phú La", "Commune_Phú Lãm", "Commune_Phú Lương", "Commune_Phú Minh", "Commune_Phú Mãn", "Commune_Phú Thượng",
    "Commune_Phú Thị", "Commune_Phú Xuyên", "Commune_Phú Đô", "Commune_Phúc Diễn", "Commune_Phúc La", "Commune_Phúc Lợi", "Commune_Phúc Thọ", "Commune_Phúc Tân",
    "Commune_Phúc Xá", "Commune_Phúc Đồng", "Commune_Phương Canh", "Commune_Phương Liên", "Commune_Phương Liệt", "Commune_Phương Mai", "Commune_Phương Trung", "Commune_Phượng Cách",
    "Commune_Phạm Đình Hổ", "Commune_Phố Huế", "Commune_Phụng Châu", "Commune_Quan Hoa", "Commune_Quang Lãng", "Commune_Quang Minh", "Commune_Quang Tiến", "Commune_Quang Trung",
    "Commune_Quán Thánh", "Commune_Quảng An", "Commune_Quất Động", "Commune_Quốc Oai", "Commune_Quốc Tử Giám", "Commune_Quỳnh Lôi", "Commune_Quỳnh Mai", "Commune_Song Phương",
    "Commune_Sài Sơn", "Commune_Sài Đồng", "Commune_Tam Hiệp", "Commune_Tam Hưng", "Commune_Tam Thuấn", "Commune_Thanh Liệt", "Commune_Thanh Lâm", "Commune_Thanh Lương",
    "Commune_Thanh Nhàn", "Commune_Thanh Trì", "Commune_Thanh Xuân Bắc", "Commune_Thanh Xuân Nam", "Commune_Thanh Xuân Trung", "Commune_Thuỷ Xuân Tiên", "Commune_Thành Công",
    "Commune_Thư Phú", "Commune_Thượng Mỗ", "Commune_Thượng Thanh", "Commune_Thượng Đình", "Commune_Thạch Bàn", "Commune_Thạch Hòa", "Commune_Thịnh Liệt", "Commune_Thịnh Quang",
    "Commune_Thọ An", "Commune_Thổ Quan", "Commune_Thụy Hương", "Commune_Thụy Khuê", "Commune_Thụy Lâm", "Commune_Thụy Phương", "Commune_Tiên Dương", "Commune_Tiên Dược",
    "Commune_Tiên Phương", "Commune_Tiến Xuân", "Commune_Tiền Phong", "Commune_Toà Nhà 335 Cầu Giấy", "Commune_Tri Trung", "Commune_Triều Khúc", "Commune_Trung Hòa",
    "Commune_Trung Liệt", "Commune_Trung Phụng", "Commune_Trung Sơn Trầm", "Commune_Trung Tự", "Commune_Trung Văn", "Commune_Tràng Tiền", "Commune_Tráng Việt", "Commune_Trâu Quỳ",
    "Commune_Trúc Bạch", "Commune_Trương Định", "Commune_Trạm Trôi", "Commune_Trần Hưng Đạo", "Commune_Trần Phú", "Commune_Tân Dân", "Commune_Tân Hội", "Commune_Tân Lập",
    "Commune_Tân Mai", "Commune_Tân Minh", "Commune_Tân Phú", "Commune_Tân Tiến", "Commune_Tân Triều", "Commune_Tân Xã", "Commune_Tân Ước", "Commune_Tây Mỗ", "Commune_Tây Tựu",
    "Commune_Tương Mai", "Commune_Tả Thanh Oai", "Commune_Tổ 5 Vĩnh Hưng", "Commune_Tứ Hiệp", "Commune_Tứ Liên", "Commune_Uy Nỗ", "Commune_Việt Hùng", "Commune_Việt Hưng",
    "Commune_Vân Canh", "Commune_Vân Côn", "Commune_Vân Hà", "Commune_Vân Nội", "Commune_Võng La", "Commune_Văn Chương", "Commune_Văn Miếu", "Commune_Văn Quán",
    "Commune_Văn Điển", "Commune_Vĩnh Hưng", "Commune_Vĩnh Ngọc", "Commune_Vĩnh Phúc", "Commune_Vĩnh Quỳnh", "Commune_Vĩnh Tuy", "Commune_Vũ Trọng Phụng", "Commune_Vạn Phúc",
    "Commune_Vạn Yên", "Commune_Xuân Canh", "Commune_Xuân Giang", "Commune_Xuân Khanh", "Commune_Xuân La", "Commune_Xuân Mai", "Commune_Xuân Nộn", "Commune_Xuân Phương",
    "Commune_Xuân Tảo", "Commune_Xuân Đỉnh", "Commune_Yên Hòa", "Commune_Yên Mỹ", "Commune_Yên Nghĩa", "Commune_Yên Phụ", "Commune_Yên Sơn", "Commune_Yên Sở", "Commune_Yên Thường",
    "Commune_Yên Viên", "Commune_Yết Kiêu", "Commune_Ô Chợ Dừa", "Commune_Đa Tốn", "Commune_Đan Phượng", "Commune_Điện Biên", "Commune_Đông Anh", "Commune_Đông Dư",
    "Commune_Đông Hội", "Commune_Đông La", "Commune_Đông Mỹ", "Commune_Đông Ngạc", "Commune_Đông Xuân", "Commune_Đông Yên", "Commune_Đường Hoa Phụng Châu",
    "Commune_Đại Kim", "Commune_Đại Mạch", "Commune_Đại Mỗ", "Commune_Đại Thành", "Commune_Đại Yên", "Commune_Đại Áng", "Commune_Đặng Xá", "Commune_Định Công",
    "Commune_Đống Mác", "Commune_Đồng Mai", "Commune_Đồng Nhân", "Commune_Đồng Phú", "Commune_Đồng Tháp", "Commune_Đồng Trúc", "Commune_Đồng Tâm", "Commune_Đồng Xuân",
    "Commune_Đội Cấn", "Commune_Đức Giang", "Commune_Đức Thượng", "Commune_Đức Thắng", "PostType_Nhà", "PostType_Đất", "District_Bắc Từ Liêm", "District_Chương Mỹ", "District_Cầu Giấy", "District_Gia Lâm", "District_Hai Bà Trưng",
    "District_Hoài Đức", "District_Hoàn Kiếm", "District_Hoàng Mai", "District_Hà Đông", "District_Long Biên",
    "District_Mê Linh", "District_Mỹ Đức", "District_Nam Từ Liêm", "District_Phú Xuyên", "District_Phúc Thọ", 
    "District_Quốc Oai", "District_Sóc Sơn", "District_Sơn Tây", "District_Thanh Oai", "District_Thanh Trì", 
    "District_Thanh Xuân", "District_Thường Tín", "District_Thạch Thất", "District_Tây Hồ", "District_Đan Phượng",
    "District_Đông Anh", "District_Đống Đa", "District_Ứng Hòa", "Direction_Bắc", "Direction_Nam", "Direction_Tây",
    "Direction_Tây - Bắc", "Direction_Tây - Nam", "Direction_Đông", "Direction_Đông - Bắc", "Direction_Đông - Nam",
    "Legal_Sổ đỏ/Sổ hồng", "Legal_Vi bằng", "Interior_Cơ bản", "Interior_Không có", "Interior_Đầy đủ"
]

print(len(columnsz))

X = pd.DataFrame(columns=columnsz)

# Prepare input data
new_data = {
    'Area': [150],
    'Bedrooms': [0],
    'Bathrooms': [0],
    'Commune': ['Hàng Bồ'],
    'PostType': ['Đất'],
    'District': ['Sóc Sơn'],
    'Direction': ['0'],
    'Legal': ['Hợp đồng mua bán'],
    'Interior': ['Không có'],
    'Width_meters': [5.48],
    'Floors': [0],
    'Entrancewidth': [0]
}

# Convert to DataFrame
new_df = pd.DataFrame(new_data)
categorical_columns = ['Commune', 'PostType', 'District', 'Direction', 'Legal', 'Interior']
# Mã hóa dữ liệu mới bằng cách sử dụng cùng một cột phân loại
new_df = pd.get_dummies(new_df, columns=categorical_columns, drop_first=False)

# Đảm bảo rằng tất cả các cột trong dữ liệu mới có mặt trong dữ liệu huấn luyện
missing_cols = set(X.columns) - set(new_df.columns)
missing_df = pd.DataFrame(0, index=new_df.index, columns=list(missing_cols))

# Kết hợp DataFrame hiện tại với các cột bị thiếu
df = pd.concat([new_df, missing_df], axis=1)

# Sắp xếp lại các cột theo thứ tự của X
new_df_final = df[X.columns]

print(new_df_final)
num_columns = new_df_final.columns.size  # hoặc len(new_df.columns)
print("Số lượng cột:", num_columns)

# Load model
# Tải mô hình đã huấn luyện
model_rf = joblib.load('model_randomforest.pkl')
model_gb = joblib.load('model_gradientboosting.pkl')
model_st = joblib.load('model_stacking.pkl')
# Dự đoán giá trị log
log_prediction_rf = model_rf.predict(new_df_final)
log_prediction_gb = model_gb.predict(new_df_final)
log_prediction_st = model_st.predict(new_df_final)

# Chuyển đổi từ log về giá trị gốc
original_prediction_rf = np.expm1(log_prediction_rf)
original_prediction_gb = np.expm1(log_prediction_gb)
original_prediction_st = np.expm1(log_prediction_st)
# In kết quả dự đoán gốc
print("Kết quả dự đoán - RF:", original_prediction_rf[0])
print("Kết quả dự đoán - GB:", original_prediction_gb[0])
print("Kết quả dự đoán - ST:", original_prediction_st[0])