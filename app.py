import sys
import numpy as np
from scipy import signal as sp_signal

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QDoubleSpinBox, QComboBox, QGroupBox,
    QFrame, QSplitter, QScrollArea, QCheckBox
)
from PyQt5.QtCore import Qt

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# -------------------------------------------------------------------------
# UI Styling (Dark Flaw-Detector Theme)
# -------------------------------------------------------------------------
DARK_STYLE = """
QMainWindow {
    background-color: #090D11;
}
QWidget {
    color: #C9D1D9;
    font-family: "Segoe UI", "Helvetica Neue", Helvetica, Arial, sans-serif;
    font-size: 11px;
}
QGroupBox {
    border: 1px solid #1F2937;
    border-radius: 6px;
    margin-top: 10px;
    font-weight: bold;
    color: #38BDF8;
    background-color: #111827;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 2px 8px;
    background-color: #111827;
    border-radius: 3px;
}
QLabel {
    color: #9CA3AF;
}
QDoubleSpinBox, QComboBox {
    background-color: #090D11;
    border: 1px solid #374151;
    border-radius: 4px;
    padding: 4px 6px;
    color: #38BDF8;
    font-weight: bold;
}
QDoubleSpinBox:focus, QComboBox:focus {
    border: 1px solid #38BDF8;
}
QCheckBox {
    color: #C9D1D9;
    font-weight: bold;
}
QFrame#metricCard {
    background-color: #090D11;
    border: 1px solid #1F2937;
    border-radius: 6px;
}
"""


class AScanAnalyzerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ultrasonic A-Scan Flaw Analyzer")
        self.resize(1420, 880)
        self.setMinimumSize(1024, 720)

        self.init_ui()
        self.recalculate()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(8)

        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        # -----------------------------------------------------------------
        # LEFT PANEL: Flaw Detector Controls
        # -----------------------------------------------------------------
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        scroll_content = QWidget()
        ctrl_layout = QVBoxLayout(scroll_content)

        # 1. Receiver & Probe Parameters
        group_rx = QGroupBox("1. RECEIVER & PROBE CONFIG")
        grid_rx = QGridLayout(group_rx)
        grid_rx.setSpacing(6)

        grid_rx.addWidget(QLabel("System Gain (dB):"), 0, 0)
        self.spin_gain = self.create_spinbox(0.0, 80.0, 24.0, grid_rx, 0, 1, step=1.0)

        grid_rx.addWidget(QLabel("Time Range (us):"), 1, 0)
        self.spin_range = self.create_spinbox(5.0, 100.0, 30.0, grid_rx, 1, 1, step=5.0)

        grid_rx.addWidget(QLabel("Probe Frequency (MHz):"), 2, 0)
        self.spin_freq = self.create_spinbox(0.5, 20.0, 5.0, grid_rx, 2, 1, step=0.5)

        grid_rx.addWidget(QLabel("Material Velocity (m/s):"), 3, 0)
        self.spin_velocity = self.create_spinbox(1000.0, 12000.0, 5900.0, grid_rx, 3, 1, step=50.0)

        grid_rx.addWidget(QLabel("Noise Floor Level (%):"), 4, 0)
        self.spin_noise = self.create_spinbox(0.0, 20.0, 2.5, grid_rx, 4, 1, step=0.5)

        ctrl_layout.addWidget(group_rx)

        # 2. Gate Setup & Threshold Detection
        group_gates = QGroupBox("2. GATES & THRESHOLD DETECTOR")
        grid_g = QGridLayout(group_gates)
        grid_g.setSpacing(6)

        grid_g.addWidget(QLabel("Gate A Start (us):"), 0, 0)
        self.spin_gate_a_start = self.create_spinbox(1.0, 50.0, 4.0, grid_g, 0, 1, step=0.5)

        grid_g.addWidget(QLabel("Gate A End (us):"), 1, 0)
        self.spin_gate_a_end = self.create_spinbox(1.0, 50.0, 16.0, grid_g, 1, 1, step=0.5)

        grid_g.addWidget(QLabel("Gate B Start (us):"), 2, 0)
        self.spin_gate_b_start = self.create_spinbox(1.0, 50.0, 16.5, grid_g, 2, 1, step=0.5)

        grid_g.addWidget(QLabel("Gate B End (us):"), 3, 0)
        self.spin_gate_b_end = self.create_spinbox(1.0, 50.0, 28.0, grid_g, 3, 1, step=0.5)

        grid_g.addWidget(QLabel("Detection Threshold (%):"), 4, 0)
        self.spin_threshold = self.create_spinbox(5.0, 100.0, 25.0, grid_g, 4, 1, step=5.0)

        ctrl_layout.addWidget(group_gates)

        # 3. Manual Cursors & Overlays
        group_cursor = QGroupBox("3. CURSORS & REF CURVES")
        grid_c = QGridLayout(group_cursor)
        grid_c.setSpacing(6)

        grid_c.addWidget(QLabel("Manual Cursor 1 (us):"), 0, 0)
        self.spin_cursor1 = self.create_spinbox(0.0, 100.0, 8.8, grid_c, 0, 1, step=0.2)

        self.chk_dac = QCheckBox("Enable DAC Reference Curve")
        self.chk_dac.setChecked(True)
        self.chk_dac.stateChanged.connect(self.recalculate)
        grid_c.addWidget(self.chk_dac, 1, 0, 1, 2)

        ctrl_layout.addWidget(group_cursor)
        ctrl_layout.addStretch()

        scroll.setWidget(scroll_content)
        left_layout.addWidget(scroll)

        # Connect change signals
        for spin in [self.spin_gain, self.spin_range, self.spin_freq, self.spin_velocity,
                     self.spin_noise, self.spin_gate_a_start, self.spin_gate_a_end,
                     self.spin_gate_b_start, self.spin_gate_b_end, self.spin_threshold, self.spin_cursor1]:
            spin.valueChanged.connect(self.recalculate)

        # -----------------------------------------------------------------
        # RIGHT PANEL: Oscilloscope Display & Quantitative Readouts
        # -----------------------------------------------------------------
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)

        # Readouts Header Grid
        metrics_group = QGroupBox("AUTOMATED ECHO ANALYSIS & READOUTS")
        grid_metrics = QGridLayout(metrics_group)
        grid_metrics.setSpacing(6)

        self.lbl_peak_amp = self.create_metric_card("Gate A Peak Amp", "0.0 %", grid_metrics, 0, 0)
        self.lbl_peak_tof = self.create_metric_card("Gate A Peak ToF", "0.00 us", grid_metrics, 0, 1)
        self.lbl_flaw_depth = self.create_metric_card("Flaw Depth (Gate A)", "0.00 mm", grid_metrics, 0, 2)
        self.lbl_bw_thick = self.create_metric_card("Back-wall Thick (Gate B)", "0.00 mm", grid_metrics, 1, 0)
        self.lbl_snr = self.create_metric_card("Signal-to-Noise Ratio", "0.0 dB", grid_metrics, 1, 1)
        self.lbl_cursor_val = self.create_metric_card("Cursor 1 Amplitude", "0.0 %", grid_metrics, 1, 2)

        right_layout.addWidget(metrics_group)

        # Industrial Scope Screen
        plots_group = QGroupBox("ULTRASONIC FLAW DETECTOR A-SCAN DISPLAY")
        layout_plots = QVBoxLayout(plots_group)

        self.fig = Figure(figsize=(9, 6), facecolor='#05080A')
        self.canvas = FigureCanvas(self.fig)
        layout_plots.addWidget(self.canvas)

        right_layout.addWidget(plots_group, stretch=1)

        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([360, 1040])

    def create_spinbox(self, min_val, max_val, val, layout, row, col, step=0.1):
        spin = QDoubleSpinBox()
        spin.setRange(min_val, max_val)
        spin.setValue(val)
        spin.setSingleStep(step)
        layout.addWidget(spin, row, col)
        return spin

    def create_metric_card(self, title, default_val, layout, row, col):
        card = QFrame()
        card.setObjectName("metricCard")
        vbox = QVBoxLayout(card)
        vbox.setContentsMargins(6, 4, 6, 4)

        lbl_title = QLabel(title.upper())
        lbl_title.setStyleSheet("color: #9CA3AF; font-size: 10px; font-weight: bold;")
        lbl_val = QLabel(default_val)
        lbl_val.setStyleSheet("color: #38BDF8; font-size: 12px; font-weight: bold;")

        vbox.addWidget(lbl_title)
        vbox.addWidget(lbl_val)
        layout.addWidget(card, row, col)
        return lbl_val

    def generate_ascan(self):
        gain_db = self.spin_gain.value()
        time_range = self.spin_range.value()
        fc = self.spin_freq.value()
        velocity = self.spin_velocity.value()
        noise_pct = self.spin_noise.value()

        v_mm_us = velocity / 1000.0

        # Time vector
        fs = max(50.0, fc * 16.0)
        t = np.linspace(0, time_range, int(time_range * fs))

        def echo_pulse(t0, base_amp):
            dt = t - t0
            dur = 2.5 / fc
            env = np.exp(-0.5 * (dt / (dur / 3.0)) ** 2)
            linear_gain = 10.0 ** (gain_db / 20.0)
            return base_amp * linear_gain * env * np.cos(2 * np.pi * fc * dt)

        # Pulse components: Initial Pulse, Surface Echo, Defect Echoes, Back-Wall Echo
        t_initial = 0.2
        t_surface = 1.5
        t_defect1 = 8.8   # Internal defect 1
        t_defect2 = 12.2  # Internal defect 2
        t_backwall = 22.5 # Back-wall

        rf_signal = echo_pulse(t_initial, 0.08)
        rf_signal += echo_pulse(t_surface, 0.06)
        rf_signal += echo_pulse(t_defect1, 0.035)
        rf_signal += echo_pulse(t_defect2, 0.015)
        rf_signal += echo_pulse(t_backwall, 0.05)

        # Add Gaussian noise floor
        np.random.seed(42)
        noise_std = (noise_pct / 100.0) * (10.0 ** (gain_db / 20.0)) * 0.01
        rf_signal += np.random.normal(0, noise_std, len(t))

        # Rectification (Full-Wave Rectified A-scan in % Screen Height)
        envelope = np.abs(sp_signal.hilbert(rf_signal - np.mean(rf_signal)))
        rectified_fsh = np.clip(envelope * 100.0, 0.0, 110.0)

        return t, rectified_fsh, v_mm_us, noise_std * 100.0

    def recalculate(self):
        t, rectified_fsh, v_mm_us, noise_fsh = self.generate_ascan()

        gA_start = self.spin_gate_a_start.value()
        gA_end = self.spin_gate_a_end.value()
        gB_start = self.spin_gate_b_start.value()
        gB_end = self.spin_gate_b_end.value()
        thresh = self.spin_threshold.value()
        cursor1_t = self.spin_cursor1.value()

        # Gate A Peak Search (Internal Defect Evaluation)
        mask_gA = (t >= gA_start) & (t <= gA_end)
        if np.any(mask_gA):
            sub_t = t[mask_gA]
            sub_fsh = rectified_fsh[mask_gA]
            idx_max = np.argmax(sub_fsh)
            peakA_amp = sub_fsh[idx_max]
            peakA_tof = sub_t[idx_max]

            if peakA_amp >= thresh:
                flaw_depth = (peakA_tof - 1.5) * v_mm_us / 2.0
            else:
                flaw_depth = 0.0
        else:
            peakA_amp, peakA_tof, flaw_depth = 0.0, 0.0, 0.0

        # Gate B Peak Search (Back-Wall Thickness Evaluation)
        mask_gB = (t >= gB_start) & (t <= gB_end)
        if np.any(mask_gB):
            sub_t = t[mask_gB]
            sub_fsh = rectified_fsh[mask_gB]
            idx_max = np.argmax(sub_fsh)
            peakB_tof = sub_t[idx_max]
            bw_thick = (peakB_tof - 1.5) * v_mm_us / 2.0
        else:
            bw_thick = 0.0

        # SNR Calculation (Gate A Peak vs Noise Floor)
        noise_level = max(0.01, noise_fsh)
        snr_db = 20.0 * np.log10(max(1.0, peakA_amp) / noise_level)

        # Cursor 1 Measurement
        idx_cursor = np.argmin(np.abs(t - cursor1_t))
        cursor_amp = rectified_fsh[idx_cursor]

        # Update Readout Cards
        self.lbl_peak_amp.setText(f"{peakA_amp:.1f} % FSH")
        self.lbl_peak_tof.setText(f"{peakA_tof:.2f} us")
        self.lbl_flaw_depth.setText(f"{flaw_depth:.2f} mm")
        self.lbl_bw_thick.setText(f"{bw_thick:.2f} mm")
        self.lbl_snr.setText(f"{snr_db:.1f} dB")
        self.lbl_cursor_val.setText(f"{cursor_amp:.1f} % FSH")

        self.plot_visuals(t, rectified_fsh, gA_start, gA_end, gB_start, gB_end, thresh, cursor1_t, peakA_tof, peakA_amp)

    def plot_visuals(self, t, rectified_fsh, gA_start, gA_end, gB_start, gB_end, thresh, cursor1_t, peakA_tof, peakA_amp):
        self.fig.clear()

        # Oscilloscope colors
        bg_color = '#05080A'
        grid_color = '#13231B'
        trace_color = '#00FF66'  # Phosphor Green
        gateA_color = '#FFCC00'  # Yellow
        gateB_color = '#00E5FF'  # Cyan
        thresh_color = '#FF3366' # Coral/Red
        cursor_color = '#E0E0E0'

        ax = self.fig.add_subplot(111)
        ax.set_facecolor(bg_color)

        # A-scan Rectified Waveform
        ax.plot(t, rectified_fsh, color=trace_color, linewidth=1.2, label="Rectified A-Scan")
        ax.fill_between(t, 0, rectified_fsh, color=trace_color, alpha=0.15)

        # Threshold Line
        ax.axhline(thresh, color=thresh_color, linestyle='--', linewidth=1.0, label=f"Threshold ({thresh:.0f}%)")

        # Gate A Overlay
        ax.plot([gA_start, gA_end], [thresh, thresh], color=gateA_color, linewidth=2.5, label="Gate A")
        ax.axvline(gA_start, color=gateA_color, linestyle=':', linewidth=0.8)
        ax.axvline(gA_end, color=gateA_color, linestyle=':', linewidth=0.8)

        # Gate B Overlay
        ax.plot([gB_start, gB_end], [thresh, thresh], color=gateB_color, linewidth=2.5, label="Gate B")
        ax.axvline(gB_start, color=gateB_color, linestyle=':', linewidth=0.8)
        ax.axvline(gB_end, color=gateB_color, linestyle=':', linewidth=0.8)

        # Distance Amplitude Correction (DAC) Reference Curve Option
        if self.chk_dac.isChecked():
            t_dac = np.linspace(1.5, self.spin_range.value(), 200)
            dac_curve = 85.0 * np.exp(-0.04 * (t_dac - 1.5))
            ax.plot(t_dac, dac_curve, color='#FF9900', linestyle='-.', linewidth=1.2, label="DAC Ref Curve (80% FSH)")

        # Manual Cursor Line
        ax.axvline(cursor1_t, color=cursor_color, linestyle='-', linewidth=1.0, label=f"Cursor 1 ({cursor1_t:.2f} us)")

        # Peak Detection Marker
        if peakA_amp >= thresh:
            ax.scatter([peakA_tof], [peakA_amp], color='#FF0055', s=60, zorder=5)

        ax.set_title("EPOCH-STYLE ULTRASONIC FLAW DETECTOR SCREEN", color='#00FF66', fontsize=9, fontweight='bold', loc='left')
        ax.set_xlabel("Time of Flight / Range (us)", color='#9CA3AF', fontsize=8)
        ax.set_ylabel("Amplitude (% Full Screen Height)", color='#9CA3AF', fontsize=8)
        ax.set_ylim(0, 110)
        ax.set_xlim(0, self.spin_range.value())

        # Oscilloscope Grid Lines (Major & Minor)
        ax.tick_params(colors='#9CA3AF', labelsize=7)
        ax.grid(True, which='major', linestyle='-', linewidth=0.6, color=grid_color)
        ax.minorticks_on()
        ax.grid(True, which='minor', linestyle=':', linewidth=0.3, color=grid_color)
        ax.legend(facecolor='#0B1217', edgecolor=grid_color, labelcolor='#C9D1D9', fontsize=7, loc='upper right')

        for spine in ax.spines.values():
            spine.set_color('#1F2937')

        self.fig.tight_layout()
        self.canvas.draw()


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setStyleSheet(DARK_STYLE)

    window = AScanAnalyzerApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()