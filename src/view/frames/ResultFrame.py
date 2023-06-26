from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt6.QtWidgets import QFrame, QGroupBox, QVBoxLayout, QComboBox, QPushButton, QSpinBox, QLabel, QGridLayout, \
    QSizePolicy, QHBoxLayout
from PyQt6.QtCore import Qt

from view.utils.MatPlotLibCanvas import MatPlotLibCanvas


class ResultFrame(QFrame):

    def __init__(self, strings: dict):
        super(ResultFrame, self).__init__()

        # Main Layout
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.strings = strings

        # Plot Result gb
        self.plot_result_gb = QGroupBox(self.strings['ResultFrame']['GroupBoxes'][0])
        self.main_layout.addWidget(self.plot_result_gb)

        # Plot config layout
        self.plot_result_layout = QVBoxLayout()
        self.plot_result_gb.setLayout(self.plot_result_layout)

        # Отрисовка результирующих 2d графиков
        self.mplc_2d = MatPlotLibCanvas(False)

        # Тулбар для работы с графиком
        self.nav_tb = NavigationToolbar(self.mplc_2d, self)

        # Отрисовка результирующих 3d графиков
        self.mplc_3d = MatPlotLibCanvas(True)
        self.mplc_3d.hide()

        # Graphic layout
        self.plot_result_layout.addWidget(self.nav_tb)
        self.plot_result_layout.addWidget(self.mplc_2d)
        self.plot_result_layout.addWidget(self.mplc_3d)

        self.sub_layout = QHBoxLayout()
        self.main_layout.addLayout(self.sub_layout)

        # Plot config gb
        self.plot_config_gb = QGroupBox(self.strings['ResultFrame']['GroupBoxes'][1])
        self.plot_config_gb.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        self.sub_layout.addWidget(self.plot_config_gb)

        # Plot config layout
        self.plot_layout = QGridLayout()
        self.plot_config_gb.setLayout(self.plot_layout)

        # Plot Type pick cb
        self.plot_type_layout = QVBoxLayout()
        self.plot_layout.addLayout(self.plot_type_layout, 0, 0)
        self.plot_type_label = QLabel(self.strings['ResultFrame']['PlotType'][0])
        self.plot_type_layout.addWidget(self.plot_type_label)

        self.plot_type_cb = QComboBox()
        self.plot_type_cb.addItem(self.strings['ResultFrame']['PlotType'][1], 0)
        self.plot_type_cb.addItem(self.strings['ResultFrame']['PlotType'][2], 1)
        self.plot_type_cb.addItem(self.strings['ResultFrame']['PlotType'][3], 2)
        self.plot_type_cb.addItem(self.strings['ResultFrame']['PlotType'][4], 3)
        self.plot_type_cb.addItem(self.strings['ResultFrame']['PlotType'][5], 4)
        self.plot_type_cb.addItem(self.strings['ResultFrame']['PlotType'][6], 5)
        self.plot_type_cb.addItem(self.strings['ResultFrame']['PlotType'][7], 6)
        self.plot_type_cb.addItem(self.strings['ResultFrame']['PlotType'][8], 7)
        self.plot_type_cb.addItem(self.strings['ResultFrame']['PlotType'][9], 8)
        self.plot_type_layout.addWidget(self.plot_type_cb)

        # Frame pick sb
        self.frame_pick_layout = QVBoxLayout()
        self.plot_layout.addLayout(self.frame_pick_layout, 0, 1)
        self.frame_pick_label = QLabel(self.strings['ResultFrame']['FrameNum'][0])
        self.frame_pick_layout.addWidget(self.frame_pick_label)

        self.frame_pick_sb = QSpinBox()
        self.frame_pick_sb.setRange(1, 1024)
        self.frame_pick_layout.addWidget(self.frame_pick_sb)

        # Loop pick sb
        self.loop_pick_layout = QVBoxLayout()
        self.plot_layout.addLayout(self.loop_pick_layout, 0, 2)
        self.loop_pick_label = QLabel(self.strings['ResultFrame']['LoopNum'][0])
        self.loop_pick_layout.addWidget(self.loop_pick_label)

        self.loop_pick_sb = QSpinBox()
        self.loop_pick_sb.setRange(1, 1024)
        self.loop_pick_layout.addWidget(self.loop_pick_sb)

        # Chirp pick sb
        self.chirp_pick_layout = QVBoxLayout()
        self.plot_layout.addLayout(self.chirp_pick_layout, 1, 0)
        self.chirp_pick_label = QLabel(self.strings['ResultFrame']['ChirpNum'][0])
        self.chirp_pick_layout.addWidget(self.chirp_pick_label)

        self.chirp_pick_sb = QSpinBox()
        self.chirp_pick_sb.setRange(1, 1024)
        self.chirp_pick_layout.addWidget(self.chirp_pick_sb)

        # Lane pick cb
        self.lane_pick_layout = QVBoxLayout()
        self.plot_layout.addLayout(self.lane_pick_layout, 1, 1)
        self.lane_pick_label = QLabel(self.strings['ResultFrame']['LaneNum'][0])
        self.lane_pick_layout.addWidget(self.lane_pick_label)

        self.lane_pick_cb = QComboBox()
        self.lane_pick_cb.addItem(self.strings['ResultFrame']['LaneNum'][1], 0)
        self.lane_pick_cb.addItem(self.strings['ResultFrame']['LaneNum'][2], 1)
        self.lane_pick_cb.addItem(self.strings['ResultFrame']['LaneNum'][3], 2)
        self.lane_pick_cb.addItem(self.strings['ResultFrame']['LaneNum'][4], 3)
        self.lane_pick_layout.addWidget(self.lane_pick_cb)

        # Plot button
        self.plot_result_layout = QVBoxLayout()
        self.plot_layout.addLayout(self.plot_result_layout, 1, 2)
        self.plot_result_label = QLabel(self.strings['ResultFrame']['PlotBuild'][0])
        self.plot_result_layout.addWidget(self.plot_result_label)

        self.plot_button = QPushButton(self.strings['ResultFrame']['PlotBuild'][1])
        self.plot_result_layout.addWidget(self.plot_button)

        # CFAR config gb
        self.cfar_config_gb = QGroupBox(self.strings['ResultFrame']['GroupBoxes'][3])
        self.cfar_config_gb.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        self.sub_layout.addWidget(self.cfar_config_gb)
        self.cfar_config_gb.hide()

        # CFAR layout
        self.cfar_layout = QGridLayout()
        self.cfar_config_gb.setLayout(self.cfar_layout)

        # Guard Cell layout
        self.guard_cell_layout = QVBoxLayout()
        # Guard Cell label
        self.guard_cell_label = QLabel(self.strings['ResultFrame']['CFAR'][0])
        self.guard_cell_layout.addWidget(self.guard_cell_label)
        # Guard Cell sb
        self.guard_cell_sb = QSpinBox()
        self.guard_cell_sb.setRange(1, 100)
        self.guard_cell_sb.setValue(5)
        self.guard_cell_layout.addWidget(self.guard_cell_sb)
        self.cfar_layout.addLayout(self.guard_cell_layout, 0, 0)

        # Training Cell layout
        self.training_cell_layout = QVBoxLayout()
        # Guard Cell label
        self.training_cell_label = QLabel(self.strings['ResultFrame']['CFAR'][1])
        self.training_cell_layout.addWidget(self.training_cell_label)
        # Guard Cell sb
        self.training_cell_sb = QSpinBox()
        self.training_cell_sb.setRange(1, 100)
        self.training_cell_sb.setValue(10)
        self.training_cell_layout.addWidget(self.training_cell_sb)
        self.cfar_layout.addLayout(self.training_cell_layout, 1, 0)

        # Navigation gp
        self.navigation_gp = QGroupBox(self.strings['ResultFrame']['GroupBoxes'][4])
        self.navigation_gp.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        self.navigation_gp.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.main_layout.addWidget(self.navigation_gp)
        # Navigation layout
        self.navigation_layout = QHBoxLayout()
        self.navigation_gp.setLayout(self.navigation_layout)
        # Re-config button
        self.re_config_button = QPushButton(self.strings['ResultFrame']['Navigation'][0])
        self.navigation_layout.addWidget(self.re_config_button)
        # Exit button
        self.exit_button = QPushButton(self.strings['ResultFrame']['Navigation'][1])
        self.navigation_layout.addWidget(self.exit_button)
