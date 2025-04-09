from helper_dialogs.delete_item_state.confirm_delete import ConfirmDeleteDialog
from helper_dialogs.delete_item_state.success_delete_item import SuccessDeleteItemDialog

from utils.specific_buttons_enabler import SpecificButtonsEnabler


# This class will be called by the delete button of the context menu
class DeleteEntityHandler:
    def __init__(self, selected_rows, identifiers, current_model, table_view, entity_type, save_changes_button,
                 undo_all_changes_button):

        self.selected_rows = selected_rows
        self.identifiers = identifiers
        self.current_model = current_model
        self.table_view = table_view
        self.entity_type = entity_type

        self.save_changes_button = save_changes_button
        self.undo_all_changes_button = undo_all_changes_button

    def delete_entities(self):
        self.confirm_to_delete_dialog = ConfirmDeleteDialog(self.entity_type, self.identifiers)
        self.confirm_to_delete_dialog.exec()

        confirm_delete_decision = self.confirm_to_delete_dialog.get_confirm_delete_decision()

        if confirm_delete_decision:

            for selected_row in self.selected_rows:
                self.current_model.delete_entity_from_db(selected_row, self.entity_type)

            self.current_model.update_data_from_db_after_deleting(self.selected_rows)

            self.table_view.clearSelection()
            self.current_model.update_page_view(self.table_view)

            self.current_model.set_has_changes(True)
            if self.entity_type == "student":

                SpecificButtonsEnabler.enable_save_and_undo_buttons(self.save_changes_button,
                                                                    self.undo_all_changes_button,
                                                                    students_table_model=self.current_model)
            elif self.entity_type == "program":

                SpecificButtonsEnabler.enable_save_and_undo_buttons(self.save_changes_button,
                                                                    self.undo_all_changes_button,
                                                                    programs_table_model=self.current_model)
            elif self.entity_type == "college":

                SpecificButtonsEnabler.enable_save_and_undo_buttons(self.save_changes_button,
                                                                    self.undo_all_changes_button,
                                                                    colleges_table_model=self.current_model)

            self.success_delete_item_dialog = SuccessDeleteItemDialog(self.entity_type)
            self.success_delete_item_dialog.exec()
