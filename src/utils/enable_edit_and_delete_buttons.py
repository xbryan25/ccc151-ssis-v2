
class EnableEditAndDeleteButtons:
    @staticmethod
    def enable_button(button, model):
        if model.get_data()[0][0] != "":
            button.setEnabled(True)
        else:
            button.setEnabled(False)
