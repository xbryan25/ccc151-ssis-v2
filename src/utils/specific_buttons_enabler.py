

class SpecificButtonsEnabler:
    # [0] is the delete button
    # [1] is the edit button
    # [2] is the view demographic button

    @staticmethod
    def enable_buttons(buttons, model):

        if model.get_data()[0][0]:
            buttons[0].setEnabled(True)
        else:
            buttons[0].setEnabled(False)

    @staticmethod
    def enable_save_button(save_button, students_table_model=None, programs_table_model=None, colleges_table_model=None):

        if ((students_table_model and students_table_model.get_has_changes()) or
                (programs_table_model and programs_table_model.get_has_changes()) or
                (colleges_table_model and colleges_table_model.get_has_changes())):

            save_button.setEnabled(True)
        else:
            save_button.setEnabled(False)

