import sys
import os
import random
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class ImageChangerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Image Changer App')
        self.setGeometry(100, 100, 600, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QGridLayout(self.central_widget)

        # Get the list of image file names from the assets folder
        image_files = [
            "archer.png", "bomb.png", "chip.png", "knight.png",
            "map.png", "rubiks-cube.png", "treasure.png", "virtual-reality.png"
        ]

        # Duplicate the image file names to create pairs
        image_files *= 2

        # Shuffle the list of image file names
        random.shuffle(image_files)

        # Create a list to hold references to the image labels
        self.image_labels = []

        # Load the initial image for all squares (question-mark.png)
        for row in range(4):
            for col in range(4):
                image_label = QLabel(self)
                image_label.setAlignment(Qt.AlignCenter)
                self.load_image(image_label, "assets/question-mark.png")
                self.image_labels.append(image_label)

                # Connect the clicked signal to the change_image function for each label
                image_label.mousePressEvent = lambda event, row=row, col=col: self.change_image(event, row, col)

                self.layout.addWidget(image_label, row, col)

        # Store the randomly assigned images for each card
        self.randomly_assigned_images = list(image_files)

    def load_image(self, label, image_path):
        pixmap = QPixmap(image_path)
        label.setPixmap(pixmap)
        label.setFixedSize(pixmap.width(), pixmap.height())

    def change_image(self, event, row, col):
        # Check if the left mouse button is clicked
        if event.button() == Qt.LeftButton:
            # Change the image of the clicked square to the randomly assigned one
            index = row * 4 + col
            image_path = os.path.join("assets", self.randomly_assigned_images[index])
            self.load_image(self.image_labels[index], image_path)

            # Print the clicked card index (You can modify this part as needed)
            print(f"Card clicked: {index}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageChangerApp()
    window.show()
    sys.exit(app.exec_())
