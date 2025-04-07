
class SpecificButtonsEnabler:

    @staticmethod
    def enable_save_and_undo_buttons(save_button, undo_button, students_table_model=None, programs_table_model=None,
                                     colleges_table_model=None):

        if ((students_table_model and students_table_model.get_has_changes()) or
                (programs_table_model and programs_table_model.get_has_changes()) or
                (colleges_table_model and colleges_table_model.get_has_changes())):

            save_button.setEnabled(True)
            undo_button.setEnabled(True)
        else:
            save_button.setEnabled(False)
            undo_button.setEnabled(False)

