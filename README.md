# Password-Manager
## 7. Xây dựng hệ thống quản lý mật khẩu (Password Manager) cá nhân:
Lưu trữ mật khẩu mã hóa, tích hợp tính năng tạo mật khẩu mạnh và 
chống keylogger.
# Các thành viên
Nguyễn Lâm Khoi | 
Phạm Phước | 
Nguyễn Anh Khoa | 


# TINH NANG - Password Manager (Chu de 7 ATTT)

> Mon: An toan Thong tin - HK2 2025-2026
> Chu de 7: Xay dung he thong quan ly mat khau ca nhan
> Ngon ngu: Python 3  |  Thu vien: cryptography, pyperclip, tkinter

==========================================================================
## 1. MA HOA AES-256-GCM
==========================================================================

File: crypto.py

Toan bo du lieu mat khau duoc ma hoa bang AES-256-GCM truoc khi luu xuong dia.

  Thuat toan    : AES-256-GCM (Advanced Encryption Standard)
  Kich thuoc khoa: 256 bit (32 bytes) - muc bao mat toi da cua AES
  Nonce         : 96 bit (12 bytes) - so ngau nhien 1 lan, dam bao ciphertext khac nhau moi lan
  GCM Tag       : 128 bit - xac thuc toan ven, phat hien file bi sua doi

Vi sao chon AES-GCM?
  - Tinh bao mat (Confidentiality): Du lieu ma hoa hoan toan
  - Tinh toan ven (Integrity): GCM tag phat hien neu ai sua file vault
  - Tinh xac thuc (Authenticity): Chi ai biet dung Master Password moi decrypt duoc

==========================================================================
## 2. DAN XUAT KHOA - PBKDF2-HMAC-SHA256
==========================================================================

File: crypto.py - ham derive_key()

Master Password KHONG luu truc tiep ma qua ham dan xuat khoa:

  Master Password + Salt (128-bit ngau nhien)
       --> PBKDF2-HMAC-SHA256 (600,000 vong lap)
       --> Khoa AES-256 (256-bit)

  Iterations : 600,000  (NIST SP 800-132 nam 2023 khuyen nghi)
  Salt       : 128-bit ngau nhien moi lan encrypt --> Chong Rainbow Table Attack
  Output     : 256-bit key dung cho AES-256

Tai sao can 600,000 vong lap?
  Moi lan thu mat khau mat ~0.5 giay --> brute-force 1 ty mat khau ton ~15 nam

==========================================================================
## 3. CHONG KEYLOGGER - BAN PHIM AO (Virtual Keyboard)
==========================================================================

File: ui/login.py

Keylogger la phan mem doc hai theo doi tung phim bam tren ban phim vat ly.

Giai phap da trien khai:
  [1] Ban phim ao tren man hinh: nguoi dung CLICK CHUOT thay vi go ban phim
      --> Keylogger khong the ghi lai thao tac chuot --> mat khau duoc bao ve

  [2] Nut "Xao tron ban phim": doi vi tri ngau nhien cac phim moi lan nhan
      --> Chong Screen Recorder (ke tan cong ghi man hinh xem vi tri ban click)

Co che hoat dong:
  Click vao phim ao --> luu vao bien noi bo --> khong di qua OS keyboard hook

Ban phim vat ly van cho phep dung (tien loi) nhung ban phim ao an toan hon.

==========================================================================
## 4. GIOI HAN DANG NHAP - CHONG BRUTE-FORCE
==========================================================================

File: ui/login.py

  - Toi da 5 lan nhap sai Master Password
  - Lan thu 5 sai --> App bi KHOA hoan toan den khi khoi dong lai
  - Hien thi dem nguoc so lan con lai
  - Ngan chan tan cong brute-force truc tiep vao ung dung

==========================================================================
## 5. TAO MAT KHAU MANH - DUNG secrets MODULE (CSPRNG)
==========================================================================

File: crypto.py - ham generate_password()
UI  : ui/generator.py

