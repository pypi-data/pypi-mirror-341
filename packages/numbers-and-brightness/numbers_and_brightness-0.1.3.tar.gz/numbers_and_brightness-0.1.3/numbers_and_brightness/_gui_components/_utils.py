from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox

def show_error_message(parent, message):
    msg_box = QMessageBox(parent)
    msg_box.setIcon(QMessageBox.Icon.Critical)
    msg_box.setWindowTitle("Error")
    msg_box.setText(message)
    msg_box.exec()

def show_finished_popup(parent, message, title):
    msg = QMessageBox(parent)
    msg.setIcon(QMessageBox.Icon.Information)
    msg.setWindowTitle(title)
    msg.setText(message)
    msg.exec()

def wrap_text(name: str, max_num: int) -> str:
    if len(name) > max_num:
        return f"...{name[-max_num:]}"
    return name