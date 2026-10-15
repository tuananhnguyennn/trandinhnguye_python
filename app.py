import pandas as pd
import streamlit as st

# --- 1. Tiêu đề ứng dụng ---
st.title("QUẢN LÝ LƯƠNG NHÂN VIÊN")
st.markdown("---")

# --- 2. Dữ liệu mẫu (10 nhân viên) ---
# Quy tắc tính tổng lương: Lương cơ bản * Hệ số + Phụ cấp
data = {
    "Họ tên": [
        "Phan Nhật Nam", 
        "Đặng Thu Thảo", 
        "Võ Minh Trí", 
        "Lâm Ngọc Hân",
        "Hồ Tuấn Kiệt", 
        "Trần Mai Anh", 
        "Nguyễn Hải Đăng", 
        "Đinh Tố Như",
        "Tô Quang Minh", 
        "Lê Phương Trinh"
    ],
    "Lương cơ bản (Triệu VNĐ)": [8.0, 10.0, 7.5, 6.0, 12.0, 8.5, 11.0, 5.0, 7.0, 9.0],
    "Hệ số": [1.2, 1.5, 1.0, 1.0, 2.0, 1.2, 1.8, 1.0, 1.0, 1.5],
    "Phụ cấp (Triệu VNĐ)": [1.0, 1.5, 0.5, 0.5, 2.0, 1.0, 1.5, 0.0, 0.5, 1.0]
}

df = pd.DataFrame(data)

# Tính Tổng lương
df["Tổng lương (Triệu VNĐ)"] = (
    df["Lương cơ bản (Triệu VNĐ)"] * df["Hệ số"] + df["Phụ cấp (Triệu VNĐ)"]
).round(2)

# Phân loại mức thu nhập
def phan_loai_thu_nhap(luong):
    if luong >= 20.0:
        return "Mức Cao"
    elif luong >= 10.0:
        return "Mức Khá"
    else:
        return "Mức Trung bình"

df["Mức thu nhập"] = df["Tổng lương (Triệu VNĐ)"].apply(phan_loai_thu_nhap)

# --- 3. Hiển thị bảng lương ---
st.subheader("📋 Bảng lương chi tiết tháng này")
st.dataframe(df, use_container_width=True)

# --- 4. Các thống kê tổng quan ---
st.markdown("---")
st.subheader("📊 Thống kê quỹ lương")

col1, col2, col3 = st.columns(3)

# Tính toán các chỉ số
tong_quy_luong = df["Tổng lương (Triệu VNĐ)"].sum().round(2)
luong_trung_binh = df["Tổng lương (Triệu VNĐ)"].mean().round(2)
nv_max = df.loc[df["Tổng lương (Triệu VNĐ)"].idxmax()]
nv_min = df.loc[df["Tổng lương (Triệu VNĐ)"].idxmin()]

col1.metric("Tổng quỹ lương", f"{tong_quy_luong} Tr")
col2.metric("Lương trung bình", f"{luong_trung_binh} Tr")
col3.metric(
    "Lương cao nhất",
    f"{nv_max['Họ tên']}",
    f"{nv_max['Tổng lương (Triệu VNĐ)']} Tr"
)

st.info(
    f"🔻 **Nhân viên có mức lương thấp nhất:** {nv_min['Họ tên']} ({nv_min['Tổng lương (Triệu VNĐ)']} Tr)"
)

# --- 5. Tra cứu lương từng nhân viên (Selectbox) ---
st.markdown("---")
st.subheader("🔍 Tra cứu thông tin nhân viên")

selected_employee = st.selectbox(
    "Chọn tên nhân viên để xem chi tiết:", df["Họ tên"].tolist()
)

# Lọc dữ liệu nhân viên được chọn
emp_info = df[df["Họ tên"] == selected_employee].iloc[0]

# Hiển thị thông tin
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Lương cơ bản", f"{emp_info['Lương cơ bản (Triệu VNĐ)']} Tr")
c2.metric("Hệ số", emp