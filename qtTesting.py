import sys
import os
import random
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QGridLayout
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QTimer

class ImageChangerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('CS335 Memory game')
        self.setGeometry(100, 100, 600, 600)

         # Set the window icon
        icon_path = os.path.join("assets", "code.png")
        self.setWindowIcon(QIcon(icon_path))


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

        # Create a list to hold the positions and assigned images
        self.card_positions = []

        # Create a list to keep track of flipped cards
        self.flipped_cards = []

        # Create a QLabel to cover the whole screen for displaying the "matched.png" image
        self.matched_label = QLabel(self.central_widget)
        self.matched_label.setAlignment(Qt.AlignCenter)
        self.matched_label.setGeometry(self.central_widget.geometry())
        self.matched_label.hide()

        # Create a timer for showing the matched image
        self.matched_timer = QTimer(self)
        self.matched_timer.setSingleShot(True)
        self.matched_timer.timeout.connect(self.reset_matched_cards)

        # Load the initial image for all squares (question-mark.png)
        for row in range(4):
            for col in range(4):
                image_label = QLabel(self)
                image_label.setAlignment(Qt.AlignCenter)
                self.load_image(image_label, "assets/question-mark.png")
                self.image_labels.append(image_label)

                # Store the position and assigned image in the list
                self.card_positions.append(((row, col), image_files.pop()))

                # Connect the clicked signal to the change_image function for each label
                image_label.mousePressEvent = lambda event, row=row, col=col: self.change_image(event, row, col)

                self.layout.addWidget(image_label, row, col)

    def load_image(self, label, image_path):
        pixmap = QPixmap(image_path)
        label.setPixmap(pixmap)
        label.setFixedSize(pixmap.width(), pixmap.height())

    def change_image(self, event, row, col):
        # Check if the left mouse button is clicked
        if event.button() == Qt.LeftButton:
            # Find the position of the clicked square in the card_positions list
            index = row * 4 + col
            position, assigned_image = self.card_positions[index]

            # Check if the maximum number of flipped cards (2) is reached
            if len(self.flipped_cards) == 2:
                # Flip back the first card in the list
                first_card_index = self.flipped_cards.pop(0)
                self.flip_card_back(first_card_index)

            # Change the image of the clicked square to the assigned one
            image_path = os.path.join("assets", assigned_image)
            self.load_image(self.image_labels[index], image_path)

            # Keep track of the flipped card index
            self.flipped_cards.append(index)

            # Check if two cards are flipped and their images are the same
            if len(self.flipped_cards) == 2:
                first_index, second_index = self.flipped_cards
                first_image = self.card_positions[first_index][1]
                second_image = self.card_positions[second_index][1]

                if first_image == second_image:
                    # Display the "matched.png" image covering the whole screen for 2 seconds
                    self.show_matched_image()
                    return

            # Print the clicked card position and assigned image (Modify this part as needed)
            print(f"Card clicked: Position={position}, Assigned Image={assigned_image}")

    def flip_card_back(self, index):
        # Flip back the card at the given index to the initial image
        self.load_image(self.image_labels[index], "assets/question-mark.png")

    def show_matched_image(self):
        # Display the "matched.png" image covering the whole screen for 2 seconds
        self.load_image(self.matched_label, "assets/matched.png")
        self.matched_label.raise_()  # Bring the matched_label to the front
        self.matched_label.show()
        self.matched_timer.start(2000)  # 2000 milliseconds (2 seconds)

    def reset_matched_cards(self):
        # Reset the matched cards back to the initial state
        for index in self.flipped_cards:
            self.load_image(self.image_labels[index], "assets/question-mark.png")
        self.flipped_cards = []
        self.matched_label.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageChangerApp()
    window.show()
    sys.exit(app.exec_())
