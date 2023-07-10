# retention-issues
Progetto per la tesi: **Analisi di retention issue in progetti Open Source in Github**   

## Indice
 - [Introduzione](#Introduzione)
 - [Requisiti fondamentali](#Requisiti-fondamentali)
 - [File](#File)
 - [Funzioni utilizzate](#Funzioni-utilizzate)
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
* `tqdm`: usato per vedere la barra di avanzamento durante l'esecuzione di un ciclo;
* `json`: usato per la manipolazione dei file json;
* `csv`: usato per la manipolazione dei file csv;
* `time`: usato per lavorare con la gestione dei tempi;
* `re`: usato per utilizzare le espressioni regolari;
* `datetime`: usato per utilizzare le date;
* `torch`: usato per l'addestramento dei modelli;
* `openpyxl`: usato per leggere e scrivere file Excel; 

Per installare le librerie eseguire il comando  
`pip install -r requirements.txt`  
oppure  
`pip install <nome libreria>` sul terminale.  
oppure  
`python -m pip install <nome libreria>` sul terminale. 

Scaricare ***MongoDB*** cliccando sul [link](https://www.mongodb.com/try/download/community).  
Una volta scaricato bisogna stabilire una connessione (di default: *mongodb://localhost:27017*)  
Stabilita la connessione bisognerà:  
  * Cliccare sul tasto "**+**" alla destra della scritta **Databases**;    
  * Inserire il **Database name** e il **Collection name** e poi cliccare il tasto **Create Database**;    
  * Andare sulla collezione appena creata e cliccare il tasto **Import Data**;    
  * Selezionare il file JSON **DB** presente nella cartella **Database** e cliccare il tasto **JSON**;   
  * Cliccare il tasto **Import**;

  Adesso il Database è correttamente importato su **MongoDB**.  
 
## File  
 **Indice**  
 - [utilities.py](#utilitiespy)
 - [datasetRetentionIssue.py](#datasetretentionissuepy)
 - [extractUser.py](#extractuserpy)
 - [extractActiveUsers.py](#extractactiveuserspy)
 - [oneYearIssue.py](#oneyearissuepy)
 
### **`utilities.py`**   
  Contiene delle funzioni basilari:  
   * **[`get_access_token()`](#get_access_token)**: restituisce il *personal access token*;
   * **[`extract_owner(html_url)`](#extract_owner)**: dato l'url della issue restituisce tramite le espressioni regolari il proprietario della repository;
   * **[`extract_name(html_url)`](#extract_name)**: dato l'url della issue restituisce tramite le espressioni regolari il nome della repository;
   * **[`extract_repository(html_url)`](#extract_repository)**: dato l'url della issue restituisce tramite le espressioni regolari il nome completo della repository;
   * **[`extract_number(html_url)`](#extract_number)**: dato l'url della issue restituisce tramite le espressioni regolari il numero della issue;  
### **`datasetRetentionIssue.py`**  
  Fatto questo viene stabilita una connessione al database.  
  Viene creata la variabile `result` contente l'url di ciascuna issue presente nel database.  
  Viene chiamata la funzione [`create_dataset(result)`](#create_dataset) che crea il file `retentionIssue.csv` contente l'url di ciascuna issue presente nel database.
### **extractUser.py**  
  Legge il file `Dataset/retentionIssue.csv`
### **extractActiveUsers.py**
 Viene iterato il dataset `users.csv` e per ciascun utente si ricava: 
  * `user` = nome dell'utente;
  * `issue_url` = url della prima issue fatta dall'utente;
  * `repository` = nome della repository;  

 nella variabile `prs` con la funzione [`extract_prs(user, repository)`](#extract_prs) vengono salvate tutte le pull request fatte dall'utente;  
 nella variabile `issues` con la funzione [`extract_issues(user, repository, issue_url, prs)`](#extract_issues) vengono salvate tutte le issue fatte dall'utente;  
 se il numero delle issue è maggiore di 1: l'utente verrà salvato nel file `activeUsers.json` con:  
  * *id* = nome dell'utente 
  * *issues* = lista di tutte le issue fatte dall'utente.  
  
### **oneYearIssue.py**
 Viene iterato il file `activeUsers.json` e per ogni utente si ricava:  
  * l'url della good first issue messo nella variabile `good_first_issue`;
  * proprietario della repository con [`utilities.extract_owner(good_first_issue)`](#extract_owner) ;    
  * nome della repository con [`utilities.extract_name(good_first_issue)`](#extract_name);  
  * nome completo della repository con [`utilities.extract_repository(good_first_issue)`](#extract_repository);
  * numero della issue con [`utilities.extract_number(good_first_issue)`](#extract_number); 
  * tutte le issue fatte dall'utente inserite nella lista `issue_utente`;
  * tutte le issue della repository dalla data di chiusura della `good_first_issue` fino all'anno successivo;  
  
 Le issue della repository sono salvate nella lista `issue_repo` e sono ricavate dalla funzione [`extract_repo_issues(repository, number)`](#extract_repo_issues).  
 Viene creato il dizionario `user_issues` contenente:
  * *good-first_issue* = `good_first_issue`;
  * *retention-issue-candidate* = `issue_utente`;
  * *issue-di-progetto* = `issue_repo`;  
  
 Il dizionario `user_issue` viene salvato nel file `{user}--{owner}.{name}.json`.  
  
## Funzioni Utilizzate
### `get_access_token()`
* **Risultato**  
Restituisce il *personal access token* utile per l'accesso su Github.
### `extract_owner()`
* **Parametri**  
  * `html_url` = url della issue
* **Funzione**  
Con le espressioni regolari si ricava il proprietario della repository.
* **Risultato**  
`owner` = proprietario della repository.
### `extract_name()`
* **Parametri**  
  * `html_url` = url della issue
* **Funzione**  
Con le espressioni regolari si ricava il nome della repository.
* **Risultato**  
`name` = nome della repository.
### `extract_repository()`
* **Parametri**  
  * `html_url` = url della issue
* **Funzione**  
Con le espressioni regolari si ricava il nome completo della repository.
* **Risultato**  
`repository` = nome completo della repository.
### `extract_number()`
* **Parametri**  
  * `html_url` = url della issue
* **Funzione**  
Con le espressioni regolari si ricava il numero della issue.
* **Risultato**  
`number` = numero della issue.
### `create_dataset()`
* **Parametri**  
  * `result` = url di tutte le good first issue
* **Funzione**  
Viene creato un DataFrame vuoto chiamato `df_project`.  
Per ogni issue presente nella lista `result`:  
  - Aggiunge una nuova riga al DataFrame `df_project` con l'url della issue.  
  
  Esporta il DataFrame in un file CSV chiamato `retentionIssues.csv`
* **Risultato**  
`retentionIssues.csv` = file CSV contente l'url di tutte le good first issue.
### `extract_prs_list()`
* **Parametri**  
  * `owner` = proprietario della repository;
  * `name` = nome della repository;
  * `numebr` = numero della issue;
* **Funzione**  
Viene stabilita la query con le GraphQL che si ricava le pull request associate alla issue.  
Viene definito il dizionario delle intestazioni per la richiesta API.  
Viene eseguita la richiesta API GraphQL.  
Se il codice della risposta è 200 (risposta affermativa) vengono salvate nella variabile `prs_list` tutte le pull request associate alla issue.
* **Risultato**  
`prs_list` = tutte le pull request associate alla issue.
### `extract_pr_owner()`
* **Parametri**  
  * `repository` = nome completo della repository;
  * `pr` = numero della pull request;
* **Funzione**  
Fa l'accesso a GitHub con il personal access token.  
Recupera l'oggetto Repository corrispondente al nome fornito.  
Recupera l'oggetto PullRequest corrispondente al numero fornito.
Recupera il proprietario della PullRequest e lo inserisce nella variabile `pr_owner`.
* **Risultato**  
`pr_owner` = proprietario della PullRequest.
### `extract_first_issue()`
* **Parametri**  
  * `repository` = nome completo della repository;
  * `pr_owner` = proprietario della PullRequest;
  * `pr` = numero della PullRequest;
  * `issue_url` = url della issue;
* **Funzione**  
Recupera l'oggetto Repository corrispondente al nome fornito.
Ricava tutti i commit del `pr_owner` nella Repository.  
Ottiene il primo commit del `pr_owner` nella Repository.  
Ricava la PullRequest associata al primo commit.  
Estrae l'URL della prima PullRequest trovata (se presente).
Controlla se il numero della PullRequest corrisponde a `pr`.  
Se corrispondono:  
Lettura del file CSV contenente i dati degli utenti e creazione di un DataFrame.  
Aggiunta delle informazioni dell'autore al DataFrame.  
Scrittura del DataFrame nel file CSV `users.csv`.
* **Risultato**  
`users.csv` = file contente nome e url della prima issue degli utenti che come prima issue nella Repository hanno fatto la good first issue.
### `extract_prs()`
* **Parametri**  
  * `user` = nome dell'utente;
  * `repository` = nome completo della repository;
* **Funzione**  
Recupera l'oggetto Repository corrispondente al nome fornito.  
Ricava tutti i commit di `user` nella Repository.  
Per ogni commit ricava la PullRequest associata.  
Inserisci tutte le PullRequest nella lista `prs`.
* **Risultato**  
`prs` = lista di tutte le PullRequest di `user`.
### `extract_issues()`
* **Parametri**  
  * `user` = nome dell'utente;
  * `repository` = nome completo della repository;
  * `prs` = lista di tutte le PullRequest di `user`;
* **Funzione**  
Recupera l'oggetto Repository corrispondente al nome fornito.  
Per ogni numero di  PullRequest in `prs`:  
Recupera l'oggetto PullRequest corrispondente al numero fornito.  
Controlla se l'autore della PullRequest corrisponde a `user`.  
Costruisce l'URL della pagina della PullRequest.  
Facciamo una richiesta HTTP per la pagina del pull request.  
Analizziamo il contenuto HTML della pagina del pull request con BeautifulSoup.  
Estraiamo parte dell'URL delle issue dal repository.  
Troviamo tutti i tag "a" nella pagina HTML della PullRequest.  
Per ogni tag "a" estraiamo il link presente nell'href.  
Se il link corrisponde al link di una issue salviamo il numero della issue. 
Recupera l'oggetto Issue corrispondente al numero appena trovato.
Inesrisci tutti gli url delle issue nella lista `issue_list`.
* **Risultato**  
`issue_list` = url di tutte le issue fatte da `user`.
### `extract_repo_issues()`
* **Parametri**  
  * `repository` = nome completo della repository;
  * `numer` = numero della issue;
* **Funzione**  
Recupera l'oggetto Repository corrispondente al nome fornito.
Recupera l'oggetto Issue corrispondente al numero fornito.
Estrae la data di chiusura della Issue e la salva nella variabile `data_inizio`.  
Calcola un delta pari a 365 giorni.  
Calcola `data_fine` aggiungendo a `data_inizio` il delta.  
Ricava tutte le issue della repository a partire dalla `data_inizio` fino alla `data_fine`.  
Salva queste issue nella variabile `issue_repo`.
* **Risultato**  
`issue_repo` = issue della repository a partire dalla `data_inizio` fino alla `data_fine`.

## Tabella
| **Nome File** | **Quantità** |
|-----------|---------|
| retentionIssue.csv | 354648 |  
| users.csv | 11167 |
| ActiveUsers.json|  4120  |  
