using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows;
using System.Windows.Controls;

namespace ISwearItsNoAi
{
    public partial class TimeTrackingW : Window
    {
        private List<Employee> employees = new List<Employee>();
        private List<TimeRecord> timeRecords = new List<TimeRecord>();

        public TimeTrackingW()
        {
            InitializeComponent();
            InitializeData();
            LoadEmployees();
            LoadTimeRecords();
        }

        private void InitializeData()
        {
            // Тестовые данные
            employees.AddRange(new[]
            {
                new Employee { Id = 1, Name = "Иванов И.И." },
                new Employee { Id = 2, Name = "Петров П.П." },
                new Employee { Id = 3, Name = "Сидоров С.С." }
            });

            // Устанавливаем даты по умолчанию
            dpStartDate.SelectedDate = DateTime.Today.AddDays(-7);
            dpEndDate.SelectedDate = DateTime.Today;
        }

        private void LoadEmployees()
        {
            cmbEmployees.ItemsSource = employees;
            cmbEmployees.DisplayMemberPath = "Name";
            if (cmbEmployees.Items.Count > 0)
                cmbEmployees.SelectedIndex = 0;
        }

        private void LoadTimeRecords()
        {
            // Здесь будет загрузка из базы данных
            // Пока используем тестовые данные
            timeRecords.Clear();

            // Обновляем DataGrid
            dgTimeRecords.ItemsSource = null;
            dgTimeRecords.ItemsSource = timeRecords;

            tbStatus.Text = $"Загружено записей: {timeRecords.Count}";
        }

        private void BtnArrival_Click(object sender, RoutedEventArgs e)
        {
            if (cmbEmployees.SelectedItem is Employee employee)
            {
                var record = new TimeRecord
                {
                    EmployeeId = employee.Id,
                    EmployeeName = employee.Name,
                    Date = DateTime.Today,
                    ArrivalTime = DateTime.Now.TimeOfDay
                };

                timeRecords.Add(record);
                LoadTimeRecords();
                tbStatus.Text = $"Зафиксирован приход: {employee.Name} в {record.ArrivalTime}";
            }
        }

        private void BtnDeparture_Click(object sender, RoutedEventArgs e)
        {
            if (cmbEmployees.SelectedItem is Employee employee)
            {
                var todayRecord = timeRecords.FirstOrDefault(r =>
                    r.EmployeeId == employee.Id &&
                    r.Date.Date == DateTime.Today);

                if (todayRecord != null)
                {
                    todayRecord.DepartureTime = DateTime.Now.TimeOfDay;
                    LoadTimeRecords();
                    tbStatus.Text = $"Зафиксирован уход: {employee.Name} в {todayRecord.DepartureTime}";
                }
                else
                {
                    MessageBox.Show("Сначала зафиксируйте приход сотрудника");
                }
            }
        }

        private void BtnFilter_Click(object sender, RoutedEventArgs e)
        {
            // Здесь будет фильтрация по датам
            LoadTimeRecords();
            tbStatus.Text = "Применены фильтры";
        }
    }

    // Классы данных
    public class Employee
    {
        public int Id { get; set; }
        public string Name { get; set; }
    }

    public class TimeRecord
    {
        public int EmployeeId { get; set; }
        public string EmployeeName { get; set; }
        public DateTime Date { get; set; }
        public TimeSpan ArrivalTime { get; set; }
        public TimeSpan DepartureTime { get; set; }
        public string WorkedHours
        {
            get
            {
                if (ArrivalTime != TimeSpan.Zero && DepartureTime != TimeSpan.Zero)
                {
                    var worked = DepartureTime - ArrivalTime;
                    return $"{worked.Hours:00}:{worked.Minutes:00}";
                }
                return "-";
            }
        }
    }
}