Tinh nang:
  - Tuy chon bo ky tu: Chu hoa (A-Z) | Chu thuong (a-z) | So (0-9) | Ky tu dac biet (!@#$%^&*)
  - Do dai tuy chinh: 8 - 64 ky tu
  - Dam bao co it nhat 1 ky tu tu moi nhom duoc chon
  - Xao tron vi tri ngau nhien (chong pattern)

So sanh random vs secrets:

  random module (cu, KHONG an toan):
    - Pseudo-Random Number Generator (PRNG)
    - Dung seed co dinh --> co the predict neu biet output
    - KHONG nen dung cho bao mat

  secrets module (moi, AN TOAN):
    - Cryptographically Secure PRNG (CSPRNG)
    - Lay tu OS entropy nguon (/dev/urandom tren Linux, CryptGenRandom tren Windows)
    - KHONG the predict --> Dung chuan cho bao mat

==========================================================================
## 6. DANH GIA DO MANH MAT KHAU
==========================================================================

File: crypto.py - ham check_password_strength()
UI  : dashboard.py, generator.py

Thanh mau hien thi do manh realtime khi go mat khau:

  0-25 diem  : Rat yeu  (Do)
  26-50 diem : Yeu      (Cam)
  51-70 diem : Trung binh (Vang)
  71-85 diem : Manh     (Xanh la)
  86-100 diem: Rat manh (Xanh dam)

Tieu chi danh gia:
  + Do dai >= 8 ky tu  (+10 diem)
  + Do dai >= 12 ky tu (+10 diem)
  + Do dai >= 16 ky tu (+10 diem)
  + Co chu hoa         (+20 diem)
  + Co chu thuong      (+20 diem)
  + Co so              (+15 diem)
  + Co ky tu dac biet  (+15 diem)

==========================================================================
## 7. TIM KIEM TAI KHOAN REALTIME
==========================================================================

File: ui/dashboard.py

  - Go vao o tim kiem --> danh sach loc ngay lap tuc (khong can nhan Enter)
  - Tim theo ten Site HOAC Username
  - Hien thi "Tim thay X / Y tai khoan"
  - Nut X xoa nhanh tu khoa tim kiem

==========================================================================
## 8. AN/HIEN MAT KHAU (Show/Hide Password)
==========================================================================

File: ui/dashboard.py

  - Nut mat meo (eye icon) ben canh o mat khau de toggle show/hide
  - Mac dinh hien thi dau (an)
  - Click --> hien mat khau ro, icon doi thanh mat nheo
  - Bao ve khoi "shoulder surfing" (nguoi ngoi canh nhin trom)

==========================================================================
## 9. TRUONG GHI CHU (Notes Field)
==========================================================================

File: ui/dashboard.py | vault.py (cau truc du lieu)

Moi tai khoan co them truong ghi chu tu do de luu:
  - Email khoi phuc
  - Cau hoi bao mat
  - URL dang nhap dac biet
  - Thong tin them khac

Ghi chu duoc ma hoa cung voi mat khau trong vault.

==========================================================================
## 10. LUU TRU AN TOAN - VAULT MA HOA
==========================================================================

File: vault.py

  - Toan bo vault luu trong 1 file vault.json (noi dung la binary ma hoa)
  - Format nhi phan: [Salt 16B] + [Nonce 12B] + [Ciphertext + GCM Tag]
  - Khong co Master Password dung --> khong doc duoc gi
  - Dung absolute path --> khong bi loi khi chay tu thu muc khac

==========================================================================
## HUONG DAN CHAY UNG DUNG
==========================================================================

Buoc 1 - Cai thu vien (chi can lam 1 lan):
  pip install cryptography pyperclip

Buoc 2 - Chay ung dung:
  cd "d:\An_toan_thong_tin\github\passwordManager\passwordManager"
  python main.py

Lan dau dung: Nhap bat ky mat khau nao lam Master Password
              He thong tu tao vault rong va vao thang Dashboard

QUAN TRONG: Khong co tinh nang reset Master Password.
            Quen mat khau = mat toan bo du lieu trong vault!

==========================================================================
## CAU TRUC PROJECT
==========================================================================

  passwordManager/
  |-- main.py              # Diem khoi chay ung dung
  |-- crypto.py            # Ma hoa AES-256-GCM, PBKDF2, generate_password
  |-- vault.py             # Luu/tai vault ma hoa
  |-- requirements.txt     # Thu vien can cai: cryptography, pyperclip
  |-- vault.json           # Vault ma hoa (tu tao khi chay lan dau)
  |-- Tinh_nang.md         # File nay - tai lieu tinh nang
  |-- ui/
      |-- __init__.py
      |-- login.py         # Man hinh dang nhap + ban phim ao
      |-- dashboard.py     # Man hinh chinh quan ly tai khoan
      |-- generator.py     # Cua so tao mat khau manh

==========================================================================
## TAI LIEU THAM KHAO
==========================================================================

  - NIST SP 800-132 (2023): Recommendation for Password-Based Key Derivation
  - NIST FIPS 197: Advanced Encryption Standard (AES)
  - Python secrets module: https://docs.python.org/3/library/secrets.html
  - RFC 5288: AES Galois Counter Mode (GCM) Cipher Suites for TLS
  - OWASP Password Storage Cheat Sheet
