
# 🚀 Port Firewall Menu Projesi

## 1. Projenin Amacı ve Genel İşleyişi
Port Firewall Menu, port tabanlı güvenlik duvarı yönetimini kullanıcı dostu bir menü sistemiyle kolaylaştırmayı hedefler. 
Kullanıcılar port açma, kapatma ve zamanlama işlemlerini hızlı bir şekilde gerçekleştirebilir. 
Ayrıca, portlar üzerindeki trafik loglanarak güvenlik amacıyla saklanır.

## 🐐 2. Takım Üyeleri
- **Engin Can Ünlüer** - 2320191039
- **Ferhat Civelek** - 2320191053

## 3. Kullanılan Kütüphaneler ve Versiyonları
- Python 3.9 veya üzeri
- subprocess (standart kütüphane)
- datetime (standart kütüphane)
- json (standart kütüphane)
- threading (standart kütüphane)

## 4. Gerekli Araçlar ve Kurulum Gereksinimleri
- **İşletim Sistemi:** Linux
- **Python:** 3.9 veya üzeri
- **Gerekli Paketler ve Araçlar:**
  - iptables
  - tcpdump

## 5. Zorunlu Çalışma Parametreleri
- **Port Numarası:** Açılacak, kapatılacak veya zamanlanacak port numarası belirtilmelidir.
- **Zaman Parametreleri:** Zamanlama özelliği için portun açılacağı ve kapanacağı saatler belirtilmelidir.

## 6. Opsiyonel Parametreler ve Kullanımları
- **Trafik Loglama:** Varsayılan olarak aktiftir. İstenirse bu özellik devre dışı bırakılabilir.
- **Menü Seçenekleri:** Yalnızca belirli işlemler seçilebilir (örneğin, sadece port açma işlemi).

## 🛠️ 7. Kurulum ve Çalıştırma Talimatları
1. **Depoyu Klonlayın:**
   ```bash
   git clone https://github.com/kullaniciadi/port-firewall-menu.git
   cd port-firewall-menu
   ```

2. **Gerekli Python Kütüphanelerini Yükleyin:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Projeyi Çalıştırın:**
   ```bash
   python3 autoport.py
   ```

4. **Menüden İşlemleri Seçin:**
   - Port açma
   - Port kapatma
   - Zamanlı port yönetimi
   - Trafik loglarını inceleme
