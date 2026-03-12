import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QSlider,
    QVBoxLayout, QHBoxLayout, QFileDialog,
    QScrollArea, QFrame, QLineEdit
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class Overlay(QWidget):

    def __init__(self, image_path):
        super().__init__()
        
        self.image_path = image_path

        self.setWindowTitle("Pixel Perfect Overlay")

        # 👇 sempre no topo
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)

        self.resize(900, 700)

        main_layout = QVBoxLayout()

        # -------------------------
        # PAINEL DE CONTROLE
        # -------------------------

        control_panel = QFrame()
        control_layout = QHBoxLayout()

        self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.opacity_slider.setRange(10, 100)
        self.opacity_slider.setValue(100)
        self.opacity_slider.valueChanged.connect(self.change_opacity)

        self.scale_multiplier = 10  # allow tenths of a percent

        self.scale_slider = QSlider(Qt.Orientation.Horizontal)
        self.scale_slider.setRange(10 * self.scale_multiplier, 300 * self.scale_multiplier)
        self.scale_slider.setValue(100 * self.scale_multiplier)
        self.scale_slider.valueChanged.connect(self.change_scale)

        self.scale_input = QLineEdit()
        self.scale_input.setText(self._format_scale_text(self.scale_slider.value()))
        self.scale_input.setMaximumWidth(70)
        self.scale_input.returnPressed.connect(self.update_scale_from_input)

        control_layout.addWidget(QLabel("Opacidade"))
        control_layout.addWidget(self.opacity_slider)

        scale_layout = QVBoxLayout()
        scale_layout.addWidget(QLabel("Escala"))
        scale_layout.addWidget(self.scale_slider)
        scale_layout.addWidget(self.scale_input)
        
        control_layout.addLayout(scale_layout)

        control_panel.setLayout(control_layout)

        # -------------------------
        # AREA DA IMAGEM
        # -------------------------

        self.image_label = QLabel()
        self.image_label.setPixmap(QPixmap(image_path))

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.image_label)
        self.scroll_area.setWidgetResizable(False)

        main_layout.addWidget(control_panel)
        main_layout.addWidget(self.scroll_area)

        self.setLayout(main_layout)

    def change_opacity(self, value):
        self.setWindowOpacity(value / 100)

    def change_scale(self, slider_value):
        scale_percent = slider_value / self.scale_multiplier
        self.scale_factor = scale_percent / 100
        self.scale_input.setText(self._format_scale_text(slider_value))

        scaled = QPixmap(self.image_path).scaled(
            QPixmap(self.image_path).size() * self.scale_factor,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.FastTransformation
        )

        self.image_label.setPixmap(scaled)
        self.image_label.resize(scaled.size())

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