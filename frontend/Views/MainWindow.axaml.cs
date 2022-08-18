using Avalonia.Collections;
using Avalonia.Controls;
using Avalonia.ReactiveUI;
using Parthenon.Models;
using Parthenon.ViewModels;
using ReactiveUI;
using System.Collections.Generic;
using System.Reactive;
using System.Threading.Tasks;

namespace Parthenon.Views {
    public partial class MainWindow : ReactiveWindow<MainWindowViewModel> {
        private List<BatchEntryModel> _batchEntries = new List<BatchEntryModel> {
            new BatchEntryModel(69, "23:00:00", "0.696", "0.696", "0.696", "0.696", "0.696", "0.696", "0.696", "0.696", "0.696", "0.696"),
            new BatchEntryModel(70, "23:00:00", "0.696", "0.696", "0.696", "0.696", "0.696", "0.696", "0.696", "0.696", "0.696", "0.696"),
            new BatchEntryModel(71, "23:00:00", "0.696", "0.696", "0.696", "0.696", "0.696", "0.696", "0.696", "0.696", "0.696", "0.696")
        };

        public MainWindow() {
            InitializeComponent();

            this.WhenActivated(d => d(ViewModel!.ShowHelpDialog.RegisterHandler(ShowHelpDialog)));
            this.WhenActivated(d => d(ViewModel!.ShowSyncDialog.RegisterHandler(ShowSyncDialog)));

            var batchEntriesView = new DataGridCollectionView(_batchEntries);
            BatchEntriesDataGrid.Items = batchEntriesView;
    }

        private async Task ShowHelpDialog(InteractionContext<bool, Unit> context) {
            var helpDialog = new HelpDialogWindow();
            await helpDialog.ShowDialog(this);
        }
        private async Task ShowSyncDialog(InteractionContext<bool, Unit> context) {
            var syncDialog = new SyncDialogWindow();
            await syncDialog.ShowDialog(this);
        }
    }
}
