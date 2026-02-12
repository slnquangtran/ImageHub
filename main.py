import customtkinter as ctk
import threading
import os
import json
from imgdw import optimized_image_download

class ImageDownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        # Path to store user preferences (palette)
        self.config_path = os.path.join(os.path.expanduser("~"), ".imagehub_config.json")
        
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
        
        self.header_label = ctk.CTkLabel(
            header_frame,
            text="IMAGE HUB",
            font=ctk.CTkFont(size=26, weight="bold", family="Arial"),
            text_color="#FF8C00"  # Màu cam đậm
        )
        self.header_label.pack(expand=True)
        
        # Main content - frame với nền đen và border xám
        self.main_frame = ctk.CTkFrame(
            self, 
            corner_radius=20,
            fg_color="#111111",
            border_color="#555555",  # Border xám
            border_width=2
        )
        self.main_frame.pack(pady=15, padx=15, fill="both", expand=True)

        # Color palette bar (five swatches) for theming
        self.palette_colors = ["#A0B57A", "#CFE19A", "#F2F0D2", "#F4D9B5", "#C28B65"]
        self.accent_color = self.palette_colors[2]
        self.palette_blocks = []
        self._build_color_palette(self.main_frame)
        self._load_saved_palette()
        
        # Search section
        ctk.CTkLabel(
            self.main_frame,
            text="🔍 Search Keyword",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FF8C00"  # Cam
        ).pack(pady=(25, 5), padx=30, anchor="w")
        
        self.keyword_entry = ctk.CTkEntry(
            self.main_frame,
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
        slider_section = ctk.CTkFrame(self.main_frame, fg_color="transparent")
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
        quick_buttons_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
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
            self.main_frame,
            text="🚀 START DOWNLOAD",
            command=self.start_download,
            height=55,
            font=ctk.CTkFont(size=18, weight="bold"),
            corner_radius=12,
            fg_color="#FF8C00",  # Cam
            hover_color="#E67E00",  # Cam đậm hơn
            text_color=self._text_color_for_bg(self.accent_color),  # Chữ phù hợp màu nền
            border_color="#555555",  # Border xám
            border_width=2
        )
        self.download_btn.pack(pady=20, padx=30, fill="x")
        
        # Progress bar với màu cam
        self.progress_bar = ctk.CTkProgressBar(
            self.main_frame,
            height=8,
            corner_radius=4,
            fg_color="#1A1A1A",
            progress_color=self.accent_color,  # Cam
            border_color="#555555",  # Border xám
            border_width=1
        )
        self.progress_bar.pack(pady=5, padx=30, fill="x")
        self.progress_bar.set(0)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text="👆 Enter keyword and adjust slider",
            font=ctk.CTkFont(size=14),
            text_color=self.accent_color  # Cam
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

    # --- Color palette helpers ---
    def _build_color_palette(self, parent):
        """Create a horizontal color palette bar with five swatches."""
        palette_frame = ctk.CTkFrame(parent, height=40, corner_radius=6, fg_color="transparent")
        palette_frame.pack(pady=(6, 8), padx=30, fill="x")

        palette_strip = ctk.CTkFrame(palette_frame, fg_color="transparent")
        palette_strip.pack(fill="x")

        self.palette_blocks = []
        for idx, color in enumerate(self.palette_colors):
            swatch = ctk.CTkFrame(palette_strip, height=28, corner_radius=6, fg_color=color, border_color="#555555")
            swatch.pack(side="left", expand=True, fill="both", padx=6)
            swatch.bind("<Button-1>", lambda e, i=idx: self._on_palette_click(i))
            self.palette_blocks.append(swatch)

        self._highlight_selected_palette()

    def _on_palette_click(self, index):
        self.select_color(index)

    def select_color(self, index):
        self.accent_color = self.palette_colors[index]
        self._apply_color_theme(self.accent_color)
        self._highlight_selected_palette()
        self._save_palette(index=index)

    def _highlight_selected_palette(self):
        for i, block in enumerate(self.palette_blocks):
            if self.palette_colors[i] == self.accent_color:
                block.configure(border_width=2, border_color=self.accent_color)
            else:
                block.configure(border_width=1, border_color="#555555")

    def _apply_color_theme(self, color):
        # Determine readable text color on given bg
        text_color = self._text_color_for_bg(color)
        # Slightly lighter hover for button to show press feedback
        hover_color = self._adjust_color(color, 40)

        # Header
        if hasattr(self, 'header_label'):
            self.header_label.configure(text_color=color)
        # Main frame border/background tweaks via accent
        self.keyword_entry.configure(text_color=text_color)
        self.main_frame.configure(border_color="#555555")

        # Controls
        self.download_btn.configure(
            fg_color=color,
            hover_color=hover_color,
            text_color=text_color
        )
        self.count_slider.configure(progress_color=color, button_color=color, border_color="#555555")
        self.progress_bar.configure(progress_color=color)
        self.status_label.configure(text_color=color)
        # Entry/text hint may be updated as well
        self.count_display.configure(text_color=text_color)

    def _text_color_for_bg(self, hex_color):
        r, g, b = self._parse_hex(hex_color)
        # Relative luminance
        lum = (0.2126 * r + 0.7152 * g + 0.0722 * b)
        return '#000000' if lum > 128 else '#FFFFFF'

    def _parse_hex(self, hex_color):
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3:
            r = int(hex_color[0] * 2, 16)
            g = int(hex_color[1] * 2, 16)
            b = int(hex_color[2] * 2, 16)
        else:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
        return r, g, b

    def _rgb_to_hex(self, r, g, b):
        return '#%02x%02x%02x' % (max(0, min(255, int(r))), max(0, min(255, int(g))), max(0, min(255, int(b))))

    def _adjust_color(self, hex_color, amount=0):
        r, g, b = self._parse_hex(hex_color)
        r = max(0, min(255, r + amount))
        g = max(0, min(255, g + amount))
        b = max(0, min(255, b + amount))
        return self._rgb_to_hex(r, g, b)

    # Palette persistence helpers
    def _load_saved_palette(self):
        try:
            if not os.path.exists(self.config_path):
                return
            with open(self.config_path, "r") as f:
                data = json.load(f)
            idx = data.get("palette_index")
            color = data.get("palette_color")
            if isinstance(idx, int) and 0 <= idx < len(self.palette_colors):
                self.accent_color = self.palette_colors[idx]
            elif isinstance(color, str) and color in self.palette_colors:
                self.accent_color = color
                idx = self.palette_colors.index(color)
            else:
                return
            self._apply_color_theme(self.accent_color)
            self._highlight_selected_palette()
        except Exception:
            pass

    def _save_palette(self, index=None, color=None):
        try:
            if index is None and color is None:
                return
            if index is None and isinstance(color, str):
                if color in self.palette_colors:
                    index = self.palette_colors.index(color)
            if index is None:
                return
            with open(self.config_path, "w") as f:
                json.dump({"palette_index": int(index)}, f)
        except Exception:
            pass

if __name__ == "__main__":
    # Đảm bảo theme là dark mode
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    
    app = ImageDownloaderApp()
    app.mainloop()
