import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import connectdb as cn
import program

# Hàm kiểm tra đăng nhập
def login():
    username = username_entry.get()
    password = password_entry.get()
    
    # Truy cập cơ sở dữ liệu
    con = cn.connectDB()
    cursor = con.cursor(dictionary=True)
    sql = "SELECT tt.HoTen, dn.Quyen, q.TenQuyen FROM dangnhap AS dn, thongtindangnhap AS tt, quyen as q WHERE dn.TenDN = %s AND dn.MatKhau = %s AND dn.TenDN = tt.TenDN AND dn.Quyen = q.Quyen"
    cursor.execute(sql, (username, password))
    result = cursor.fetchone()
    con.close()
    # cursor.close()

    if result is not None:
        result_label.config(text="Đăng nhập thành công!")
        username_entry.delete(0, tk.END)  # Xóa nội dung ô nhập liệu username
        password_entry.delete(0, tk.END)  # Xóa nội dung ô nhập liệu password
        
        login_frame.pack_forget()  # Ẩn giao diện đăng nhập

        if result['Quyen']==0:
            show_button_TCLS_Admin()
        else:
            show_button_NDSX_Baove()
        main_frame.pack()  # Hiển thị màn hình chính
        display_user_info(name=result['HoTen'], role=result['TenQuyen'])
        result_label.config(text="")
    else:
        result_label.config(text="Đăng nhập thất bại!")

# Hàm show các nút theo tài khoản đăng nhập
def show_button_TCLS_Admin():
    DSKH_button.pack()
    TCLS_button.pack()
    NDBS_button.pack_forget()

def show_button_NDSX_Baove():
    DSKH_button.pack_forget()
    TCLS_button.pack_forget()
    NDBS_button.pack()

# Hàm đăng xuất
def logout():
    main_frame.pack_forget()  # Ẩn màn hình chính
    login_frame.pack()  # Hiển thị giao diện đăng nhập

# Hiển thị frame Danh Sách Khách Hàng
def DanhSachKH():
    main_frame.pack_forget()
    dskh_frame.pack()
    for item in tree.get_children():
        tree.delete(item)

    con = cn.connectDB()
    cursor = con.cursor()
    cursor.execute("SELECT kh.ID_KhachHang, kh.HoTen, kh.DiaChi, kh.SDT, bsx.ID_BienSo FROM khachhang as kh, biensoxe as bsx WHERE kh.ID_KhachHang = bsx.ID_KhachHang")
    i = 0 
    for r in cursor:
        tree.insert('', i, text='', values=(r[0], r[1], r[2], r[3], r[4]))
        i += 1
    tree.pack()

# Hiển thị frame Tra cứu lịch sử
def TCLS():
    main_frame.pack_forget()
    TCLS_frame.pack()
    dsls_tree.pack()

# Hiện thị frame Nhận diện biển số
def NDBS():
    main_frame.pack_forget()
    NDSX_frame.pack()
    show_cam()

# Hàm xử lý nút Quay lại khi ở frame DSKH, TCLS
def comeback():
    dskh_frame.pack_forget()
    tree.pack_forget()
    TCLS_frame.pack_forget()
    dsls_tree.pack_forget()
    main_frame.pack()

# Hàm xử lý nút Quay lại khi ở frame NDBS
def cam_comback():
    NDSX_frame.pack_forget()
    cam.release()
    main_frame.pack()

# Hàm xử lý nút Quay lại khi ở frame DKKH
def register_comeback():
    DKKH_Frame.pack_forget()
    dskh_frame.pack()
    for item in tree.get_children():
        tree.delete(item)
    
    con = cn.connectDB()
    cursor = con.cursor()
    cursor.execute("SELECT kh.ID_KhachHang, kh.HoTen, kh.DiaChi, kh.SDT, bsx.ID_BienSo FROM khachhang as kh, biensoxe as bsx WHERE kh.ID_KhachHang = bsx.ID_KhachHang")
    i = 0 
    for r in cursor:
        tree.insert('', i, text='', values=(r[0], r[1], r[2], r[3], r[4]))
        i += 1

    register_id_entry.delete(0, tk.END)
    register_name_entry.delete(0, tk.END)
    register_address_entry.delete(0, tk.END)
    register_sdt_entry.delete(0, tk.END)
    register_idbs_entry.delete(0, tk.END)
    register_result_label.config(text="")

    tree.pack()

