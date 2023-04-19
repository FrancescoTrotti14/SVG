# retention-issues
Progetto per la tesi: **Creazione di un bot per i neo contributori di progetti open source in Github**   

## Indice
 - [Introduzione](#Introduzione)
 - [Requisiti fondamentali](#Requisiti-fondamentali)
 - [File](#File)
 - [Funzioni utilizzate](#Funzioni-utilizzate)
 - [Cartelle](#cartelle)
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
 - [datasetRetentionIssue.py](#datasetretentionissuepy)
 - [extractUser.py](#extractuserpy)
 - [extractActiveUsers.py](#extractactiveuserspy)
 - [one_year_issue.py](#one_year_issuepy)
 
### **`utilities.py`**   
  Contiene delle funzioni basilari:  
   * **[`get_access_token()`](#get_access_token)**: restituisce il *personal access token*;
   * **[`extract_owner(html_url)`](#extract_owner)**: dato l'url della issue restituisce tramite le espressioni regolari il proprietario della repository;
   * **[`extract_name(html_url)`](#extract_name)**: dato l'url della issue restituisce tramite le espressioni regolari il nome della repository;
   * **[`extract_repository(html_url)`](#extract_repository)**: dato l'url della issue restituisce tramite le espressioni regolari il nome completo della repository;
   * **[`extract_number(html_url)`](#extract_number)**: dato l'url della issue restituisce tramite le espressioni regolari il numero della issue;  
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
  Viene creata la variabile `result` contente l'url di ciascuna issue presente nel database.  
  Viene chiamata la funzione [`create_dataset(result)`](#create_dataset) che crea il file `retentionIssue.csv` contente l'url di ciascuna issue presente nel database.
### **extractUser.py**  
  Viene iterato il dataset `retentionnIssue.csv` e per ogni issue presente nel database si ricava:  
   * proprietario della repository con [`utilities.extract_owner(html_url)`](#extract_owner) ;    
   * nome della repository con [`utilities.extract_name(html_url)`](#extract_name);  
   * numero della issue con [`utilities.extract_number(html_url)`](#extract_number);  
   * nome completo della repository ;

 Vengono prese tutte le pull request associate alla issue e salvate nella variabile `prs_list` con la funzione [`extract_prs_list(owner, name, number)`](#extract_prs_list).  
 Se la variabile `prs_list` non è vuota: per ogni pull request in `prs_list` viene estratto il proprietario della pull request con la funzione [`extract_pr_owner(repository)`](#extract_pr_owner) e inserito nella variabile `pr_owner`.  
 Se la variabile `pr_owner` non è vuota viene chiamata la funzione [`extract_first_issue(repository, pr_owner, pr, issue_url)`](#extract_first_issue) che costruirà il dataset `users.csv` contente il nome e l'url della prima issue fatta nella repository.  
### **extractActiveUsers.py**
 Viene iterato il dataset `users.csv` e per ciascun utente si ricava: 
  * `user` = nome dell'utente;
  * `issue_url` = url della prima issue fatta dall'utente;
  * `repository` = nome della repository;  

 nella variabile `prs` con la funzione [`extract_prs(user, repository)`](#extract_prs) vengono salvate tutte le pull request fatte dall'utente;  
 nella variabile `issues` con la funzione [`extract_issues(user, repository, issue_url, prs)`](#extract_issues) vengono salvate tutte le issue fatte dall'utente;  
 se il numero delle issue è maggiore di 1: l'utente verrà salvato nel file `activeUsers.json` con *id* = nome dell'utente e *issues* = lista di tutte le issue fatte dall'utente.  
### **one_year_issue.py**
  

## Funzioni Utilizzate
### `get_access_token()`
### `extract_owner()`
### `extract_name()`
### `extract_repository()`
### `extract_number()`
### `create_dataset()`
### `extract_prs_list()`
### `extract_pr_owner()`
### `extract_first_issue()`
### `extract_prs()`
### `extract_issues()`

## Cartelle

## Tabella
| **Nome File** | **Quantità** |
|-----------|---------|
| retentionIssue.csv | 354648 |  
| users.csv | 11167 |
| ActiveUsers.json|  4120  |  
