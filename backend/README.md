# Parthenon Backend

## Layers
- API (**CoreAPI**, **CA**) (Logic layer for API)
  - `Parthenon_Encrypted_Socket_API` (Proprietary Encrypted Berkeley Sockets frontend for API)
- Validation (**Static Validation**, **SV**) (Validation layer)
  - Converts raw data to `struct/` object.
- Ingestion Engine (**IE**) (Fetches data from upstream data source)
  - FTP_CSV (Ingestion engine for CSV file stored on FTP Server)
- Data Storage Engine (**DSE**) (Stores `struct/` data in backend format)
  - `Parthenon_DSEI` (Proprietary Data Storage Engine Implementation)

## Synchronization Steps
1. API frontend calls CoreAPI `#synchronize`.
2. Ingestion Engine Implementation (**IEI**), in this case `FTP_CSV`, connects to server and downloads raw data.
3. IEI passes data to Core Validation (**CV**) to check the data and CV returns structured objects.
4. Structured objects are passed to CoreAPI
5. CoreAPI passes structured objects to Data Storage Engine Implementation (**DSEI**) which refreshes its indexes and stores the new data.