# Hiện Frame Đăng ký Khách hàng
def register_cus():
    dskh_frame.pack_forget()
    tree.pack_forget()
    DKKH_Frame.pack()

# Hàm xử lý nút đăng ký khách hàng trong frame DKKH
def RegisterAction():
    id = register_id_entry.get()
    name = register_name_entry.get()
    address = register_address_entry.get()
    phone = register_sdt_entry.get()
    bs = register_idbs_entry.get()

    con = cn.connectDB()
    cursor = con.cursor(dictionary=True)
    cursor2 = con.cursor(dictionary=True)
    cursor3 = con.cursor(dictionary=True)

    sql = "SELECT * FROM khachhang kh WHERE kh.ID_KhachHang = %s"
    insert_kh = "INSERT INTO khachhang(ID_KhachHang, Hoten, DiaChi, SDT) VALUES(%s,%s,%s,%s)"
    insert_bs = "INSERT INTO biensoxe(ID_BienSo,ID_KhachHang) VALUES(%s,%s)"

    cursor.execute(sql, (id,))
    result = cursor.fetchone()
    # con.close()

    if result is not None:
        register_result_label.config(text="Mã KH đã tồn tại!")
    else:
        cursor2.execute(insert_kh, (id, name, address, phone))
        cursor3.execute(insert_bs, (bs, id))
        con.commit()
        # DanhSachKH()
        register_result_label.config(text="Đăng kí thành công!")

# Hàm xử lý nút xóa khách hàng trong frame DSKH
def Delete_Cus():
    id = delete_cus_entry.get()

    con = cn.connectDB()
    delete_cursor = con.cursor(dictionary=True)
    delete_cursor2 = con.cursor(dictionary=True)
    delete_cursor3 = con.cursor(dictionary=True)

    sql_check = "SELECT * FROM khachhang kh WHERE kh.ID_KhachHang = %s"
    sql_kh = "DELETE FROM khachhang WHERE ID_KhachHang = %s"
    sql_bs = "DELETE FROM biensoxe WHERE ID_KhachHang = %s"
    delete_cursor.execute(sql_check, (id,))

    result = delete_cursor.fetchone()
    if result is None:
        # Kiểm tra xem label đã được tạo chưa
        if not hasattr(Delete_Cus, "delete_label"):
            # Nếu chưa, tạo mới label
            Delete_Cus.delete_label = tk.Label(dskh_frame, text='Mã KH không tồn tại')
            Delete_Cus.delete_label.pack()
        else:
            # Nếu đã tồn tại, cập nhật nội dung của label
            Delete_Cus.delete_label.config(text='Mã KH không tồn tại')
    else:
        # Nếu label đã tồn tại, hủy nó
        if hasattr(Delete_Cus, "delete_label"):
            Delete_Cus.delete_label.destroy()

        delete_cursor3.execute(sql_bs,(id,))
        delete_cursor2.execute(sql_kh, (id,))
        con.commit()

        for item in tree.get_children():
            tree.delete(item)

        con = cn.connectDB()
        cursor = con.cursor()
        cursor.execute("SELECT kh.ID_KhachHang, kh.HoTen, kh.DiaChi, kh.SDT, bsx.ID_BienSo FROM khachhang as kh, biensoxe as bsx WHERE kh.ID_KhachHang = bsx.ID_KhachHang")
        i = 0 
        for r in cursor:
            tree.insert('', i, text='', values=(r[0], r[1], r[2], r[3], r[4]))
            i += 1
        tree.pack()

        # Kiểm tra xem label đã được tạo chưa
        if not hasattr(Delete_Cus, "delete_label"):
            # Nếu chưa, tạo mới label
            Delete_Cus.delete_label = tk.Label(dskh_frame, text='Xóa Thành Công')
            Delete_Cus.delete_label.pack()
        else:
            # Nếu đã tồn tại, cập nhật nội dung của label
            Delete_Cus.delete_label.config(text='Xóa Thành Công')

