using Avalonia.Collections;
using Parthenon.Models;
using ReactiveUI;
using System.Collections.Generic;
using System.Reactive;
using System.Reactive.Linq;
using System.Windows.Input;

namespace Parthenon.ViewModels {

    public class MainWindowViewModel : ViewModelBase {
        public ICommand HelpButtonClickCommand { get; }
        public Interaction<bool, Unit> ShowHelpDialog { get; }

        public ICommand SyncButtonClickCommand { get; }
        public Interaction<bool, Unit> ShowSyncDialog { get; }
        

        private bool _useDateRange = false;
        public bool UseDateRange { get => _useDateRange; set => this.RaiseAndSetIfChanged(ref _useDateRange, value); }


        public MainWindowViewModel() {
            ShowHelpDialog = new Interaction<bool, Unit>();
            HelpButtonClickCommand = ReactiveCommand.Create(async () => {
                await ShowHelpDialog.Handle(false);
            });

            ShowSyncDialog = new Interaction<bool, Unit>();
            SyncButtonClickCommand = ReactiveCommand.Create(async () => {
                await ShowSyncDialog.Handle(false);
            });
        }

    }


}
