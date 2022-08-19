using Avalonia.Controls;
using ReactiveUI;
using System;
using System.Reactive.Linq;
using System.Threading.Tasks;
using System.Windows.Input;

namespace Parthenon.ViewModels {

    public class MainWindowViewModel : ViewModelBase {
        public ICommand HelpButtonClickCommand { get; }
        public Interaction<bool, Window> ShowHelpDialog { get; }

        public ICommand SyncButtonClickCommand { get; }
        public Interaction<bool, Window> ShowSyncDialog { get; }
        

        private bool _useDateRange = false;
        public bool UseDateRange
        {
            get => _useDateRange;
            set
            {
                this.RaiseAndSetIfChanged(ref _useDateRange, value);
                this.RaisePropertyChanged(nameof(UseDateRangePrompt));
            }
        }

        public string UseDateRangePrompt {
            get => _useDateRange
                ? "Only data between these dates will be displayed."
                : "All data will be displayed.";
        }


        public MainWindowViewModel() {
            ShowHelpDialog = new Interaction<bool, Window>();
            HelpButtonClickCommand = ReactiveCommand.Create(async () => {
                await ShowHelpDialog.Handle(false);
            });

            ShowSyncDialog = new Interaction<bool, Window>();
            SyncButtonClickCommand = ReactiveCommand.Create(async () => {
                var subscription = ShowSyncDialog.Handle(false).Subscribe();
                // Console.WriteLine("subscribed");
                await Task.Delay(2000);
                // Console.WriteLine("delayed");
                // subscription.Dispose();
            });
        }

    }


}
