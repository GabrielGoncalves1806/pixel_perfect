import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QSlider,
    QVBoxLayout, QHBoxLayout, QFileDialog,
    QScrollArea, QFrame, QLineEdit, QPushButton
)
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import Qt


class Overlay(QWidget):

    def __init__(self, image_path):
        super().__init__()
        
        self.image_path = image_path
        self.original_pixmap = QPixmap(self.image_path)

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAutoFillBackground(False)
        self.setStyleSheet("background: transparent;")

        self.setWindowTitle("Pixel Perfect Overlay")

        # 👇 sempre no topo
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)

        self.resize(900, 700)

        main_layout = QVBoxLayout()

        # -------------------------
        # PAINEL DE CONTROLE
        # -------------------------

        control_panel = QFrame()
        control_panel.setStyleSheet("background-color: rgba(30, 30, 30, 0.9);")
        control_layout = QHBoxLayout()

        self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.opacity_slider.setRange(10, 100)
        self.opacity_slider.setValue(100)
        self.opacity_slider.valueChanged.connect(self.change_opacity)

        self.window_opacity_supported = sys.platform != "linux"
        self.current_alpha = 1.0

        self.scale_multiplier = 10  # allow tenths of a percent

        self.scale_slider = QSlider(Qt.Orientation.Horizontal)
        self.scale_slider.setRange(10 * self.scale_multiplier, 300 * self.scale_multiplier)
        self.scale_slider.setValue(100 * self.scale_multiplier)
        self.scale_slider.valueChanged.connect(self.change_scale)

        self.scale_input = QLineEdit()
        self.scale_input.setText(self._format_scale_text(self.scale_slider.value()))
        self.scale_input.setMaximumWidth(70)
        self.scale_input.returnPressed.connect(self.update_scale_from_input)

        self.change_image_button = QPushButton("Trocar imagem")
        self.change_image_button.clicked.connect(self.select_new_image)

        control_layout.addWidget(QLabel("Opacidade"))
        control_layout.addWidget(self.opacity_slider)

        scale_layout = QVBoxLayout()
        scale_layout.addWidget(QLabel("Escala"))
        scale_layout.addWidget(self.scale_slider)
        scale_layout.addWidget(self.scale_input)
        
        control_layout.addLayout(scale_layout)
        control_layout.addWidget(self.change_image_button)

        control_panel.setLayout(control_layout)

        # -------------------------
        # AREA DA IMAGEM
        # -------------------------

        self.image_label = QLabel()
        self.image_label.setStyleSheet("background: transparent;")
        self.refresh_image()

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.image_label)
        self.scroll_area.setWidgetResizable(False)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setStyleSheet("background: transparent;")
        self.scroll_area.viewport().setStyleSheet("background: transparent;")

        main_layout.addWidget(control_panel)
        main_layout.addWidget(self.scroll_area)

        self.setLayout(main_layout)

    def change_opacity(self, value):
        self.current_alpha = value / 100
        if self.window_opacity_supported:
            self.setWindowOpacity(self.current_alpha)
        else:
            self.refresh_image()

    def change_scale(self, slider_value):
        self.apply_scale(slider_value)

    def update_scale_from_input(self):
        try:
            value = float(self.scale_input.text().replace(',', '.'))
            min_percent = self.scale_slider.minimum() / self.scale_multiplier
            max_percent = self.scale_slider.maximum() / self.scale_multiplier
            if min_percent <= value <= max_percent:
                slider_value = int(round(value * self.scale_multiplier))
                self.scale_slider.setValue(slider_value)
            else:
                self.scale_input.setText(self._format_scale_text(self.scale_slider.value()))
        except ValueError:
            self.scale_input.setText(self._format_scale_text(self.scale_slider.value()))

    def _format_scale_text(self, slider_value):
        if isinstance(slider_value, (int, float)):
            scale_percent = slider_value / self.scale_multiplier if isinstance(slider_value, int) else slider_value
        else:
            scale_percent = float(slider_value)
        return f"{scale_percent:.1f}"

    def apply_scale(self, slider_value=None):
        if slider_value is None:
            slider_value = self.scale_slider.value()
        scale_percent = slider_value / self.scale_multiplier
        self.scale_factor = scale_percent / 100
        self.scale_input.setText(self._format_scale_text(slider_value))
        self.refresh_image()

    def select_new_image(self):
        file, _ = QFileDialog.getOpenFileName(
            self,
            "Escolha a imagem",
            "",
            "Images (*.png *.jpg *.bmp)"
        )
        if file:
            self.image_path = file
            self.original_pixmap = QPixmap(self.image_path)
            self.apply_scale()

    def refresh_image(self):
        if self.original_pixmap.isNull():
            return

        target_size = self.original_pixmap.size() * self.scale_factor if hasattr(self, 'scale_factor') else self.original_pixmap.size()
        scaled = self.original_pixmap.scaled(
            target_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.FastTransformation
        )

        if self.window_opacity_supported or self.current_alpha >= 0.995:
            display_pixmap = scaled
        else:
            display_pixmap = QPixmap(scaled.size())
            display_pixmap.fill(Qt.GlobalColor.transparent)
            painter = QPainter(display_pixmap)
            painter.setOpacity(self.current_alpha)
            painter.drawPixmap(0, 0, scaled)
            painter.end()

        self.image_label.setPixmap(display_pixmap)
        self.image_label.resize(display_pixmap.size())


app = QApplication(sys.argv)

file, _ = QFileDialog.getOpenFileName(
    None,
    "Escolha a imagem",
    "",
    "Images (*.png *.jpg *.bmp)"
)

if file:
    window = Overlay(file)
    window.show()

sys.exit(app.exec())