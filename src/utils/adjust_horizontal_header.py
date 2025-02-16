

class AdjustHorizontalHeader:

    @staticmethod
    def for_students_table_view(horizontal_header):

        horizontal_header.resizeSection(0, 90)
        horizontal_header.resizeSection(1, 220)
        horizontal_header.resizeSection(2, 220)
        horizontal_header.resizeSection(3, 90)
        horizontal_header.resizeSection(4, 120)
        horizontal_header.resizeSection(5, 100)

        horizontal_header.setVisible(True)

    @staticmethod
    def for_programs_table_view(horizontal_header):

        horizontal_header.resizeSection(0, 110)
        horizontal_header.resizeSection(1, 460)
        horizontal_header.resizeSection(2, 110)

        horizontal_header.setVisible(True)

    @staticmethod
    def for_colleges_table_view(horizontal_header):
        horizontal_header.resizeSection(0, 100)
        horizontal_header.resizeSection(1, 580)

        horizontal_header.setVisible(True)



