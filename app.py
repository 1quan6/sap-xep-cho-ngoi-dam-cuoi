from flask import Flask, render_template
import random

app = Flask(__name__)

# Danh sách khách mời và điểm thân thiết
khach_moi = ["Vợ", "Chồng", "ng yêu", "Anh", "Chị", "Em ruột", "Cha", "Mẹ", "Con cái", 
             "Anh họ", "Chị họ", "Em họ", "Gì", "Bác", "Cháu", "Bạn bè", "Không quen biết"]
ma_tran_than_thiet = {
    ("Vợ", "Chồng", "ng yêu"): 2000, ("Anh", "Chị", "Em ruột"): 900, ("Cha", "Mẹ", "Con cái"): 700,
    ("Anh họ", "Chị họ", "Em họ"): 500, ("Gì", "Bác", "Cháu"): 300, ("Bạn bè",): 100, ("Không quen biết",): 0,
}

# Tham số GA
SO_NGUOI_MOI_BAN = 6
SO_LUONG_BAN = len(khach_moi) // SO_NGUOI_MOI_BAN

def tinh_diem_than_thiet(so_do):
    """ Tính tổng điểm thân thiết cho sơ đồ chỗ ngồi."""
    diem = 0
    for ban in so_do:
        for i in range(len(ban)):
            for j in range(i + 1, len(ban)):
                for nhom, diem_nhom in ma_tran_than_thiet.items():
                    if ban[i] in nhom and ban[j] in nhom:
                        diem += diem_nhom
                        break
    return diem

def tao_so_do():
    """Sinh sơ đồ ngẫu nhiên."""
    khach_xao_tron = random.sample(khach_moi, len(khach_moi))
    so_do = [khach_xao_tron[i:i + SO_NGUOI_MOI_BAN] for i in range(0, len(khach_xao_tron), SO_NGUOI_MOI_BAN)]
    return so_do

@app.route("/")
def index():
    so_do = tao_so_do()
    tong_diem = tinh_diem_than_thiet(so_do)
    return render_template("index.html", khach_moi=khach_moi, so_do=so_do, tong_diem=tong_diem)


if __name__ == "__main__":
    app.run(debug=True)
