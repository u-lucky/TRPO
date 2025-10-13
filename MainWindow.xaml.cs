using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace ISwearItsNoAi
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        private void OpenTimeTracking_Click(object sender, RoutedEventArgs e)
        {
            TimeTrackingW window = new TimeTrackingW();
            window.Owner = this;
            window.Show();
        }

        private void OpenLibrary_Click(object sender, RoutedEventArgs e)
        {
            LibraryW window = new LibraryW();
            window.Owner = this;
            window.Show();
        }

        private void OpenTravel_Click(object sender, RoutedEventArgs e)
        {
            TravelW window = new TravelW();
            window.Owner = this;
            window.Show();
        }

        private void OpenAccounting_Click(object sender, RoutedEventArgs e)
        {
            MoneyAccountW window = new MoneyAccountW();
            window.Owner = this;
            window.Show();
        }
    }
}