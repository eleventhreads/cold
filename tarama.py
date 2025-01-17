import os
import shutil
from tkinter import Tk, filedialog, Button, Label, messagebox, Frame, ttk, Entry, StringVar, OptionMenu, Canvas, Scrollbar
from pathlib import Path
from PIL import Image, ImageTk

# PDF dosyalarındaki tarih bilgisi çıkarma (Kasım 2023 gibi)
def extract_date_from_filename(filename):
    parts = filename.split()
    if len(parts) >= 2:
        month = parts[0]
        year = parts[1]
        return f"{month}_{year}"
    return None

# PDF'leri uygun klasöre taşıma
def move_pdfs_to_folders(base_directory):
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith(".pdf"):
                folder_name = extract_date_from_filename(file)
                if folder_name:
                    target_folder = os.path.join(base_directory, folder_name)
                    Path(target_folder).mkdir(parents=True, exist_ok=True)  # Klasörü oluştur

                    # Dosyayı hedef klasöre taşı
                    source_file = os.path.join(root, file)
                    target_file = os.path.join(target_folder, file)
                    shutil.move(source_file, target_file)
                    print(f"Moved: {file} to {target_folder}")

# PDF sıralama işlemi
class PdfSorterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TERMAL BELEDİYESİ")
        self.root.geometry("500x750")

        # Dark mode renk paleti sağlar
        self.bg_color = "#545454"  # Koyu gri arka plan
        self.fg_color = "white"  # Beyaz yazı rengi
        self.button_bg_color = "#3498db"  # Buton rengi
        self.button_fg_color = "darkblue"  # Buton yazı rengi
        
        # Logo Resmi Yükleme
        self.logo_image = Image.open(r"C:\Users\Mert\Desktop\masaüstü\tarama\logo.png")
        self.logo_image = self.logo_image.resize((100, 100))  # Boyutlandırma (isteğe bağlı)
        self.logo = ImageTk.PhotoImage(self.logo_image)

        # Ana menü sekmesi oluşturma
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)
        
        # Ana menü ekranı
        self.main_menu_frame = Frame(self.notebook, bg=self.bg_color)
        self.notebook.add(self.main_menu_frame, text="Ana Menü")
        
        # Logo'yu Ana Menüye Ekle
        self.logo_label = Label(self.main_menu_frame, image=self.logo, bg=self.bg_color)
        self.logo_label.pack(pady=20)

        # Ana menüdeki butonlar
        self.label = Label(self.main_menu_frame, text="ANA MENÜ", font=("Helvetica", 16), fg=self.fg_color, bg=self.bg_color)
        self.label.pack(pady=20)

        # PDF sıralama aracı açma butonu
        self.open_sorting_button = Button(self.main_menu_frame, text="PDF Dosyası Kategorilendirme Aracı", command=self.ask_for_password, width=30, bg=self.button_bg_color, fg=self.button_fg_color)
        self.open_sorting_button.pack(pady=10)

        # Dosya arama aracı butonu
        self.open_search_button = Button(self.main_menu_frame, text="Dosya Arama Aracı", command=self.open_file_search_tool, width=30, bg=self.button_bg_color, fg=self.button_fg_color)
        self.open_search_button.pack(pady=10)

    # Şifre doğrulama fonksiyonu
    def ask_for_password(self):
        def verify_password():
            entered_password = password_entry.get()
            if entered_password == "1123":  # Burada şifreyi kontrol ediyoruz
                self.open_pdf_sorting_tool()  # Şifre doğruysa PDF sıralama aracını aç
                password_window.destroy()
            else:
                messagebox.showerror("Şifre Yanlış", "Yanlış şifre, tekrar deneyin. Şifreyi hatırlamıyorsanız Yönetici ile iletişime geçiniz!")

        # Şifre girmesi için pencere açıyoruz
        password_window = Tk()
        password_window.title("Şifre Girişi")
        password_window.geometry("300x150")

        password_label = Label(password_window, text="Şifreyi Girin:", font=("Helvetica", 12))
        password_label.pack(pady=10)

        password_entry = Entry(password_window, show="*", font=("Helvetica", 12))
        password_entry.pack(pady=5)

        submit_button = Button(password_window, text="Giriş", command=verify_password, width=20, bg=self.button_bg_color, fg=self.button_fg_color)
        submit_button.pack(pady=10)
        
        # Enter tuşuna basıldığında şifre doğrulama işlemini tetiklemek için bind ekliyoruz
        password_entry.bind("<Return>", lambda event: verify_password())  # Enter tuşuna basıldığında verify_password() fonksiyonunu çalıştır

        password_window.mainloop()

    # PDF Dosyası Kategorilendirme Aracı sekmesini açma
    def open_pdf_sorting_tool(self):
        # Yeni sekme oluşturma
        self.sorting_frame = Frame(self.notebook, bg=self.bg_color)
        self.notebook.add(self.sorting_frame, text="PDF Sıralama")

        # PDF sıralama sekmesi içeriği
        self.label = Label(self.sorting_frame, text="PDF dosyalarını kategorilere ayırın.", font=("Helvetica", 14), fg=self.fg_color, bg=self.bg_color)
        self.label.pack(pady=20)

        # Klasör seçme butonu
        self.select_button = Button(self.sorting_frame, text="Klasör Seç", command=self.select_folder, width=20, bg=self.button_bg_color, fg=self.button_fg_color)
        self.select_button.pack(pady=10)

        # Başlat butonu
        self.start_button = Button(self.sorting_frame, text="Başlat", state="disabled", command=self.start_sorting, width=20, bg=self.button_bg_color, fg=self.button_fg_color)
        self.start_button.pack(pady=10)

        # Sekmeyi kapatma butonu
        self.back_button = Button(self.sorting_frame, text="Sekmeyi Kapat", command=self.close_sorting_tool, width=20, bg=self.button_bg_color, fg=self.button_fg_color)
        self.back_button.pack(pady=10)

        # Seçilen klasör bilgisi
        self.selected_folder = None

        # Yeni açılan sekmeyi aktif hale getir
        self.notebook.select(self.sorting_frame)

    # Klasör seçme fonksiyonu
    def select_folder(self):
        self.selected_folder = filedialog.askdirectory(title="Klasör Seçin")
        if self.selected_folder:
            messagebox.showinfo("Klasör Eklendi", f"Seçilen Klasör: {self.selected_folder}")
            self.start_button.config(state="normal")  # Başlat butonunu aktif hale getir

    # PDF sıralama işlemi
    def start_sorting(self):
        if self.selected_folder:
            try:
                move_pdfs_to_folders(self.selected_folder)
                messagebox.showinfo("Başarı", "PDF'ler başarıyla sıralandı!")
            except Exception as e:
                messagebox.showerror("Hata", f"Bir hata oluştu: {e}")
        else:
            messagebox.showwarning("Klasör Seçilmedi", "Lütfen önce bir klasör seçin.")

    # PDF sıralama aracını kapatma ve ana menüye dönme
    def close_sorting_tool(self):
        # PDF sıralama sekmesini kapat
        self.notebook.forget(self.sorting_frame)
        self.selected_folder = None  # Seçilen klasörü sıfırla
        self.start_button.config(state="disabled")  # Başlat butonunu devre dışı bırak

        # Ana menüyü tekrar aktif hale getir
        self.notebook.select(self.main_menu_frame)

    # Dosya arama ekranını açma
    def open_file_search_tool(self):
        # Yeni sekme oluştur
        self.search_frame = Frame(self.notebook, bg=self.bg_color)
        self.notebook.add(self.search_frame, text="Dosya Arama")

        # Arama sekmesi içerikleri
        self.label = Label(self.search_frame, text="PDF dosyalarını arayın.", font=("Helvetica", 14), fg=self.fg_color, bg=self.bg_color)
        self.label.pack(pady=20)

        # Arşivlerin bulunduğu Klasörleri seçme butonu
        self.select_folder_button = Button(self.search_frame, text="Arşiv Klasörünü Seç", command=self.select_search_folder, width=30, bg=self.button_bg_color, fg=self.button_fg_color)
        self.select_folder_button.pack(pady=10)

        # Ay seçimi için filtreme aracını ekler
        self.month_filter_label = Label(self.search_frame, text="Ay Seçin (Boş bırakabilirsiniz):", fg=self.fg_color, bg=self.bg_color)
        self.month_filter_label.pack(pady=5)
        self.month_filter = StringVar(self.search_frame)
        self.month_filter.set("Tüm Aylar")
        months = ["Tüm Aylar", "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
        self.month_menu = OptionMenu(self.search_frame, self.month_filter, *months)
        self.month_menu.pack(pady=5)

        # Yıl seçimi için filtreleme yapılmasını sağlar
        self.year_filter_label = Label(self.search_frame, text="Yıl Girin (Boş bırakabilirsiniz):", fg=self.fg_color, bg=self.bg_color)
        self.year_filter_label.pack(pady=5)
        self.year_filter = Entry(self.search_frame, width=30)
        self.year_filter.pack(pady=5)

        # Kelime arama filtresi yapılmasını sağlar
        self.name_filter_label = Label(self.search_frame, text="Kelime ile Arama (Boş bırakabilirsiniz):", fg=self.fg_color, bg=self.bg_color)
        self.name_filter_label.pack(pady=5)
        self.name_filter_entry = Entry(self.search_frame, width=30)
        self.name_filter_entry.pack(pady=5)

        # Arama başlatma butonu
        self.search_button = Button(self.search_frame, text="Arama Başlat", command=self.perform_search, width=20, bg=self.button_bg_color, fg=self.button_fg_color)
        self.search_button.pack(pady=10)

        # Arama sonuçlarını gösteren kısım
        self.results_frame = Frame(self.search_frame, bg=self.bg_color)
        self.results_frame.pack(pady=10)

        # Seçilen arama klasörü başlangıçta boş gelmesini sağlar
        self.search_folder = None

        # Arama sonuçlarının sayısını gösterecek etiket
        self.results_count_label = Label(self.search_frame, text="", font=("Helvetica", 12), fg=self.fg_color, bg=self.bg_color)
        self.results_count_label.pack(pady=10)

        # Sekmeyi aktif hale getir
        self.notebook.select(self.search_frame)

        # Geri dön butonu
        self.back_button = Button(self.search_frame, text="Sekmeyi Kapat", command=self.close_search_tool, width=20, bg=self.button_bg_color, fg=self.button_fg_color)
        self.back_button.pack(pady=10)

    # Arama yapacak klasörü seçme aracı
    def select_search_folder(self):
        self.search_folder = filedialog.askdirectory(title="Arama Yapılacak Klasörü Seçin")
        if self.search_folder:
            messagebox.showinfo("Klasör Seçildi", f"Arama yapılacak klasör: {self.search_folder}")

    # Türkçe karakterleri ve büyük/küçük harf farklarını dikkate almadan arama yapma büyük harfle yazarken türkçe karakter yazmıyoruz
    def perform_search(self):
        # Arama filtresi parametreleri
        month_filter = self.month_filter.get() if self.month_filter.get() != "Tüm Aylar" else None
        year_filter = self.year_filter.get().strip() if self.year_filter.get().strip() != "" else None
        name_filter = self.name_filter_entry.get().strip().lower()

        # Arama yapılacak klasörü pc içerisinde seçmemize yarar, ileride bu kısmı sabit yapmalıyız ama departmanlar bazında ayırmamız gerekecek
        if not self.search_folder:
            messagebox.showwarning("Klasör Seçilmedi", "Lütfen önce bir klasör seçiniz.")
            return

        # Arama sonuçlarını temizle farklı filtreleme ile arama yaptığımızda öncekileri ekrana getirmez
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        # Arama sonuçlarını depolayalım
        results = self.search_pdfs(self.search_folder, month_filter, year_filter, name_filter)

        # Sonuçları sayısı
        self.results_count_label.config(text=f"Bulunan Dosya Sayısı= {len(results)}")

        if results:
            # Kaydırılabilir bir alan hazırlıyoruz scrool kullanarak birden fazla veriyi karşımıza getirir
            canvas = Canvas(self.results_frame, bg=self.bg_color)
            scrollbar = Scrollbar(self.results_frame, orient="vertical", command=canvas.yview)
            results_frame = Frame(canvas, bg=self.bg_color)

            canvas.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side="right", fill="y")
            canvas.pack(side="left", fill="both", expand=True)
            canvas.create_window((0, 0), window=results_frame, anchor="nw")

            for file, folder in results:
                file_label = Label(results_frame, text=file, font=("Helvetica", 8), fg=self.fg_color, bg=self.bg_color)
                file_label.pack(pady=5)

                # Klasöre gitmek için buton pdf dosyalarının bulunduğu konumu seçmemizi sağlar
                open_folder_button = Button(results_frame, text="Klasöre Git", command=lambda folder=folder: os.startfile(folder), width=20, bg=self.button_bg_color, fg=self.button_fg_color)
                open_folder_button.pack(pady=5)

            # Canvas'ın boyutlarını güncelle
            results_frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))

        else:
            messagebox.showinfo("Sonuç Bulunamadı", "Arama kriterlerine uyan dosya bulunamadı.") 

    # PDF dosyalarını arama; bu işlemi sseçmiş ya da belirtmiş olduğumuz klasörün içerisinden bulur
    def search_pdfs(self, folder, month_filter=None, year_filter=None, name_filter=""):
        results = []
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.endswith(".pdf"):
                    filename_lower = file.lower()

                    # Arama kriterlerini kontrol eder arama kriterine olanları tutar
                    if name_filter and name_filter not in filename_lower:
                        continue
                    
                    if month_filter:
                        if not file.lower().startswith(month_filter.lower()):
                            continue
                    
                    if year_filter and not file.lower().__contains__(year_filter.lower()):
                        continue

                    # Kriterlere uyan dosyayı sonuç listesine ekle
                    results.append((file, root))
        return results

    # Dosya arama aracını kapatma  sekmeler arası koyulması gereken bir buton bu sayede programı kapatmadan birden fazla işlemi yapmamıza yarar
    def close_search_tool(self):
        self.notebook.forget(self.search_frame)
        self.search_folder = None
        self.notebook.select(self.main_menu_frame)

if __name__ == "__main__":
    root = Tk()
    app = PdfSorterApp(root)
    root.mainloop()