import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene
from ui_file import Ui_MainWindow  # Import the generated UI class

class MeasurementPlotApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.run_button.clicked.connect(self.run_measurement_and_plot)

        # Create a QGraphicsScene for the plot display
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)

    def run_measurement_and_plot(self):
        # Simulating measurement data
        x = np.linspace(0, 10, 100)
        y = np.sin(x)

        # Clear the previous plot and plot new data
        plt.figure()
        plt.plot(x, y)
        plt.xlabel("X-axis")
        plt.ylabel("Y-axis")
        plt.title("Measurement Plot")
        plt.grid()

        # Display the plot in the QGraphicsScene
        self.scene.clear()
        self.scene.addPixmap(plt.gcf().canvas.get_renderer().tostring_argb())

def main():
    app = QApplication(sys.argv)
    window = MeasurementPlotApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
