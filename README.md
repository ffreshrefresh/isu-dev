# Port Firewall Management

Bu proje, **port tabanlı güvenlik duvarı yönetimi** için bir araç sağlar. Kullanıcılar port açma, kapama, zamanlama ve trafik loglama gibi işlemleri kolaylıkla gerçekleştirebilir. Araç, port güvenliğini artırmak için ek önlemler sunar ve loglama sistemiyle işlemleri kayıt altına alır.

---

## 🚀 Özellikler

- **Port Yönetimi:**
  - Belirtilen portları güvenlik duvarında açma ve kapatma.
  - Açık portların kontrol edilmesi.

- **Zamanlama:**
  - Portların belirli zaman aralıklarında otomatik olarak açılması ve kapatılması.

- **Trafik Loglama:**
  - Port üzerinden gelen tüm trafik `port_logs.json` dosyasına loglanır.

- **Güvenlik:**
  - Trafik sınırlamaları ve port tarama tespiti.

---

## 🛠️ Kurulum

### Gerekli Araçlar ve Teknolojiler:
- **Python 3.9 veya üzeri**
- **iptables** (Linux sistemlerde güvenlik duvarı yönetimi için)
- **tcpdump** (Port trafiğini loglamak için)

### Adımlar:

1. **Proje Deposu:**
   Depoyu klonlayın:
   ```bash
   git clone https://github.com/kullaniciadi/port-firewall-management.git
   cd port-firewall-management
2. Gereksinimleri indirin:
   pip install -r requirements.txt
   
3. Gerekli Sistem Araçları: iptables ve tcpdump yüklü değilse şu komutu çalıştırın:
   sudo apt install iptables tcpdump
   
4. Uygulamayı Çalıştırın:,
   sudo python3 autoport.py
   
## 🐐 Proje Ekibi

Engin Can Ünlüer - 2320191039

Ferhat Civelek - 2320191053
