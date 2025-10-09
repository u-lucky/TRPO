using System;
using System.Collections.Generic;
using System.Windows;
using System.Windows.Controls;

namespace QuoteMaster
{
    public partial class MainWindow : Window
    {
        // Коллекция цитат
        private List<Quote> quotes;
        private Random random;

        public MainWindow()
        {
            InitializeComponent(); // Эта строка должна быть первой в конструкторе
            random = new Random();
            InitializeQuotes();
            ShowRandomQuote();
        }

        // Инициализация коллекции цитат
        private void InitializeQuotes()
        {
            quotes = new List<Quote>
            {
                new Quote("Запомни: всего одна ошибка – и ты ошибся...", "Стетхем Джейсон"),
                new Quote("Делай, как надо. Как не надо, не делай.", "Стетхем Джейсон"),
                new Quote("Не будьте эгоистами, в первую очередь думайте о себе!", "Джейсон Стетхем"),
                new Quote("Слово — не воробей. Вообще ничто не воробей, кроме самого воробья.", "Джейсон Стетхем"),
                new Quote("Если я не вернусь через пять минут, просто подождите дольше.", "Эйс Вентура"),
                new Quote("Не будьте такими скромными — вы не настолько хороши", "Голда Меир "),
                new Quote("Я помню это так, будто это было вчера. Хотя, если честно, вчера я помню не очень хорошо", "Дори"),
                new Quote("Я разговариваю сам с собой, потому что только мои ответы меня устраивают.", "Джордж Карлин"),
                new Quote("Прежде чем жениться на ком-то, сначала заставьте его поработать за компьютером с медленным интернетом — так вы узнаете его настоящего.", "Уилл Феррелл"),
                new Quote("Судя по карте, мы проехали целых десять сантиметров.", "Гарри Данн"),
                new Quote("Злые вы, уйду я от вас.", "Три Лягушонка"),
                new Quote("Если тебе где-то не рады в рваных носках, то и в целых туда идти не стоит.", "Джейсон Стейтхем"),
                new Quote("Работа не волк. Никто не волк. Только волк волк.", "Джейсон Стейтхем"),
                new Quote("Если закрыть глаза, становится темно.", "Джейсон Стейтхем"),
                new Quote("Тут — это вам не там.", "Джейсон Стейтхем")
            };
        }

        // Показать случайную цитату
        private void ShowRandomQuote()
        {
            if (quotes.Count > 0)
            {
                int index = random.Next(quotes.Count);
                quoteText.Text = $"\"{quotes[index].Text}\"";
                authorText.Text = $"— {quotes[index].Author}";
            }
        }

        // Обработчик кнопки "Новая цитата"
        private void NewQuoteButton_Click(object sender, RoutedEventArgs e)
        {
            ShowRandomQuote();
        }

        // Обработчик кнопки "Копировать"
        private void CopyButton_Click(object sender, RoutedEventArgs e)
        {
            string fullQuote = $"{quoteText.Text} {authorText.Text}";
            Clipboard.SetText(fullQuote);
            MessageBox.Show("Цитата скопирована в буфер обмена!", "Успех",
                          MessageBoxButton.OK, MessageBoxImage.Information);
        }

        // Обработчик кнопки "Выход"
        private void ExitButton_Click(object sender, RoutedEventArgs e)
        {
            Application.Current.Shutdown();
        }
    }

    // Класс для хранения цитат
    public class Quote
    {
        public string Text { get; set; }
        public string Author { get; set; }

        public Quote(string text, string author)
        {
            Text = text;
            Author = author;
        }
    }
}