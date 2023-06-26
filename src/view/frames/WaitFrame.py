from PyQt6.QtCore import Qt
from PyQt6.QtGui import QMovie, QPixmap
from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout, QGroupBox, QHBoxLayout, QPushButton


class WaitFrame(QFrame):

    def __init__(self, strings: dict, successfully_image: str, gif: str, error_image: str):
        super(WaitFrame, self).__init__()

        self.strings = strings

        # Main Layout
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Wait gif
        self.wait_gif_label = QLabel()
        self.wait_gif_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.wait_gif_label)

        self.movie = QMovie(gif)
        self.wait_gif_label.setMovie(self.movie)
        self.movie.start()

        # Successfully image
        self.successfully_image = QPixmap(successfully_image)
        self.successfully_img = QLabel()
        self.successfully_img.setPixmap(self.successfully_image)
        self.successfully_img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.successfully_img.hide()
        self.main_layout.addWidget(self.successfully_img)

        # Error image
        self.error_img = QLabel()
        self.error_image = QPixmap(error_image)
        self.error_img.setPixmap(self.error_image)
        self.error_img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_img.hide()
        self.main_layout.addWidget(self.error_img)

        # Info label
        self.info_label = QLabel(self.strings['WaitFrame']['label'][0])
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.info_label)

        # navigation
        # Navigation gp
        self.navigation_layout = QHBoxLayout()
        # Exit button
        self.exit_button = QPushButton(self.strings['WaitFrame']['navigation'][0])
        self.navigation_layout.addWidget(self.exit_button)
        self.exit_button.setDisabled(True)
        # Back button
        self.back_button = QPushButton(self.strings['WaitFrame']['navigation'][1])
        self.navigation_layout.addWidget(self.back_button)
        self.back_button.setDisabled(True)
        # CSV create button
        self.csv_create_button = QPushButton(self.strings['WaitFrame']['navigation'][2])
        self.navigation_layout.addWidget(self.csv_create_button)
        self.csv_create_button.setDisabled(True)
        # Next button
        self.next_button = QPushButton(self.strings['WaitFrame']['navigation'][3])
        self.next_button.setDisabled(True)
        self.navigation_layout.addWidget(self.next_button)
        # Open log txt file
        self.open_log_button = QPushButton(self.strings['WaitFrame']['navigation'][4])
        self.open_log_button.hide()
        self.navigation_layout.addWidget(self.open_log_button)
        self.main_layout.addLayout(self.navigation_layout)