# Hàm xử lý nút quét cam nhận biển số trong frame NDBS
def CamCheck():
    cv2.imwrite('images/numberplate.jpg',gray)
    bs = program.readnumberplate()
    if bs == '':
        bs = 'Không xác định'

    else:
        con = cn.connectDB()
        cursor = con.cursor(dictionary=True)

        sql = "SELECT ls.TrangThai FROM lichsu AS ls WHERE ls.ID_BienSo = %s"
        cursor.execute(sql, (bs,))
        result = cursor.fetchone()
        # print(result)

    # Kiểm tra xem label đã được tạo chưa
    if not hasattr(CamCheck, "ndbs_label"):
        # Nếu chưa, tạo mới label
        CamCheck.ndbs_label = tk.Label(NDSX_frame, text=bs,font=10, width=20)
        CamCheck.ndbs_label.pack()
    else:
        # Nếu đã tồn tại, cập nhật nội dung của label
        CamCheck.ndbs_label.config(text=bs)

# Hàm xử lý nút tìm kiếm trong frame TCLS
def SearchBSX():
    id = dsls_search_entry.get()

    con = cn.connectDB()
    search_cursor = con.cursor(dictionary=True)

    sql_search = "SELECT * FROM lichsu WHERE ID_BienSo = %s"
    search_cursor.execute(sql_search, (id,))
    result_search = search_cursor.fetchone()

    if result_search is None:
        for item in dsls_tree.get_children():
            dsls_tree.delete(item)
    else:
        for item in dsls_tree.get_children():
            dsls_tree.delete(item)
    
        search_cursor2 = con.cursor()
        search_cursor2.execute("SELECT * FROM lichsu WHERE ID_BienSo = %s", (id,))
        i = 0 
        for r in search_cursor2:
            dsls_tree.insert('', i, text='', values=(r[1], r[2], r[3], r[4]))
            i += 1
        dsls_tree.pack()

# Hàm xử lý nút làm mới trong frame TCLS
def SearchFrefresh():
    for item in dsls_tree.get_children():
        dsls_tree.delete(item)
    
    cursor = con.cursor()
    cursor.execute("SELECT * FROM lichsu")
    i = 0 
    for r in cursor:
        dsls_tree.insert('', i, text='', values=(r[1], r[2], r[3], r[4]))
        i += 1
    dsls_tree.pack()

# Hàm xử lý hiện cam khi vào frame NDBS
def show_cam():
   ret, NDSX_frame = cam.read()
   if ret:
        NDSX_frame = cv2.resize(NDSX_frame, (400, 400)) # resize the frame to 200x200
        img = cv2.cvtColor(NDSX_frame, cv2.COLOR_BGR2RGB)
        n_plate_detector = cv2.CascadeClassifier("haarcascade_license_plate_rus_16stages.xml")
        detections = n_plate_detector.detectMultiScale(img, scaleFactor=1.05, minNeighbors=3)
        for (x, y, w, h) in detections:
        # vẽ hình chữ nhật xung quanh vùng biển số xe 
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255),2)
            # in chữ cạnh vùng biển số xe
            cv2.putText(img, "Bien so xe", (x - 20, y - 10),
            cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 255), 2)
            
            # tạo một khung chỉ chứa hình ảnh của biển số xe nhận diện được
            number_plate = img[y:y + h, x:x + w]
            # điểu chỉnh màu của khung trên thành tối
            global gray
            gray = cv2.cvtColor(number_plate,cv2.COLOR_BGR2GRAY)
            cv2.imshow("Bien so xe", gray)
            # cv2.imwrite('images/numberplate.jpg',gray)

        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        label_cam.imgtk = imgtk
        label_cam.configure(image=imgtk)
   window.after(10, show_cam)

# Hàm hiện thị tên và quyền tk đăng nhập
def display_user_info(name, role):
    # Hiển thị thông tin người dùng trong giao diện chính
    user_info_label.config(text=f"Tên: {name}")
    role_info_label.config(text=f"Quyền: {role}")

# Hàm show ảnh đại diện app
def show_avatar(image_path):
    image = Image.open(image_path)
    image = image.resize((300, 300), Image.ANTIALIAS)
    tk_image = ImageTk.PhotoImage(image)
    avatar_label.config(image=tk_image)
    avatar_label.image = tk_image
# Tạo cửa sổ
window = tk.Tk()
window.title("Ứng dụng")
window.geometry("700x600")

# Tạo frame cho giao diện đăng nhập
login_frame = tk.Frame(window)
login_label = tk.Label(login_frame, text="ĐĂNG NHẬP", font=40).pack(side=tk.TOP, pady=30)

username_label = tk.Label(login_frame, text="Tên đăng nhập:", width=30, font=14)
username_label.pack()
username_entry = tk.Entry(login_frame, width=30, font=14)
username_entry.pack()

