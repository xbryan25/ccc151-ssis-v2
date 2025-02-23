
# Sequence, a simple student information system (SSIS)

Sequence is a simple student information system (SSIS) made in accordance with the requirements of CCC151. 

The name 'Sequence' comes from the fact that the data in this application is stored in a particular order, hence, a sequence.

## Requirements
- Python 3.6+
- PyQT6

## Features

- Create, read, update, delete, and list (CRUDL) operations for students, programs, and colleges
- Search and sort operations
- Fullscreen mode
- Save data in lightweight .csv files

## Planned Features

- Undo changes
- Invalidate student that has a program that's not in the .csv file
- Invalidate program that is in a college that's not in the .csv file
- Settings page to disable the combobox in the table views, or entirely disable table view manipulation
- Delete multiple students using a checkbox
- Context menu popup upon right click while multiple entities are selected in the table, 
the context menu would show a delete option to delete multiple students


## To run the project on a local machine

Clone the project

```bash
  git clone https://github.com/xbryan25/ccc151-ssis-v1.git
```

Go to the project directory

```bash
  cd ccc151-ssis-v1
```

Create and activate the virtual environment

```bash
  python -m venv ccc151_ssis_v1_venv
  ccc151_ssis_v1_venv\Scripts\activate
```

Install dependencies

```bash
  pip install pyqt6
```

Switch to the working directory

```bash
  cd src
```

Run driver.py

```bash
  python3 driver.py
```
## Feedback

If you have any feedback, please reach out to @xbryan25 using this [email](mailto:bryanaganp25@gmail.com)

