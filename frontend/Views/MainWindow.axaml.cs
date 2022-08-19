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

        private void ShowHelpDialog(InteractionContext<bool, Window> context) {
            var helpDialog = new HelpDialogWindow();
            context.SetOutput(helpDialog);
            helpDialog.ShowDialog(this);
        }
        
        private void ShowSyncDialog(InteractionContext<bool, Window> context) {
            var syncDialog = new SyncDialogWindow();
            context.SetOutput(syncDialog);
            syncDialog.ShowDialog(this);
        }
    }
}
