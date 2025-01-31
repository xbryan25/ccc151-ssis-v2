
from PyQt6.QtWidgets import QApplication
from landing_page.landing_page import LandingPage


def main():
    app = QApplication([])
    landing_page = LandingPage()

    landing_page.show()
    app.exec()


if __name__ == "__main__":
    main()
