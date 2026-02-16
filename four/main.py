import sys
from dataclasses import dataclass, field
from typing import List, Optional
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QTableView, QLineEdit, QPushButton, QComboBox,
    QMessageBox, QHeaderView, QFormLayout, QGroupBox, QLabel,
    QDateEdit
)
from PyQt5.QtCore import Qt, QAbstractTableModel, QDate

# ---------- Модели данных (хранятся в памяти) ----------
@dataclass
class Group:
    id: int
    name: str

@dataclass
class Student:
    id: int
    last_name: str
    first_name: str
    group_id: int

@dataclass
class Subject:
    id: int
    name: str

@dataclass
class Grade:
    id: int
    student_id: int
    subject_id: int
    grade: int          # 2..5
    date: QDate         # используем QDate для удобства

# Глобальные хранилища (вместо базы данных)
groups: List[Group] = []
students: List[Student] = []
subjects: List[Subject] = []
grades: List[Grade] = []

# Счётчики для уникальных ID
next_group_id = 1
next_student_id = 1
next_subject_id = 1
next_grade_id = 1

# ---------- Табличные модели для отображения в QTableView ----------
class BaseTableModel(QAbstractTableModel):
    """Базовый класс для всех моделей таблиц."""
    def __init__(self, headers, data_list):
        super().__init__()
        self._headers = headers
        self._data = data_list

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._headers[section]
        return None

class GroupTableModel(BaseTableModel):
    def __init__(self, groups):
        data = [[g.id, g.name] for g in groups]
        super().__init__(["ID", "Название группы"], data)

class StudentTableModel(BaseTableModel):
    def __init__(self, students):
        # Добавляем название группы для наглядности
        data = []
        for s in students:
            group_name = next((g.name for g in groups if g.id == s.group_id), "Неизвестно")
            data.append([s.id, s.last_name, s.first_name, group_name])
        super().__init__(["ID", "Фамилия", "Имя", "Группа"], data)

class SubjectTableModel(BaseTableModel):
    def __init__(self, subjects):
        data = [[s.id, s.name] for s in subjects]
        super().__init__(["ID", "Название предмета"], data)

class GradeTableModel(BaseTableModel):
    def __init__(self, grades):
        data = []
        for g in grades:
            student = next((s for s in students if s.id == g.student_id), None)
            subject = next((s for s in subjects if s.id == g.subject_id), None)
            student_name = f"{student.last_name} {student.first_name}" if student else "Неизвестно"
            subject_name = subject.name if subject else "Неизвестно"
            data.append([g.id, student_name, subject_name, g.grade, g.date.toString("dd.MM.yyyy")])
        super().__init__(["ID", "Студент", "Предмет", "Оценка", "Дата"], data)

# ---------- Вкладки для управления ----------
class GroupsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        # Поле ввода и кнопка добавления
        input_layout = QHBoxLayout()
        self.group_name_edit = QLineEdit()
        self.group_name_edit.setPlaceholderText("Название группы")
        self.add_button = QPushButton("Добавить группу")
        self.add_button.clicked.connect(self.add_group)
        input_layout.addWidget(self.group_name_edit)
        input_layout.addWidget(self.add_button)
        self.layout.addLayout(input_layout)

        # Таблица групп
        self.table_view = QTableView()
        self.layout.addWidget(self.table_view)

        self.refresh_table()

    def refresh_table(self):
        self.model = GroupTableModel(groups)
        self.table_view.setModel(self.model)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def add_group(self):
        global next_group_id
        name = self.group_name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Сеньёр будьте добры и снизойдите до заполнения названия группы")
            return
        groups.append(Group(id=next_group_id, name=name))
        next_group_id += 1
        self.group_name_edit.clear()
        self.refresh_table()

class StudentsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        # Форма добавления
        form_group = QGroupBox("Добавить студента")
        form_layout = QFormLayout()

        self.last_name_edit = QLineEdit()
        self.first_name_edit = QLineEdit()
        self.group_combo = QComboBox()
        self.update_group_combo()

        form_layout.addRow("Фамилия:", self.last_name_edit)
        form_layout.addRow("Имя:", self.first_name_edit)
        form_layout.addRow("Группа:", self.group_combo)

        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_student)
        form_layout.addRow(self.add_button)

        form_group.setLayout(form_layout)
        self.layout.addWidget(form_group)

        # Таблица студентов
        self.table_view = QTableView()
        self.layout.addWidget(self.table_view)

        self.refresh_table()

    def update_group_combo(self):
        self.group_combo.clear()
        for g in groups:
            self.group_combo.addItem(g.name, g.id)

    def refresh_table(self):
        self.model = StudentTableModel(students)
        self.table_view.setModel(self.model)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def add_student(self):
        global next_student_id
        last = self.last_name_edit.text().strip()
        first = self.first_name_edit.text().strip()
        if not last or not first:
            QMessageBox.warning(self, "Ошибка", "Заполни фамилию и имя")
            return
        if self.group_combo.count() == 0:
            QMessageBox.warning(self, "Ошибка", "Сначала добавьте хотя бы одну группу ;)")
            return
        group_id = self.group_combo.currentData()
        students.append(Student(id=next_student_id, last_name=last, first_name=first, group_id=group_id))
        next_student_id += 1
        self.last_name_edit.clear()
        self.first_name_edit.clear()
        self.refresh_table()

class SubjectsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        input_layout = QHBoxLayout()
        self.subject_name_edit = QLineEdit()
        self.subject_name_edit.setPlaceholderText("Название предмета")
        self.add_button = QPushButton("Добавить предмет")
        self.add_button.clicked.connect(self.add_subject)
        input_layout.addWidget(self.subject_name_edit)
        input_layout.addWidget(self.add_button)
        self.layout.addLayout(input_layout)

        self.table_view = QTableView()
        self.layout.addWidget(self.table_view)

        self.refresh_table()

    def refresh_table(self):
        self.model = SubjectTableModel(subjects)
        self.table_view.setModel(self.model)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def add_subject(self):
        global next_subject_id
        name = self.subject_name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "не введено название предмета")
            return
        subjects.append(Subject(id=next_subject_id, name=name))
        next_subject_id += 1
        self.subject_name_edit.clear()
        self.refresh_table()

class GradesTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        # Форма добавления оценки
        form_group = QGroupBox("Выставить оценку")
        form_layout = QFormLayout()

        self.student_combo = QComboBox()
        self.subject_combo = QComboBox()
        self.grade_edit = QLineEdit()
        self.grade_edit.setPlaceholderText("2-5")
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)

        self.update_combos()

        form_layout.addRow("Студент:", self.student_combo)
        form_layout.addRow("Предмет:", self.subject_combo)
        form_layout.addRow("Оценка:", self.grade_edit)
        form_layout.addRow("Дата:", self.date_edit)

        self.add_button = QPushButton("Добавить оценку")
        self.add_button.clicked.connect(self.add_grade)
        form_layout.addRow(self.add_button)

        form_group.setLayout(form_layout)
        self.layout.addWidget(form_group)

        # Таблица оценок
        self.table_view = QTableView()
        self.layout.addWidget(self.table_view)

        self.refresh_table()

    def update_combos(self):
        self.student_combo.clear()
        for s in students:
            self.student_combo.addItem(f"{s.last_name} {s.first_name}", s.id)

        self.subject_combo.clear()
        for sub in subjects:
            self.subject_combo.addItem(sub.name, sub.id)

    def refresh_table(self):
        self.model = GradeTableModel(grades)
        self.table_view.setModel(self.model)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def add_grade(self):
        global next_grade_id
        if self.student_combo.count() == 0 or self.subject_combo.count() == 0:
            QMessageBox.warning(self, "Ошибка", "Сначала добавьте студентов и предметы")
            return

        try:
            grade_val = int(self.grade_edit.text().strip())
            if grade_val < 2 or grade_val > 5:
                raise ValueError
        except:
            QMessageBox.warning(self, "Ошибка", "Оценка должна быть целым числом от 2 до 5")
            return

        student_id = self.student_combo.currentData()
        subject_id = self.subject_combo.currentData()
        date = self.date_edit.date()

        grades.append(Grade(id=next_grade_id, student_id=student_id, subject_id=subject_id,
                            grade=grade_val, date=date))
        next_grade_id += 1
        self.grade_edit.clear()
        self.refresh_table()

# ---------- Главное окно ----------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Учет успеваемости студентов")
        self.setMinimumSize(800, 600)

        tabs = QTabWidget()
        tabs.addTab(GroupsTab(), "Группы")
        tabs.addTab(StudentsTab(), "Студенты")
        tabs.addTab(SubjectsTab(), "Предметы")
        tabs.addTab(GradesTab(), "Журнал оценок")

        self.setCentralWidget(tabs)

# ---------- Точка входа ----------
if __name__ == "__main__":
    # Для теста добавим немного начальных данных
    groups.append(Group(id=next_group_id, name="ИС-110"))
    next_group_id += 1
    groups.append(Group(id=next_group_id, name="ПИ-220"))
    next_group_id += 1

    students.append(Student(id=next_student_id, last_name="Питт", first_name="Брэд", group_id=1))
    next_student_id += 1
    students.append(Student(id=next_student_id, last_name="Шварцнеггер", first_name="Арнольд", group_id=1))
    next_student_id += 1
    students.append(Student(id=next_student_id, last_name="Вшивков", first_name="Дмитрий", group_id=2))
    next_student_id += 1
    students.append(Student(id=next_student_id, last_name="Лопес", first_name="Дженнифер", group_id=2))
    next_student_id += 1

    subjects.append(Subject(id=next_subject_id, name="Кайфология"))
    next_subject_id += 1
    subjects.append(Subject(id=next_subject_id, name="Исскуство сражения на пальцах"))
    next_subject_id += 1

    grades.append(Grade(id=next_grade_id, student_id=1, subject_id=1, grade=5, date=QDate.currentDate()))
    next_grade_id += 1
    grades.append(Grade(id=next_grade_id, student_id=2, subject_id=1, grade=4, date=QDate.currentDate()))
    next_grade_id += 1

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())