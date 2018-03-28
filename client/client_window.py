import sys
import PyQt5
# from auth_win import CMainWindow as WinAuth
from main_win import CAuthWindow
app = PyQt5.Qt.QApplication(sys.argv)
wnd = CAuthWindow()
wnd.show()
exit(app.exec())


