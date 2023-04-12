# retention-issues
Progetto per la tesi: **Creazione di un bot per i neo contributori di progetti open source in Github**  
a cura di: **Trotti Francesco [703010]**  

## Indice
 - [Introduzione](#Introduzione)
 - [Requisiti fondamentali](#Requisiti-fondamentali)
 - [Presentazione](#Presentazione)
 - [Funzioni utilizzate](#Funzioni-utilizzate)
 - [File](#File)
 - [Tabella](#Tabella)
 
## Introduzione
L'obbiettivo di questo programma è quello di non far andar via un utente da una repository dopo che ha svolto la prima issue.  
Infatti questo programma riesce, partendo dalla prima issue svolta, a trovare una successiva issue simile a quella svolta dall'utente. Così facendo l'utente non abbandonerà la repository.  
 
## Requisiti fondamentali
Programma realizzato con il linguaggio di programmazione Python. Per eseguire il codice si rchiede un ambiente di sviluppo (ambiente di sviluppo suggerito: Visual Studio Code)  
Relativamente alle librerie esterne importate, vediamo la necessità di installare sulla macchina:
* `pandas`: usato per la manipolazione e l’analisi dei dati;
* `beautifulsoup4`: usato per richiedere la pagina html;
* `pymongo`: usato per accedere ai database;
* `pyGithub`: usato per accedere alla informazioni presenti su GitHub;
* `requests`: usato per creare vari tipi di richieste http;   

Per installare le librerie eseguire il comando  
`pip install -r requirements.txt`  
oppure  
`pip install <nome libreria>` sul terminale.  
oppure  
`python -m pip install <nome libreria>` sul terminale. 
Una volta installate le librerie eseguire il file `main.py`.
 
## File  
 **Indice**  
 - [utilities.py](#utilitiespy)
 - [datasetRetentionIssue.py](#datasetRetentionIssuepy)
 - [extractUser.py](#extractUserpy)
 
### **`utilities.py`**   
  Contiene delle funzioni basilari:  
   * **[`get_access_token()`](#get_access_token)**: restituisce il *personal access token*;
   * **`extract_owner(html_url)`**: dato l'url della issue restituisce tramite le espressioni regolari il proprietario della repository;
   * **`extract_name(html_url)`**: dato l'url della issue restituisce tramite le espressioni regolari il nome della repository;
   * **`extract_repository(html_url)`**: dato l'url della issue restituisce tramite le espressioni regolari il nome completo della repository;
   * **`extract_number(html_url)`**: dato l'url della issue restituisce tramite le espressioni regolari il numero della issue;  
### **`datasetRetentionIssue.py`**  
  Il primo passo da fare è scaricare ***MongoDB*** cliccando sul [link](https://www.mongodb.com/try/download/community).  
Una volta scaricato bisogna stabilire una connessione (di default: *mongodb://localhost:27017*)  
Stabilita la connessione bisognerà:  
  * Cliccare sul tasto "**+**" alla destra della scritta **Databases**;    
  * Inserire il **Database name** e il **Collection name** e poi cliccare il tasto **Create Database**;    
  * Andare sulla collezione appena creata e cliccare il tasto **Import Data**;    
  * Selezionare il file JSON **DB** presente nella cartella **Database** e cliccare il tasto **JSON**;   
  * Cliccare il tasto **Import**;

  Adesso il Database è correttamente importato su **MongoDB**.  
  Fatto questo viene stabilita una connessione al database.  
  Viene creata la variabile `result`  
### **extractUser.py**  
  Viene iterato il dataset `retentionnIssue.csv` e per ogni issue presente nel database si ricava:  
   * proprietario della repository con `utilities.extract_owner(html_url)` ;    
   * nome della repository con `utilities.extract_name(html_url)`;  
   * numero della issue con `utilities.extract_number(html_url)`;  
   * nome completo della repository ;  
  

## Funzioni Utilizzate
### `get_access_token()`
### `extract_owner(html_url)`
### `extract_name(html_url)`
### `extract_repository(html_url)`
### `extract_number(html_url)`

## Tabella
| **Nome File** | **Quantità** |
|-----------|---------|
| retentionIssue.csv | 354648 |  
| users.csv | 11167 |
| passiveUsers.txt | 9 |
| usersActive.csv | 11158 |
| ActiveUsers.json|  2593  | 
| ActiveUseresLabels.json |  2593  | 