password_label = tk.Label(login_frame, text="Mật khẩu:", width=30, font=14)
password_label.pack()
password_entry = tk.Entry(login_frame, show="*", width=30, font=14)
password_entry.pack()

login_button = tk.Button(login_frame, text="Đăng nhập", width=30, font=14, command=login).pack(pady=30)

result_label = tk.Label(login_frame)
result_label.pack()


# TẠO GIAO DIỆN MÀN HÌNH CHÍNH
main_frame = tk.Frame(window)

welcome_label = tk.Label(main_frame, text="HỆ THÔNG GIỮ XE THÔNG MINH",font=20).pack(side=tk.TOP, pady=10)

# hiện thị ảnh đại diện
avatar_label = tk.Label(main_frame, bg="lightgray")
avatar_label.pack()

# Gọi hàm để hiển thị ảnh đại diện
image_path = ".\\AnhDangNhap\\AnhDaiDien.png"
show_avatar(image_path)

user_info_label = tk.Label(main_frame, text="",font=14)
user_info_label.pack()
role_info_label = tk.Label(main_frame, text="",font=14)
role_info_label.pack()

logout_button = tk.Button(main_frame, text="Đăng xuất", width=30, command=logout).pack()

DSKH_button = tk.Button(main_frame, text="Danh sách khách hàng", width=30, command=DanhSachKH)

TCLS_button = tk.Button(main_frame, text="Tra cứu lịch sử", width=30, command=TCLS)

NDBS_button = tk.Button(main_frame, text="Nhận diện biển số", width=30, command=NDBS)

# TẠO GIAO DIỆN TRA LỊCH SỬ XE RA VÀO
TCLS_frame = tk.Frame(window)
# welcome_label = tk.Label(TCLS_frame, text="LỊCH SỬ BÃI GIỮ XE").pack()

dsld_frame_title = tk.Label(TCLS_frame, text="Lịch Sử Xe Ra Vào", font=14).pack()
dsls_con = cn.connectDB()
dsls_cursor = dsls_con.cursor()

dsls_cursor.execute("SELECT * FROM lichsu")

dsls_tree = ttk.Treeview(window)
dsls_tree['show'] = 'headings'

s = ttk.Style(window)
s.theme_use('clam')

dsls_tree['columns'] = ('BienSo', 'TrangThai', 'NgayVao', 'NgayRa')

# Cấu hình kích thước cho từng cột
dsls_tree.column('BienSo', width=100, minwidth=100, anchor=tk.W)
dsls_tree.column('TrangThai', width=100, minwidth=100, anchor=tk.W)
dsls_tree.column('NgayVao', width=200, minwidth=200, anchor=tk.W)
dsls_tree.column('NgayRa', width=200, minwidth=200, anchor=tk.W)

# Đặt tên cho từng cột
dsls_tree.heading('BienSo', text='Biển Số Xe', anchor=tk.CENTER)
dsls_tree.heading('TrangThai', text='Trạng Thái', anchor=tk.CENTER)
dsls_tree.heading('NgayVao', text='Ngày Vào', anchor=tk.CENTER)
dsls_tree.heading('NgayRa', text='Ngày Ra', anchor=tk.CENTER)

# Load dữ liệu từ csdl vào các cột
i = 0 
for r in dsls_cursor:
    dsls_tree.insert('', i, text='', values=(r[1], r[2], r[3], r[4]))
    i += 1

dsls_comeback_button = tk.Button(TCLS_frame, text="Quay lại", command=comeback).pack()
dsls_search_button = tk.Button(TCLS_frame, text='Tìm Kiếm', command=SearchBSX).pack(side=tk.LEFT)
dsls_search_entry = tk.Entry(TCLS_frame)
dsls_search_entry.pack(side=tk.LEFT)
dsls_refresh_button = tk.Button(TCLS_frame, text='Làm mới', command=SearchFrefresh).pack()



# TẠO GIAO DIỆN NHẬN DIỆN BIỂN SỐ
NDSX_frame = tk.Frame(window)
welcome_label = tk.Label(NDSX_frame, text="NHẬN DIỆN BIỂN SỐ").pack()

label_cam = tk.Label(NDSX_frame, width=400, height=400)
label_cam.pack(side=tk.TOP)

come_back_button = tk.Button(NDSX_frame, text="Quay lại", width=20, font=10, command=cam_comback).pack()

cam_check_button = tk.Button(NDSX_frame, text='Quét', width=20, font=10, command=CamCheck).pack()

