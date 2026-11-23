# Modules
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QTextEdit, QComboBox,
    QPushButton, QLabel, QHBoxLayout, QVBoxLayout
)
from PyQt5.QtGui import (
    QFont, QPainter, QPen, QBrush, QLinearGradient, QColor, QPainterPath
)
from PyQt5.QtCore import Qt, QPointF
from googletrans import Translator
from languages import *


# Custom stylized "V" emblem
class CoolVBadge(QWidget):
    """Stilizovani V bedž sa gradijentom i blagim sjajem."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(104, 104)
        self.setToolTip("V Edition")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w, h = float(self.width()), float(self.height())
        pad = 10.0

        # Zaobljeni bedž okvir
        card_path = QPainterPath()
        card_path.addRoundedRect(pad, pad, w - 2 * pad, h - 2 * pad, 22.0, 22.0)

        bg_grad = QLinearGradient(0, pad, w, h - pad)
        bg_grad.setColorAt(0.0, QColor("#232936"))
        bg_grad.setColorAt(1.0, QColor("#171b24"))
        painter.fillPath(card_path, QBrush(bg_grad))

        # Plavo-ljubičasti gradijent za okvir i slovo V
        accent_grad = QLinearGradient(pad, pad, w - pad, h - pad)
        accent_grad.setColorAt(0.0, QColor("#6ea8ff"))
        accent_grad.setColorAt(0.5, QColor("#4f8cff"))
        accent_grad.setColorAt(1.0, QColor("#8b5cf6"))

        border_pen = QPen(QBrush(accent_grad), 2.2)
        painter.setPen(border_pen)
        painter.drawPath(card_path)

        # Oštro, moderno stilizovano slovo V
        v_path = QPainterPath()
        top_y = 29.0
        bot_y = 74.0
        mid_x = w / 2.0

        v_path.moveTo(27.0, top_y)
        v_path.lineTo(38.0, top_y)
        v_path.lineTo(mid_x, bot_y - 4.0)
        v_path.lineTo(w - 38.0, top_y)
        v_path.lineTo(w - 27.0, top_y)
        v_path.lineTo(mid_x + 3.8, bot_y + 2.0)
        v_path.lineTo(mid_x - 3.8, bot_y + 2.0)
        v_path.closeSubpath()

        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(accent_grad))
        painter.drawPath(v_path)

        # Mali sjajni akcenat u gornjem levom kraku
        highlight_pen = QPen(QColor(255, 255, 255, 135), 1.5)
        painter.setPen(highlight_pen)
        painter.drawLine(QPointF(29.5, top_y + 2.0), QPointF(36.5, top_y + 2.0))


# Class
class Home(QWidget):
    def __init__(self):
        super().__init__()
        self.app_design()
        self.app_settings()
        self.buttons()

    def app_design(self):
        # Font
        ui_font = QFont("Segoe UI", 10)
        title_font = QFont("Segoe UI", 18, QFont.Bold)
        text_font = QFont("Segoe UI", 11)

        # Header
        self.title = QLabel("Translator")
        self.title.setFont(title_font)
        self.title.setObjectName("TitleLabel")

        self.subtitle = QLabel("Brz prevod između jezika")
        self.subtitle.setObjectName("SubtitleLabel")

        # Language selectors
        self.input_label = QLabel("Sa jezika:")
        self.input_label.setFont(ui_font)
        self.input_options = QComboBox()
        self.input_options.addItems(values)

        self.output_label = QLabel("Na jezik:")
        self.output_label.setFont(ui_font)
        self.output_options = QComboBox()
        self.output_options.addItems(values)

        # Buttons
        self.submit = QPushButton("Translate")
        self.submit.setObjectName("PrimaryButton")
        self.submit.setCursor(Qt.PointingHandCursor)
        self.submit.setMinimumHeight(40)

        self.reverse = QPushButton("⇄ Reverse")
        self.reverse.setCursor(Qt.PointingHandCursor)
        self.reverse.setMinimumHeight(36)

        self.reset = QPushButton("Clear")
        self.reset.setCursor(Qt.PointingHandCursor)
        self.reset.setMinimumHeight(36)

        # Custom V badge
        self.v_badge = CoolVBadge()

        # Text boxes
        self.input_box = QTextEdit()
        self.input_box.setFont(text_font)
        self.input_box.setPlaceholderText("Unesi tekst za prevođenje...")

        self.output_box = QTextEdit()
        self.output_box.setFont(text_font)
        self.output_box.setPlaceholderText("Prevod će se pojaviti ovde...")
        self.output_box.setReadOnly(True)

        # Layouts
        self.master = QHBoxLayout()
        self.master.setContentsMargins(20, 20, 20, 20)
        self.master.setSpacing(20)

        col1 = QVBoxLayout()
        col1.setSpacing(10)

        col2 = QVBoxLayout()
        col2.setSpacing(12)

        # Left column (controls)
        col1.addWidget(self.title)
        col1.addWidget(self.subtitle)
        col1.addSpacing(12)
        col1.addWidget(self.input_label)
        col1.addWidget(self.input_options)
        col1.addWidget(self.output_label)
        col1.addWidget(self.output_options)
        col1.addSpacing(12)
        col1.addWidget(self.submit)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        btn_row.addWidget(self.reverse)
        btn_row.addWidget(self.reset)
        col1.addLayout(btn_row)

        col1.addStretch()

        badge_row = QHBoxLayout()
        badge_row.setContentsMargins(2, 0, 0, 0)
        badge_row.addWidget(self.v_badge, alignment=Qt.AlignLeft | Qt.AlignBottom)
        badge_row.addStretch()
        col1.addLayout(badge_row)

        # Right column (text areas)
        col2.addWidget(QLabel("Originalni tekst"))
        col2.addWidget(self.input_box, 1)
        col2.addWidget(QLabel("Prevedeni tekst"))
        col2.addWidget(self.output_box, 1)

        self.master.addLayout(col1, 30)
        self.master.addLayout(col2, 70)

        self.setLayout(self.master)

        # Modern Dark Stylesheet
        self.setStyleSheet("""
            QWidget {
                background-color: #181a1f;
                color: #e6e9ef;
                font-family: "Segoe UI";
                font-size: 10pt;
            }
            #TitleLabel {
                color: #ffffff;
                font-size: 18pt;
                font-weight: bold;
            }
            #SubtitleLabel {
                color: #9aa2b1;
                font-size: 9.5pt;
            }
            QTextEdit {
                background-color: #22262e;
                color: #f3f5f8;
                border: 1px solid #323846;
                border-radius: 10px;
                padding: 12px;
            }
            QTextEdit:focus {
                border: 1px solid #4f8cff;
            }
            QComboBox {
                background-color: #22262e;
                color: #f3f5f8;
                border: 1px solid #323846;
                border-radius: 8px;
                padding: 7px 10px;
            }
            QComboBox:hover {
                border: 1px solid #4f8cff;
            }
            QComboBox QAbstractItemView {
                background-color: #22262e;
                color: #f3f5f8;
                selection-background-color: #4f8cff;
                border: 1px solid #323846;
            }
            QPushButton {
                background-color: #262b35;
                color: #e6e9ef;
                border: 1px solid #384050;
                border-radius: 8px;
                padding: 8px 12px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #303744;
            }
            QPushButton:pressed {
                background-color: #1e222a;
            }
            #PrimaryButton {
                background-color: #4f8cff;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                font-weight: bold;
            }
            #PrimaryButton:hover {
                background-color: #3d7cf5;
            }
            #PrimaryButton:pressed {
                background-color: #2f68d6;
            }
        """)

    def app_settings(self):
        self.setWindowTitle("Translator")
        self.setGeometry(100, 100, 920, 620)
        self.setMinimumSize(720, 480)

    def buttons(self):
        self.submit.clicked.connect(self.translate_click)
        self.reset.clicked.connect(self.reset_click)
        self.reverse.clicked.connect(self.reverse_translate_text)

    def translate_click(self):
        source_text = self.input_box.toPlainText().strip()
        if not source_text:
            self.output_box.setPlainText("Unesi neki tekst pre kliktanja na Translate.")
            return

        dest_name = self.output_options.currentText()
        src_name = self.input_options.currentText()

        dest_codes = [k for k, v in LANGUAGES.items() if v == dest_name]
        src_codes = [k for k, v in LANGUAGES.items() if v == src_name]

        if not dest_codes or not src_codes:
            self.output_box.setPlainText("Greška: izabrani jezik nije pronađen.")
            return

        try:
            translated = self.translate_text(source_text, dest_codes[0], src_codes[0])
            self.output_box.setPlainText(translated)
        except Exception as e:
            self.output_box.setPlainText(f"Greška pri prevođenju:\n{e}")

    def reset_click(self):
        self.input_box.clear()
        self.output_box.clear()

    def translate_text(self, text, dest_lang, src_lang):
        translator = Translator()
        translation = translator.translate(text, dest=dest_lang, src=src_lang)
        return translation.text

    def reverse_translate_text(self):
        s1, l1 = self.input_box.toPlainText(), self.input_options.currentText()
        s2, l2 = self.output_box.toPlainText(), self.output_options.currentText()

        self.input_box.setPlainText(s2)
        self.output_box.setPlainText(s1)

        self.input_options.setCurrentText(l2)
        self.output_options.setCurrentText(l1)


# Main Run
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Home()
    window.show()
    sys.exit(app.exec_())