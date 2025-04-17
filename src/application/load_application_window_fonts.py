from PyQt6.QtGui import QFont, QFontDatabase


class LoadApplicationWindowFonts:
    def __init__(self, application_window):
        self.aw = application_window

        self.cg_font_family = self.aw.cg_font_family

    def load_fonts(self):

        # Landing Page
        self.aw.landing_subtitle_label.setFont(QFont(self.cg_font_family, 14, QFont.Weight.DemiBold))
        self.aw.landing_title_label.setFont(QFont(self.cg_font_family, 48, QFont.Weight.DemiBold))
        self.aw.mode_label.setFont(QFont(self.cg_font_family, 14, QFont.Weight.DemiBold))
        self.aw.students_button.setFont(QFont(self.cg_font_family, 26, QFont.Weight.DemiBold))
        self.aw.programs_button.setFont(QFont(self.cg_font_family, 26, QFont.Weight.DemiBold))
        self.aw.colleges_button.setFont(QFont(self.cg_font_family, 26, QFont.Weight.DemiBold))
        self.aw.view_demographics_button.setFont(QFont(self.cg_font_family, 26, QFont.Weight.DemiBold))
        self.aw.about_this_app_button.setFont(QFont(self.cg_font_family, 16, QFont.Weight.DemiBold))
        self.aw.mode_button.setFont(QFont(self.cg_font_family, 16, QFont.Weight.DemiBold))

        # About This App Page
        self.aw.about_this_app_label.setFont(QFont(self.cg_font_family, 30, QFont.Weight.Medium))
        self.aw.about_this_app_title_label.setFont(QFont(self.cg_font_family, 30, QFont.Weight.Medium))
        self.aw.scroll_area_title_label.setFont(QFont(self.cg_font_family, 28, QFont.Weight.DemiBold))
        self.aw.scroll_area_contents.setFont(QFont(self.cg_font_family, 13, QFont.Weight.Medium))

        self.aw.about_this_app_back_to_main_button.setFont(QFont(self.cg_font_family, 14, QFont.Weight.DemiBold))

        # View Demographics Page

        self.aw.demographics_label.setFont(QFont(self.cg_font_family, 30, QFont.Weight.Medium))
        self.aw.demographics_title_label.setFont(QFont(self.cg_font_family, 30, QFont.Weight.Medium))

        self.aw.demographics_center_label.setFont(QFont(self.cg_font_family, 28, QFont.Weight.DemiBold))

        self.aw.gd_total_colleges_header_label.setFont(QFont(self.cg_font_family, 18, QFont.Weight.DemiBold))
        self.aw.gd_total_colleges_count_label.setFont(QFont(self.cg_font_family, 28, QFont.Weight.DemiBold))
        self.aw.gd_total_programs_header_label.setFont(QFont(self.cg_font_family, 18, QFont.Weight.DemiBold))
        self.aw.gd_total_programs_count_label.setFont(QFont(self.cg_font_family, 28, QFont.Weight.DemiBold))
        self.aw.gd_total_students_header_label.setFont(QFont(self.cg_font_family, 18, QFont.Weight.DemiBold))
        self.aw.gd_total_students_count_label.setFont(QFont(self.cg_font_family, 28, QFont.Weight.DemiBold))

        self.aw.sd_total_students_header_label.setFont(QFont(self.cg_font_family, 18, QFont.Weight.DemiBold))
        self.aw.sd_total_students_count_label.setFont(QFont(self.cg_font_family, 28, QFont.Weight.DemiBold))
        self.aw.sd_gender_header_label.setFont(QFont(self.cg_font_family, 18, QFont.Weight.DemiBold))
        self.aw.sd_gender_count_label.setFont(QFont(self.cg_font_family, 14, QFont.Weight.DemiBold))
        self.aw.sd_year_level_header_label.setFont(QFont(self.cg_font_family, 18, QFont.Weight.DemiBold))
        self.aw.sd_year_level_count_label.setFont(QFont(self.cg_font_family, 14, QFont.Weight.DemiBold))

        self.aw.pd_total_students_header_label.setFont(QFont(self.cg_font_family, 16, QFont.Weight.DemiBold))
        self.aw.pd_total_students_count_label.setFont(QFont(self.cg_font_family, 28, QFont.Weight.DemiBold))
        self.aw.pd_year_level_header_label.setFont(QFont(self.cg_font_family, 16, QFont.Weight.DemiBold))
        self.aw.pd_year_level_count_label.setFont(QFont(self.cg_font_family, 16, QFont.Weight.DemiBold))
        self.aw.pd_gender_header_label.setFont(QFont(self.cg_font_family, 16, QFont.Weight.DemiBold))
        self.aw.pd_gender_count_label.setFont(QFont(self.cg_font_family, 16, QFont.Weight.DemiBold))

        self.aw.cd_total_programs_header_label.setFont(QFont(self.cg_font_family, 16, QFont.Weight.DemiBold))
        self.aw.cd_total_programs_count_label.setFont(QFont(self.cg_font_family, 28, QFont.Weight.DemiBold))
        self.aw.cd_total_students_header_label.setFont(QFont(self.cg_font_family, 16, QFont.Weight.DemiBold))
        self.aw.cd_total_students_count_label.setFont(QFont(self.cg_font_family, 28, QFont.Weight.DemiBold))
        self.aw.cd_gender_header_label.setFont(QFont(self.cg_font_family, 16, QFont.Weight.DemiBold))
        self.aw.cd_gender_count_label.setFont(QFont(self.cg_font_family, 16, QFont.Weight.DemiBold))
        self.aw.cd_year_level_header_label.setFont(QFont(self.cg_font_family, 16, QFont.Weight.DemiBold))
        self.aw.cd_year_level_count_label.setFont(QFont(self.cg_font_family, 16, QFont.Weight.DemiBold))

        self.aw.demographics_type_combobox.setStyleSheet(f"""
                            QComboBox {{
                                font-family: {self.cg_font_family};
                                font-size: 32px;
                                font-weight: {QFont.Weight.DemiBold};
                            }}
                        """)

        self.aw.pd_select_college_combobox.setStyleSheet(f"""
                            QComboBox {{
                                font-family: {self.cg_font_family};
                                font-size: 18px;
                                font-weight: {QFont.Weight.Medium};
                            }}
                        """)

        self.aw.pd_select_program_combobox.setStyleSheet(f"""
                            QComboBox {{
                                font-family: {self.cg_font_family};
                                font-size: 18px;
                                font-weight: {QFont.Weight.Medium};
                            }}
                        """)

        self.aw.cd_select_college_combobox.setStyleSheet(f"""
                            QComboBox {{
                                font-family: {self.cg_font_family};
                                font-size: 18px;
                                font-weight: {QFont.Weight.Medium};
                            }}
                        """)

        self.aw.demographics_back_to_main_button.setFont(QFont(self.cg_font_family, 14, QFont.Weight.DemiBold))

        # Entity Page
        self.aw.entity_type_label.setFont(QFont(self.cg_font_family, 30, QFont.Weight.Medium))
        self.aw.title_label.setFont(QFont(self.cg_font_family, 30, QFont.Weight.Medium))
        self.aw.sort_label.setFont(QFont(self.cg_font_family, 13, QFont.Weight.Medium))

        self.aw.sort_type_combobox.setStyleSheet(f"""
                            QComboBox {{
                                font-family: {self.cg_font_family};
                                font-size: 16px;
                                font-weight: {QFont.Weight.Medium};
                            }}
                        """)

        self.aw.sort_order_combobox.setStyleSheet(f"""
                                    QComboBox {{
                                        font-family: {self.cg_font_family};
                                        font-size: 16px;
                                        font-weight: {QFont.Weight.Medium};
                                    }}
                                """)

        self.aw.search_label.setFont(QFont(self.cg_font_family, 13, QFont.Weight.Medium))

        self.aw.search_type_combobox.setStyleSheet(f"""
                                            QComboBox {{
                                                font-family: {self.cg_font_family};
                                                font-size: 16px;
                                                font-weight: {QFont.Weight.Medium};
                                            }}
                                        """)

        self.aw.search_method_combobox.setStyleSheet(f"""
                                                    QComboBox {{
                                                        font-family: {self.cg_font_family};
                                                        font-size: 16px;
                                                        font-weight: {QFont.Weight.Medium};
                                                    }}
                                                """)

        self.aw.search_input_lineedit.setFont(QFont(self.cg_font_family, 13, QFont.Weight.Medium))

        self.aw.students_table_view.setStyleSheet(f"""
                                                    QHeaderView::section {{
                                                        font-family: {self.cg_font_family};
                                                        font-size: 17px;
                                                        font-weight: {QFont.Weight.DemiBold};
                                                    }}
                                                """)

        self.aw.programs_table_view.setStyleSheet(f"""
                                                            QHeaderView::section {{
                                                                font-family: {self.cg_font_family};
                                                                font-size: 17px;
                                                                font-weight: {QFont.Weight.DemiBold};
                                                            }}
                                                        """)

        self.aw.colleges_table_view.setStyleSheet(f"""
                                                            QHeaderView::section {{
                                                                font-family: {self.cg_font_family};
                                                                font-size: 17px;
                                                                font-weight: {QFont.Weight.DemiBold};
                                                            }}
                                                        """)

        self.aw.back_to_main_button.setFont(QFont(self.cg_font_family, 14, QFont.Weight.DemiBold))
