import cv2 
from pytesseract import pytesseract
from PIL import Image
import mysql.connector
import datetime
import connectdb as cn

# Check tên biển số đọc từ hình ảnh lưu vào thư mục "images" đã tồn tại trong database chưa 
def checkNp(number_plate):
    print(number_plate)
    con = cn.connectDB()
    cursor = con.cursor()
    sql = "SELECT * FROM lichsu WHERE ID_BienSo = %s"
    cursor.execute(sql,(number_plate,))

    result = cursor.fetchone()
    # con.close()
    # cursor.close()
    return result

# Check tên biển số và trạng thái của bản ghi gần nhất đọc từ hình ảnh lưu vào thư mục "images" 
def checkExist(number_plate):
    con = cn.connectDB()
    cursor = con.cursor()
    sql = "SELECT * FROM biensoxe WHERE ID_BienSo = %s ORDER BY NgayVao DESC LIMIT 1"
    cursor.execute(sql,(number_plate,))
    cursor.fetchall()
    result = cursor._rowcount
    con.close()
    cursor.close()
    return result

def checkNpStatus(number_plate):
    con = cn.connectDB()
    cursor = con.cursor()
    sql = "SELECT * FROM lichsu WHERE ID_BienSo = %s ORDER BY NgayVao DESC LIMIT 1"
    cursor.execute(sql,(number_plate,))
    result = cursor.fetchone()
    # print("Ngay vao  : " + str(result[2]) + datetime.datetime.strftime(result[3],"%Y/%m/%d %H:%M:%S"))
    con.close()
    cursor.close()
    return result
# Tạo bản ghi dành cho xe vào bãi gửi xe (Cho xe vào bãi)

def insertNp(number_plate):
    print(number_plate)
    con = cn.connectDB()
    cursor = con.cursor()
    sql = "INSERT INTO lichsu(ID_BienSo,TrangThai,NgayVao) VALUES(%s,%s,%s)"
    now = datetime.datetime.now()
    date_in = now.strftime("%Y/%m/%d %H:%M:%S")
    cursor.execute(sql,(number_plate,'1',date_in))
    con.commit()
    cursor.close()
    con.close()
    print("VAO BAI GUI XE")
    print("Ngay gio vao : " + datetime.datetime.strftime(datetime.datetime.now(),"%Y/%m/%d %H:%M:%S"))

# Cập nhật bản ghi (Cho xe ra khỏi bãi)
def updateNp(Id):
    con = cn.connectDB()
    cursor = con.cursor()
    sql = "UPDATE lichsu SET TrangThai = 0, NgayRa = %s WHERE Id = %s"
    now = datetime.datetime.now()
    date_out = now.strftime("%Y/%m/%d %H:%M:%S")
    cursor.execute(sql,(date_out,Id))
    con.commit()
    cursor.close()
    con.close()
    print("RA KHOI BAI GUI XE")
    print("Ngay gio ra : " + datetime.datetime.strftime(datetime.datetime.now(),"%Y/%m/%d %H:%M:%S"))

# Đọc biển số xe từ ảnh đã lưu vào thư mục "images"
def readnumberplate():
    path_to_tesseract = r"E:\Study\HK7\XD_HTTT\Final\Tessercact-OCR\tesseract.exe"
    pytesseract.tesseract_cmd = path_to_tesseract
    image = Image.open(r"E:\Study\HK7\XD_HTTT\Final\images\numberplate.jpg")

    # tạo biến text hứng string nhận được từ hình ảnh
    text = pytesseract.image_to_string(image,lang="eng")
    number_plate = ''
    for char in str(text):
        # loại bỏ khoảng trắng
        if (char.isspace() == False):
            number_plate += char
    print("----------------------------------")
    print("Xe co bien so : " + number_plate)
    print("----------------------------------")
    if number_plate != "":
        #Gọi hàm kiểm tra xem biển số này đã tồn tại trong daatabase chưa
        check = checkNp(number_plate)
        # Nếu "check" = 0 (Xe chưa từng đến gửi tại bãi)
        if check is None:
            # Gọi hàm "insertNp" để cho xe vào gửi
            insertNp(number_plate)
        # Nếu "check" != 0 (Xe đã từng đến gửi tại bãi)
        else:
            # Gọi hàm kiểm tra trạng thái của xe
            check2 = checkNpStatus(number_plate)
            # Nếu trạng thái của xe bằng 1 (xe vào gửi và chưa lấy ra)
            if check2[2] == 1:
                # Gọi hàm "updateNp" lấy xe ra và cập nhật trạng thái cho xe này về 0 (đã lấy ra)
                updateNp(check2[0])
            # Nếu trạng thái của xe bằng 0 (xe vào gửi và lấy ra rồi) 
            else:
                # Gọi hàm "insertNp" để cho xe vào gửi
                insertNp(number_plate)
    else:
        print("Bien so khong xac dinh !")

    return number_plate




