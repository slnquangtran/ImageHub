import customtkinter as ctk
import threading
from imgdw import optimized_image_download

class ImageDownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Image Hub")
        self.geometry("550x500")
        self.resizable(False, False)
        
        # Đặt nền đen cho cửa sổ chính
        self.configure(fg_color="#000000")
        
        self.setup_ui()
        
    def setup_ui(self):
        # Header với nền đen và chữ cam
        header_frame = ctk.CTkFrame(
            self,
            height=70,
            corner_radius=0,
            fg_color="#0A0A0A",
            border_color="#555555",  # Border xám
            border_width=1
        )
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        header_label = ctk.CTkLabel(
            header_frame,
            text="IMAGE HUB",
            font=ctk.CTkFont(size=26, weight="bold", family="Arial"),
            text_color="#FF8C00"  # Màu cam đậm
        )
        header_label.pack(expand=True)
        
        # Main content - frame với nền đen và border xám
        main_frame = ctk.CTkFrame(
            self, 
            corner_radius=20,
            fg_color="#111111",
            border_color="#555555",  # Border xám
            border_width=2
        )
        main_frame.pack(pady=15, padx=15, fill="both", expand=True)
        
        # Search section
        ctk.CTkLabel(
            main_frame,
            text="🔍 Search Keyword",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FF8C00"  # Cam
        ).pack(pady=(25, 5), padx=30, anchor="w")
        
        self.keyword_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="What images are you looking for?",
            height=45,
            font=ctk.CTkFont(size=14),
            fg_color="#1E1E1E",
            border_color="#555555",  # Border xám
            text_color="#FFFFFF",
            placeholder_text_color="#888888"
        )
        self.keyword_entry.pack(pady=(0, 20), padx=30, fill="x")
        
        # Image Count Slider section
        slider_section = ctk.CTkFrame(main_frame, fg_color="transparent")
        slider_section.pack(pady=10, padx=30, fill="x")
        
        # Title and value display
        slider_header = ctk.CTkFrame(slider_section, fg_color="transparent")
        slider_header.pack(fill="x")
        
        ctk.CTkLabel(
            slider_header,
            text="📊 Number of Images",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FF8C00"  # Cam
        ).pack(side="left")
        
        # Value display với màu cam
        self.count_display = ctk.CTkLabel(
            slider_header,
            text="100",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#FF8C00",  # Cam
            width=50
        )
        self.count_display.pack(side="right")
        
        # Slider với màu cam
        self.count_slider = ctk.CTkSlider(
            slider_section,
            from_=1,
            to=500,
            number_of_steps=499,
            width=350,
            height=25,
            command=self.update_slider_value,
            fg_color="#222222",
            progress_color="#FF8C00",  # Cam cho phần đã chọn
            button_color="#FF8C00",  # Cam cho nút slider
            button_hover_color="#E67E00",  # Cam đậm hơn khi hover
            border_color="#555555",  # Border xám
            border_width=1
        )
        self.count_slider.set(100)
        self.count_slider.pack(pady=(10, 5), fill="x")
        
        # Slider ticks/labels
        ticks_frame = ctk.CTkFrame(slider_section, fg_color="transparent")
        ticks_frame.pack(fill="x")
        
        ticks = [1, 100, 200, 300, 400, 500]
        for tick in ticks:
            label = ctk.CTkLabel(
                ticks_frame,
                text=str(tick),
                font=ctk.CTkFont(size=10),
                text_color="#AAAAAA",
                width=50
            )
            label.pack(side="left", expand=True)
        
        # Quick selection buttons với border xám
        quick_buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        quick_buttons_frame.pack(pady=(5, 15), padx=30)
        
        ctk.CTkLabel(
            quick_buttons_frame,
            text="Quick select:",
            font=ctk.CTkFont(size=12),
            text_color="#FF8C00"  # Cam
        ).pack(side="left", padx=(0, 10))
        
        quick_counts = [50, 100, 200, 300]
        for count in quick_counts:
            btn = ctk.CTkButton(
                quick_buttons_frame,
                text=str(count),
                width=50,
                height=30,
                font=ctk.CTkFont(size=12),
                command=lambda c=count: self.set_slider_value(c),
                fg_color="#1A1A1A",
                hover_color="#FF8C00",  # Cam khi hover
                text_color="#FFFFFF",
                border_color="#555555",  # Border xám
                border_width=1
            )
            btn.pack(side="left", padx=5)
        
        # Download button với màu cam và border xám
        self.download_btn = ctk.CTkButton(
            main_frame,
            text="🚀 START DOWNLOAD",
            command=self.start_download,
            height=55,
            font=ctk.CTkFont(size=18, weight="bold"),
            corner_radius=12,
            fg_color="#FF8C00",  # Cam
            hover_color="#E67E00",  # Cam đậm hơn
            text_color="#000000",  # Chữ đen cho nổi bật
            border_color="#555555",  # Border xám
            border_width=2
        )
        self.download_btn.pack(pady=20, padx=30, fill="x")
        
        # Progress bar với màu cam
        self.progress_bar = ctk.CTkProgressBar(
            main_frame,
            height=8,
            corner_radius=4,
            fg_color="#1A1A1A",
            progress_color="#FF8C00",  # Cam
            border_color="#555555",  # Border xám
            border_width=1
        )
        self.progress_bar.pack(pady=5, padx=30, fill="x")
        self.progress_bar.set(0)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            main_frame,
            text="👆 Enter keyword and adjust slider",
            font=ctk.CTkFont(size=14),
            text_color="#FF8C00"  # Cam
        )
        self.status_label.pack(pady=(10, 20))
        
        # Bind Enter key
        self.bind('<Return>', lambda e: self.start_download())
        
    def update_slider_value(self, value):
        """Cập nhật giá trị hiển thị khi slider thay đổi"""
        self.count_display.configure(text=str(int(value)))
        
    def set_slider_value(self, value):
        """Đặt giá trị slider từ quick selection buttons"""
        self.count_slider.set(value)
        self.count_display.configure(text=str(value))
        
    def start_download(self):
        keyword = self.keyword_entry.get().strip()
        count = int(self.count_slider.get())
        
        if not keyword:
            self.status_label.configure(
                text="❌ Please enter a keyword",
                text_color="#FF6B6B"  # Đỏ cho lỗi
            )
            return
        
        self.status_label.configure(
            text=f"⏳ Downloading {count} images for '{keyword}'...",
            text_color="#FF8C00"  # Cam cho thông báo
        )
        self.download_btn.configure(state="disabled")
        self.progress_bar.start()
        
        def download_thread():
            try:
                downloaded_count = optimized_image_download(keyword, count)
                self.progress_bar.stop()
                self.progress_bar.set(1.0)
                self.status_label.configure(
                    text=f"✅ Successfully downloaded {downloaded_count} images!",
                    text_color="#FFD700"  # Vàng cho thành công
                )
            except Exception as e:
                self.progress_bar.stop()
                self.progress_bar.set(0)
                self.status_label.configure(
                    text=f"❌ Error: {str(e)[:60]}",
                    text_color="#FF6B6B"  # Đỏ cho lỗi
                )
            finally:
                self.download_btn.configure(state="normal")
        
        threading.Thread(target=download_thread, daemon=True).start()

if __name__ == "__main__":
    # Đảm bảo theme là dark mode
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    
    app = ImageDownloaderApp()
    app.mainloop()