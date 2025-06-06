import sys
import numpy as np
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QSlider, QPushButton, QLabel, QLineEdit, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class SineWavePlotter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sine Wave GUI")
        self.resize(900, 500)

        # Constants
        self.X_MAX_DEFAULT = 4 * np.pi
        self.SLIDER_SCALE_FACTOR = 10
        self.SLIDER_MAX = int(self.X_MAX_DEFAULT * self.SLIDER_SCALE_FACTOR * 2)  # Allow 2x default range

        # Initialize state
        self.x = self.X_MAX_DEFAULT

        # Create UI
        self._setup_ui()
        self._connect_signals()
        self.update_plot()

    def _setup_ui(self):
        """Initialize all UI components."""
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Left Panel - Plot
        left_panel = QVBoxLayout()
        left_panel.setContentsMargins(0, 0, 10, 0)

        # Reset button
        self.reset_button = QPushButton("Reset")
        self.reset_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        left_panel.addWidget(self.reset_button, alignment=Qt.AlignLeft)

        # Matplotlib Figure
        self.fig = Figure(figsize=(5, 4))
        self.canvas = FigureCanvas(self.fig)
        self.axes = self.fig.add_subplot(111)
        left_panel.addWidget(self.canvas)

        # Right Panel - Controls
        right_panel = QFrame()
        right_panel.setFrameShape(QFrame.Box)
        right_panel.setStyleSheet("QFrame { border: 1px solid gray; }")
        right_panel.setFixedWidth(200)

        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(10, 10, 10, 10)

        # Input field
        input_row = QHBoxLayout()
        input_label = QLabel("x max:")
        self.input_field = QLineEdit(f"{self.x:.2f}")
        self.input_field.setFixedWidth(80)
        input_row.addWidget(input_label)
        input_row.addWidget(self.input_field)
        right_layout.addLayout(input_row)

        # Slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1, self.SLIDER_MAX)
        self.slider.setValue(int(self.x * self.SLIDER_SCALE_FACTOR))
        self._set_slider_style()
        right_layout.addWidget(self.slider)

        # Spacer
        right_layout.addStretch()

        # Result display
        self.result_label = QLabel()
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setText(f"sin({self.x:.2f}) = {np.sin(self.x):.4f}")
        right_layout.addWidget(self.result_label)

        # Add panels to main layout
        main_layout.addLayout(left_panel)
        main_layout.addWidget(right_panel)

    def _connect_signals(self):
        """Connect all UI signals to their handlers."""
        self.slider.valueChanged.connect(self._on_slider_changed)
        self.reset_button.clicked.connect(self._on_reset_clicked)
        self.input_field.editingFinished.connect(self._on_input_field_changed)

    def _set_slider_style(self):
        self.slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #999999;
                height: 8px;
                background: #cfcfcf;
                margin: 2px 0;
            }
            QSlider::handle:horizontal {
                background: blue;
                border: 1px solid #5c5c5c;
                width: 18px;
                margin: -2px 0;
                border-radius: 3px;
            }
        """)

    def _on_slider_changed(self, value):
        self.x = value / self.SLIDER_SCALE_FACTOR
        self._update_ui_values()
        self.update_plot()

    def _on_input_field_changed(self):
        try:
            val = float(self.input_field.text())
            if val > 0:
                self.x = val
                self._update_ui_values()
                self.update_plot()
        except ValueError:
            self._update_ui_values()  # Revert to last value

    def _on_reset_clicked(self):
        self.x = self.X_MAX_DEFAULT
        self._update_ui_values()
        self.update_plot()

    def _update_ui_values(self):
        self.slider.setValue(int(self.x * self.SLIDER_SCALE_FACTOR))
        self.input_field.setText(f"{self.x:.2f}")
        self.result_label.setText(f"sin({self.x:.2f}) = {np.sin(self.x):.4f}")

    def update_plot(self):
        x_vals = np.linspace(0, self.x, 1000)
        y_vals = np.sin(x_vals)
        self.axes.clear()
        self.axes.plot(x_vals, y_vals, color='green', linewidth=2)
        self.axes.set_title(f'sin(x): 0 to {self.x:.2f}')
        self.axes.set_xlabel('x')
        self.axes.set_ylabel('y')
        self.axes.grid(True, alpha=0.3)
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    plotter = SineWavePlotter()
    plotter.show()
    sys.exit(app.exec())