from PyQt6.QtWidgets import QHeaderView
from PyQt6.QtCore import Qt

from helper_dialogs.input_prerequisite.input_prerequisite import InputPrerequisiteDialog
from helper_dialogs.save_or_undo_state.confirm_save_or_undo import ConfirmSaveOrUndoDialog
from helper_dialogs.save_or_undo_state.success_save_changes import SuccessSaveChangesDialog

from operation_dialogs.add_entity.add_student import AddStudentDialog
from operation_dialogs.add_entity.add_program import AddProgramDialog
from operation_dialogs.add_entity.add_college import AddCollegeDialog

from utils.specific_buttons_enabler import SpecificButtonsEnabler


class OpenDialogs:

    def __init__(self, application_window):

        self.aw = application_window

    def open_add_entity_dialog_for_students(self):

        if len(self.aw.students_table_model.db_handler.get_all_entities('program')) > 0:

            add_student_dialog = AddStudentDialog(self.aw.students_table_view, self.aw.students_table_model,
                                                  self.aw.save_changes_button, self.aw.undo_all_changes_button,
                                                  self.aw.reset_item_delegates.reset)
            add_student_dialog.exec()

        else:
            input_programs_dialog = InputPrerequisiteDialog("programs")
            input_programs_dialog.exec()

    def open_add_entity_dialog_for_programs(self):

        if len(self.aw.programs_table_model.db_handler.get_all_entities('college')) > 0:
            # Note: reset_item_delegates is a function

            add_program_dialog = AddProgramDialog(self.aw.programs_table_view, self.aw.programs_table_model,
                                                  self.aw.save_changes_button, self.aw.undo_all_changes_button,
                                                  self.aw.reset_item_delegates.reset)
            add_program_dialog.exec()


        else:
            input_college_dialog = InputPrerequisiteDialog("college")
            input_college_dialog.exec()

    def open_add_entity_dialog_for_colleges(self):

        add_college_dialog = AddCollegeDialog(self.aw.colleges_table_view, self.aw.colleges_table_model,
                                              self.aw.save_changes_button, self.aw.undo_all_changes_button,
                                              self.aw.reset_item_delegates.reset)
        add_college_dialog.exec()

    def open_confirm_save_or_undo_dialog(self, entity_type, button_type, max_pages_label):

        current_model = None
        current_table_view = None

        db_handler = self.aw.students_table_model.db_handler

        if entity_type == "student":
            current_model = self.aw.students_table_model
            current_table_view = self.aw.students_table_view
        elif entity_type == "program":
            current_model = self.aw.programs_table_model
            current_table_view = self.aw.colleges_table_view
        elif entity_type == "college":
            current_model = self.aw.colleges_table_model
            current_table_view = self.aw.colleges_table_view


        confirm_save_or_undo_dialog = ConfirmSaveOrUndoDialog(button_type)
        confirm_save_or_undo_dialog.exec()

        if confirm_save_or_undo_dialog.get_confirm_edit_decision():

            if button_type == "save":
                db_handler.commit_changes()

                self.aw.students_table_model.set_has_changes(False)
                self.aw.programs_table_model.set_has_changes(False)
                self.aw.colleges_table_model.set_has_changes(False)
            elif button_type == "undo":
                db_handler.rollback_changes()

                self.aw.students_table_model.set_has_changes(False)
                self.aw.programs_table_model.set_has_changes(False)
                self.aw.colleges_table_model.set_has_changes(False)

                self.aw.students_table_model.initialize_data()
                self.aw.programs_table_model.initialize_data()
                self.aw.colleges_table_model.initialize_data()

                if len(current_model.get_data()) == 0:
                    current_table_view.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
                else:
                    current_table_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

                current_model.model_data_is_empty()

                self.maintain_column_width(current_table_view, entity_type)

                if entity_type == "student":
                    max_pages_label.setText(f"/ {self.aw.students_table_model.max_pages}")
                elif entity_type == "program":
                    max_pages_label.setText(f"/ {self.aw.programs_table_model.max_pages}")
                elif entity_type == "college":
                    max_pages_label.setText(f"/ {self.aw.colleges_table_model.max_pages}")

            SpecificButtonsEnabler.enable_save_and_undo_buttons(self.aw.save_changes_button,
                                                                self.aw.undo_all_changes_button,
                                                                self.aw.students_table_model,
                                                                self.aw.programs_table_model,
                                                                self.aw.colleges_table_model)

            success_save_changes = SuccessSaveChangesDialog(button_type)
            success_save_changes.exec()

    @staticmethod
    def maintain_column_width(current_table_view, entity_type):

        table_horizontal_header = current_table_view.horizontalHeader()

        if entity_type == "student":
            table_horizontal_header.resizeSection(0, 110)
            table_horizontal_header.resizeSection(3, 110)
            table_horizontal_header.resizeSection(4, 130)

            table_horizontal_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
            table_horizontal_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            table_horizontal_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
            table_horizontal_header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
            table_horizontal_header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
            table_horizontal_header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)

        elif entity_type == "program":
            table_horizontal_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
            table_horizontal_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            table_horizontal_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)

        elif entity_type == "college":
            table_horizontal_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
            table_horizontal_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)