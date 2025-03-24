import random
import numpy as np

# Danh sách khách mời và điểm thân thiết
khach_moi = ["Vợ", "Chồng", "ng yêu", "Anh", "Chị", "Em ruột", "Cha", "Mẹ", "Con cái", "Anh họ", "Chị họ", "Em họ","Gì", "Bác","Cháu","Bạn bè","Không quen biết"]
ma_tran_than_thiet = {
    ("Vợ", "Chồng", "ng yêu"): 2000, ("Anh", "Chị", "Em ruột"): 900, ("Cha", "Mẹ", "Con cái"): 700,
    ("Anh họ", "Chị họ", "Em họ"): 500, ("Gì", "Bác","Cháu"): 300, ("Bạn bè",): 100, ("Không quen biết",): 0,
}
'''2000 điểm: Vợ/chồng/người yêu.
 900 điểm: Anh/chị/em ruột.
 700 điểm: Cha/mẹ – con cái.
 500 điểm: Anh chị em họ.
 300 điểm: Dì/chú/bác – cháu.
 100 điểm: Bạn bè.
 0 điểm: Không quen biết'''
# Tham số GA
SO_LUONG_CA_THE = 100
TY_LE_DOT_BIEN = 0.1
SO_THE_HE = 500
SO_LUONG_BAN = len(khach_moi) // 7
SO_NGUOI_MOI_BAN = 6

def tinh_diem_than_thiet(so_do):
    """ Tính tổng điểm thân thiết cho sơ đồ chỗ ngồi."""
    diem = 0
    for ban in so_do:
        for i in range(len(ban)):
            for j in range(i + 1, len(ban)):
                for nhom, diem_nhom in ma_tran_than_thiet.items():
                    if ban[i] in nhom and ban[j] in nhom:
                        diem += diem_nhom
                        break  # Dừng kiểm tra sau khi tìm thấy nhóm phù hợp
    return diem
    

def tao_quan_the():
    """Sinh quần thể ban đầu với mỗi khách chỉ xuất hiện ở một bàn duy nhất."""
    quan_the = []
    for _ in range(SO_LUONG_CA_THE):
        khach_xao_tron = random.sample(khach_moi, len(khach_moi))  # Xáo trộn danh sách khách mời
        so_do = [khach_xao_tron[i:i + SO_NGUOI_MOI_BAN] for i in range(0, len(khach_xao_tron), SO_NGUOI_MOI_BAN)]
        quan_the.append(so_do)
    return quan_the


def lai_ghep(cha, me):
    """ Lai ghép hai bố mẹ để tạo con, đảm bảo không trùng lặp khách mời. """
    diem_cat = random.randint(1, SO_LUONG_BAN )
    con = cha[:diem_cat] + me[diem_cat:]
    
    # Đảm bảo không có khách nào xuất hiện hai lần
    khach_da_co = set()
    so_do_moi = []
    
    for ban in con:
        ban_moi = [khach for khach in ban if khach not in khach_da_co]
        khach_da_co.update(ban_moi)
        so_do_moi.append(ban_moi)
    
    # Thêm khách còn thiếu từ danh sách gốc
    khach_thieu = set(khach_moi) - khach_da_co
    for ban in so_do_moi:
        while len(ban) < SO_NGUOI_MOI_BAN and khach_thieu:
            ban.append(khach_thieu.pop())
    
    return so_do_moi

def dot_bien(so_do):
    """ Đột biến bằng cách hoán đổi ngẫu nhiên hai khách mời."""
    if random.random() < TY_LE_DOT_BIEN:
        ban1, ban2 = random.sample(range(len(so_do)), 2)
        if so_do[ban1] and so_do[ban2]:  # Kiểm tra bàn có khách không
            i, j = random.randint(0, len(so_do[ban1]) - 1), random.randint(0, len(so_do[ban2]) - 1)
            so_do[ban1][i], so_do[ban2][j] = so_do[ban2][j], so_do[ban1][i]
    return so_do


def giai_thuat_di_truyen():
    """ Giải thuật di truyền để tối ưu sơ đồ chỗ ngồi."""
    quan_the = tao_quan_the()
    for _ in range(SO_THE_HE):
        quan_the = sorted(quan_the, key=tinh_diem_than_thiet, reverse=True)  #tối ưu
        quan_the_moi = quan_the[:10]
        while len(quan_the_moi) < SO_LUONG_CA_THE:
            cha, me = random.choices(quan_the[:30], k=2)
            con = lai_ghep(cha, me)
            con = dot_bien(con)
            quan_the_moi.append(con)
        quan_the = quan_the_moi
    return sorted(quan_the, key=tinh_diem_than_thiet, reverse=True)[0]


def main():
    so_do_toi_uu = giai_thuat_di_truyen()
    print("Sơ đồ chỗ ngồi tối ưu:")

    for i, ban in enumerate(so_do_toi_uu):
        diem_ban = 0
        for j in range(len(ban)):
            for k in range(j + 1, len(ban)):
                for nhom, diem_nhom in ma_tran_than_thiet.items():
                    if ban[j] in nhom and ban[k] in nhom:
                        diem_ban += diem_nhom
                        break  # Tìm thấy nhóm phù hợp thì dừng

        print(f"Bàn {i+1} ({diem_ban} điểm): {' | '.join(ban)}")

    tong_diem = tinh_diem_than_thiet(so_do_toi_uu)
    print(f"\nTổng điểm của sơ đồ tối ưu: {tong_diem}")

if __name__ == "__main__":
    main()