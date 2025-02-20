
# Rename to SpecificButtonsEnabler

class SpecificButtonsEnabler:
    # [0] is the delete button
    # [1] is the edit button

    @staticmethod
    def enable_delete_and_edit_buttons(buttons, model):

        if model.get_data()[0][0]:
            buttons[0].setEnabled(True)
            buttons[1].setEnabled(True)
        else:
            buttons[0].setEnabled(False)
            buttons[1].setEnabled(False)

    @staticmethod
    def enable_save_button(save_button, model):
        if model.get_has_changes():
            save_button.setEnabled(True)
        else:
            save_button.setEnabled(False)

