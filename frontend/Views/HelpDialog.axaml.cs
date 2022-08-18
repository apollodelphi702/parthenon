using Avalonia;
using Avalonia.Controls;
using Avalonia.Markup.Xaml;

namespace Parthenon.Views {
    public partial class HelpDialogWindow : Window {
        public HelpDialogWindow() {
            InitializeComponent();
#if DEBUG
            this.AttachDevTools();
#endif
        }

        private void InitializeComponent() {
            AvaloniaXamlLoader.Load(this);
        }
    }
}