cam = cv2.VideoCapture(0)

# TẠO GIAO DIỆN HIỂN THỊ DANH SÁCH KHÁCH HÀNG
dskh_frame = tk.Frame(window)

frame_title = tk.Label(dskh_frame, text="Danh Sách Khách Hàng", font=14).pack()
con = cn.connectDB()
cursor = con.cursor()

cursor.execute("SELECT kh.ID_KhachHang, kh.HoTen, kh.DiaChi, kh.SDT, bsx.ID_BienSo FROM khachhang as kh, biensoxe as bsx WHERE kh.ID_KhachHang = bsx.ID_KhachHang")

tree = ttk.Treeview(window)
tree['show'] = 'headings'

s = ttk.Style(window)
s.theme_use('clam')

tree['columns'] = ('MaKH', 'HoTen', 'DiaChi', 'SDT', 'BienSo')

# Cấu hình kích thước cho từng cột
tree.column('MaKH', width=120, minwidth=120, anchor=tk.W)
tree.column('HoTen', width=120, minwidth=120, anchor=tk.W)
tree.column('DiaChi', width=120, minwidth=120, anchor=tk.W)
tree.column('SDT', width=120, minwidth=120, anchor=tk.W)
tree.column('BienSo', width=120, minwidth=120, anchor=tk.W)

# Đặt tên cho từng cột
tree.heading('MaKH', text='Mã KH', anchor=tk.CENTER)
tree.heading('HoTen', text='Họ Tên', anchor=tk.CENTER)
tree.heading('DiaChi', text='Địa Chỉ', anchor=tk.CENTER)
tree.heading('SDT', text='SDT', anchor=tk.CENTER)
tree.heading('BienSo', text='Biển Số', anchor=tk.CENTER)

# Load dữ liệu từ csdl vào các cột
i = 0 
for r in cursor:
    tree.insert('', i, text='', values=(r[0], r[1], r[2], r[3], r[4]))
    i += 1
come_back_button = tk.Button(dskh_frame, text="Quay lại", command=comeback).pack()
register_button = tk.Button(dskh_frame, text='Đăng Kí Khách Hàng', command=register_cus).pack()

delete_cus_button = tk.Button(dskh_frame, text='Xóa', command=Delete_Cus).pack(side=tk.LEFT)
delete_cus_entry = tk.Entry(dskh_frame)
delete_cus_entry.pack(side=tk.LEFT)


# TẠO GIAO DIỆN ĐĂNG KÍ KHÁCH HÀNG
DKKH_Frame = tk.Frame(window)

register_id_label = tk.Label(DKKH_Frame, text="Mã Khách Hàng:", width=15, font=14).pack()
register_id_entry = tk.Entry(DKKH_Frame, width=15, font=14)
register_id_entry.pack(expand=True, fill=tk.BOTH)

register_name_label = tk.Label(DKKH_Frame, text="Họ Tên:", width=30, font=14).pack()
register_name_entry = tk.Entry(DKKH_Frame, width=30, font=14)
register_name_entry.pack()

register_address_label = tk.Label(DKKH_Frame, text="Địa Chỉ:", width=30, font=14).pack()
register_address_entry = tk.Entry(DKKH_Frame, width=30, font=14)
register_address_entry.pack()

register_sdt_label = tk.Label(DKKH_Frame, text="Số Điện Thoại:", width=30, font=14).pack()
register_sdt_entry = tk.Entry(DKKH_Frame, width=30, font=14)
register_sdt_entry.pack()

register_idbs_label = tk.Label(DKKH_Frame, text="Biển Số Xe:", width=30, font=14).pack()
register_idbs_entry = tk.Entry(DKKH_Frame, width=30, font=14)
register_idbs_entry.pack()

register_action_button = tk.Button(DKKH_Frame, text='Đăng Kí', command=RegisterAction).pack()

register_result_label = tk.Label(DKKH_Frame)
register_result_label.pack()

register_comeback_button = tk.Button(DKKH_Frame, text="Quay lại", command=register_comeback).pack()

# come_back_button = tk.Button(dskh_frame, text="Quay lại", command=comeback).pack()

# Hiển thị giao diện đăng nhập ban đầu
# main_frame.pack()
login_frame.pack()
# DKKH_Frame.pack()
# TCLS_frame.pack()
# dsls_tree.pack()

# Chạy chương trình
window.mainloop()