using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Parthenon.Models {
    public class BatchEntryModel : INotifyPropertyChanged {

        private int _batchId;
        public int BatchId { get => _batchId; set { _batchId = value; OnPropertyChanged(nameof(BatchId)); } }

        private string _timestamp;
        public string Timestamp { get => _timestamp; }

        private string _reading1;
        public string Reading1 { get => _reading1; set { _reading1 = value; OnPropertyChanged(nameof(Reading1)); } }

        private string _reading2;
        public string Reading2 { get => _reading2; set { _reading2 = value; OnPropertyChanged(nameof(Reading2)); } }

        private string _reading3;
        public string Reading3 { get => _reading3; set { _reading3 = value; OnPropertyChanged(nameof(Reading3)); } }

        private string _reading4;
        public string Reading4 { get => _reading4; set { _reading4 = value; OnPropertyChanged(nameof(Reading4)); } }

        private string _reading5;
        public string Reading5 { get => _reading5; set { _reading5 = value; OnPropertyChanged(nameof(Reading5)); } }

        private string _reading6;
        public string Reading6 { get => _reading6; set { _reading6 = value; OnPropertyChanged(nameof(Reading6)); } }

        private string _reading7;
        public string Reading7 { get => _reading7; set { _reading7 = value; OnPropertyChanged(nameof(Reading7)); } }

        private string _reading8;
        public string Reading8 { get => _reading8; set { _reading8 = value; OnPropertyChanged(nameof(Reading8)); } }

        private string _reading9;
        public string Reading9 { get => _reading9; set { _reading9 = value; OnPropertyChanged(nameof(Reading9)); } }

        private string _reading10;
        public string Reading10 { get => _reading10; set { _reading10 = value; OnPropertyChanged(nameof(Reading10)); } }

        public BatchEntryModel(int batchId, string timestamp,
                                string reading1, string reading2, string reading3, string reading4, string reading5, string reading6, string reading7, string reading8, string reading9, string reading10) {
            this._batchId = batchId;
            this._timestamp = timestamp;
            this._reading1 = reading1;
            this._reading2 = reading2;
            this._reading3 = reading3;
            this._reading4 = reading4;
            this._reading5 = reading5;
            this._reading6 = reading6;
            this._reading7 = reading7;
            this._reading8 = reading8;
            this._reading9 = reading9;
            this._reading10 = reading10;
        }

        public event PropertyChangedEventHandler? PropertyChanged;
        void OnPropertyChanged(string propertyName) {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }

    }
}
