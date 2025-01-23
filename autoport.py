import os
import subprocess
import time
from datetime import datetime
import json
import threading

def log_event(event):
    """Loglama sistemi icin JSON formatinda bir kayit olusturur.

    {
        "parametre_adi": {
            "tip": "str",
            "aciklama": "event aciklamasi"
        }
    }
    """
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "event": event
    }
    log_file_path = "port_logs.json"
    try:
        # Log dosyasi izinlerini sinirla
        if not os.path.exists(log_file_path):
            with open(log_file_path, "w") as log_file:
                os.chmod(log_file_path, 0o600)  # Sadece root okuyup yazabilir
        with open(log_file_path, "a") as log_file:
            log_file.write(json.dumps(log_entry) + "\n")
    except IOError as e:
        print(f"Log dosyasina yazma hatasi: {e}")

def check_port_status(port):
    """Belirtilen portun acik olup olmadigini kontrol eder.

    {
        "parametre_adi": {
            "tip": "int",
            "aciklama": "Kontrol edilecek port numarasi"
        }
    }
    """
    try:
        result = subprocess.run(
            ["sudo", "iptables", "-L", "INPUT", "-v", "-n"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )
        return str(port) in result.stdout
    except subprocess.SubprocessError as e:
        print(f"Port durumu kontrol edilemedi: {e}")
        return False

def open_port(port):
    """Belirtilen portu guvenlik duvarinda acar.

    {
        "parametre_adi": {
            "tip": "int",
            "aciklama": "Acilacak port numarasi"
        }
    }
    """
    if check_port_status(port):
        print(f"Port {port} zaten acik!")
        return
    try:
        subprocess.run(
            ["sudo", "iptables", "-A", "INPUT", "-p", "tcp", "--dport", str(port), "-j", "ACCEPT"],
            stderr=subprocess.DEVNULL
        )
        log_event(f"Port {port} acildi.")
    except subprocess.SubprocessError as e:
        print(f"Port acma islemi basarisiz: {e}")

def close_port(port):
    """Belirtilen portu guvenlik duvarinda kapatir.

    {
        "parametre_adi": {
            "tip": "int",
            "aciklama": "Kapatilacak port numarasi"
        }
    }
    """
    try:
        subprocess.run(
            ["sudo", "iptables", "-D", "INPUT", "-p", "tcp", "--dport", str(port), "-j", "ACCEPT"],
            stderr=subprocess.DEVNULL
        )
        log_event(f"Port {port} kapatildi.")
        # Port tarama icin guvenlik onlemi ekle
        subprocess.run(
            ["sudo", "iptables", "-A", "INPUT", "-p", "tcp", "--tcp-flags", "ALL", "SYN,ACK", "-m", "limit", "--limit", "5/min", "-j", "LOG", "--log-prefix", "Port Scan Detected: ", "--log-level", "4"],
            stderr=subprocess.DEVNULL
        )
        subprocess.run(
            ["sudo", "iptables", "-A", "INPUT", "-p", "tcp", "--tcp-flags", "ALL", "SYN,ACK", "-j", "DROP"],
            stderr=subprocess.DEVNULL
        )
    except subprocess.SubprocessError as e:
        print(f"Port kapatma islemi basarisiz: {e}")

def close_port_and_process(port):
    """Belirtilen portu guvenlik duvarinda kapatir ve portu dinleyen islemi sonlandirir.

    {
        "parametre_adi": {
            "tip": "int",
            "aciklama": "Kapatilacak port numarasi"
        }
    }
    """
    try:
        result = subprocess.run(
            ["sudo", "lsof", "-i", f":{port}"],
            stdout=subprocess.PIPE,
            text=True
        )
        lines = result.stdout.splitlines()
        if len(lines) > 1:  # Ilk satir baslik bilgisi icerir
            for line in lines[1:]:
                cols = line.split()
                pid = cols[1]  # PID genelde ikinci sutundur
                print(f"PID {pid} ile calisan islem sonlandiriliyor...")
                subprocess.run(["sudo", "kill", "-9", pid])
        else:
            print(f"Port {port} icin calisan islem bulunamadi.")
        close_port(port)
        save_rules()
        log_event(f"Port {port} ve ilgili islemler kapatildi.")
    except subprocess.SubprocessError as e:
        print(f"Islem sonlandirma veya port kapatma islemi basarisiz: {e}")

def save_rules():
    """Guvenlik duvari kurallarini kaydeder.

    {
        "parametre_adi": {
            "tip": "None",
            "aciklama": "Herhangi bir parametre almaz."
        }
    }
    """
    try:
        subprocess.run(
            ["sudo", "iptables-save", "-c", ">", "/etc/iptables/rules.v4"],
            shell=True,
            stderr=subprocess.DEVNULL
        )
    except subprocess.SubprocessError as e:
        print(f"Guvenlik duvari kurallari kaydedilemedi: {e}")

def log_port_traffic(port):
    """Porta yapilan her istegi loglar.

    {
        "parametre_adi": {
            "tip": "int",
            "aciklama": "Loglanacak port numarasi"
        }
    }
    """
    print(f"Port {port} uzerindeki trafigi loglama baslatiliyor...")
    try:
        process = subprocess.Popen(
            ["sudo", "tcpdump", "-i", "any", f"port {port}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )
        for line in process.stdout:
            log_event(f"Port {port} trafigi: {line.strip()}")
    except Exception as e:
        log_event(f"Port {port} uzerindeki trafik loglanamadi: {e}")

def start_traffic_logging(port):
    """Trafik loglama islemini bir is parcacigi olarak baslatir.

    {
        "parametre_adi": {
            "tip": "int",
            "aciklama": "Loglanacak port numarasi"
        }
    }
    """
    thread = threading.Thread(target=log_port_traffic, args=(port,))
    thread.daemon = True
    thread.start()

def scheduled_port(port, start_time, end_time):
    """Belirtilen portu belirtilen saat araliginda acip kapatir.

    {
        "parametre_adi": {
            "port": {
                "tip": "int",
                "aciklama": "Planlanacak port numarasi"
            },
            "start_time": {
                "tip": "str",
                "aciklama": "Portun acilacagi saat (HH:MM formatinda)"
            },
            "end_time": {
                "tip": "str",
                "aciklama": "Portun kapanacagi saat (HH:MM formatinda)"
            }
        }
    }
    """
    print(f"Port {port}, {start_time} ile {end_time} arasinda acik olacak...")
    while True:
        try:
            now = datetime.now().strftime("%H:%M")
            if now == start_time:
                print(f"Port {port} aciliyor...")
                open_port(port)
                save_rules()
                start_traffic_logging(port)
            elif now == end_time:
                print(f"Port {port} kapatiliyor...")
                close_port_and_process(port)
                break
        except Exception as e:
            print(f"Zamanli port yonetiminde hata: {e}")
        time.sleep(30)  # 30 saniyede bir kontrol

def menu():
    while True:
        print("\n=== Port Tabanli Guvenlik Duvari Yonetimi ===")
        print("1. Port Ac")
        print("2. Port Kapat")
        print("3. Zamanli Port")
        print("4. Cikis")
        choice = input("Seciminizi yapin (1-4): ")

        try:
            if choice == "1":
                port = input("Acmak istediginiz port numarasini girin: ")
                if not port.isdigit():
                    print("Lutfen gecerli bir port numarasi girin!")
                    continue

                port = int(port)
                if check_port_status(port):
                    print(f"Port {port} zaten acik!")
                else:
                    open_port(port)
                    save_rules()
                    start_traffic_logging(port)
                    print(f"Port {port} basariyla acildi.")
            elif choice == "2":
                port = input("Kapatmak istediginiz port numarasini girin: ")
                if not port.isdigit():
                    print("Lutfen gecerli bir port numarasi girin!")
                    continue

                port = int(port)
                if not check_port_status(port):
                    print(f"Port {port} zaten kapali!")
                else:
                    close_port_and_process(port)
            elif choice == "3":
                port = input("Zamanli olarak acmak istediginiz port numarasini girin: ")
                if not port.isdigit():
                    print("Lutfen gecerli bir port numarasi girin!")
                    continue

                port = int(port)
                start_time = input("Portun acilmasini istediginiz saati girin (HH:MM formatinda): ")
                end_time = input("Portun kapanmasini istediginiz saati girin (HH:MM formatinda): ")

                try:
                    datetime.strptime(start_time, "%H:%M")
                    datetime.strptime(end_time, "%H:%M")
                except ValueError:
                    print("Lutfen gecerli bir saat formati girin (HH:MM)!")
                    continue

                scheduled_port(port, start_time, end_time)
            elif choice == "4":
                print("Cikis yapiliyor...")
                break
            else:
                print("Gecersiz secim! Lutfen tekrar deneyin.")
        except Exception as e:
            print(f"Beklenmeyen bir hata olustu: {e}")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("Bu programi calistirmak icin root yetkisi gereklidir.")
    else:
        menu()
