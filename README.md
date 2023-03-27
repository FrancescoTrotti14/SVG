# retention-issues
Progetto per la tesi: **Creazione di un bot per i neo contributori di progetti open source in Github**  
a cura di: **Trotti Francesco [703010]**  

## Indice
 - [Introduzione](#Funzioni-utilizzate)
 - [Requisiti fondamentali](#Requisiti-fondamentali)
 - [Presentazione](#Presentazione)
 - [Funzioni utilizzate](#Funzioni-utilizzate)
  
## Presentazione
Il programma esegue quattro fasi principali:  
* **Creazione Dataset**: nella cartella `Database` è presente il database contenete tutte le retention issues.  
Il primo passo da fare è scaricare ***MongoDB*** cliccando sul [link](https://www.mongodb.com/try/download/community).  
Una volta scaricato bisogna stabilire una connessione (di default: *mongodb://localhost:27017*)  
Stabilita la connessione bisognerà:  
  * Cliccare sul tasto "**+**" alla destra della scritta **Databases**;    
  * Inserire il **Database name** e il **Collection name** e poi cliccare il tasto **Create Database**;    
  * Andare sulla collezione appena creata e cliccare il tasto **Import Data**;    
  * Selezionare il file JSON **DB** presente nella cartella **Database** e cliccare il tasto **JSON**;   
  * Cliccare il tasto **Import**;

  Adesso il Database è correttamente importato su **MongoDB**.  
  Ora il programma chiama la funzione `create_dataset()`.  
  Grazie a questa funzione il programma creerà un dataset contenente l' ***html_url*** e il ***repository_url*** di ciascuna issue presente nel Database appena importato su **MongoDB**.  
  Il dataset in questione è presente nella cartella `Dataset` con il nome di `retention-issue.csv`

* **Estrazione utenti**: In questa fase viene analizzata ciascuna issue presente nel dataset `retention-issue.csv`.  
L'obbiettivo di questa fase è capire l'utente che ha lavorato alla issue presa in questione e capire se la issue analizzata è la **prima** issue svolta dall'utente in questa **repository**.  
Quindi per ciascuna issue bisognerà:  
  * Trovare la **pull request** che chiude l'issue grazie alla funzione `extract_pr_numbers()`;
  * Trovare il **proprietario** della **pull request** grazie alla funzione `extract pr_owner()`;  
  * Trovare tutti i **commit** fatti dall'utente nella **repository**;  
  * Controllare che il **primo committ** chiuda la **pull request** analizzata;  
  * Salvare l'**utente** nel caso si verifichi il passo precedente grazie alla funzione `extract_commit_information()`;

  Ciascun utente verrà salvato all'interno del dataset `users.csv`.  
  Il dataset `users.csv` conterrà in **name** il nome dell'utente e in **html_url** l'url della prima issue svolta nella repository.
  
* **Estrazione utenti attivi**: L'obbiettivo di questa fase è quello di estrarre gli utenti che hanno svolto almeno un'altra issue all'interno della repository.  
Il programma eliminerà dal dataset `users.csv` gli utenti che hanno svolto una sola issue nella repository, creando il dataset `users1.csv` che conterrà i probabili utenti che hanno svolta più di una issue.  
Per creare il dataset `users1.csv` per ciascun utente bisognerà:    
  *  Trovare **tutti i commit** fatti dall'utente nella repository;
  *  Trovare il numero di **commit** fatti dall'utente nella pull request che chiude la issue del dataset;
  *  Fare un confronto tra i commit nell'intera repository e i commit nella pull request;
  *  Se il numero di commit nell'intera repository corrisponde al numero di commit nella pull request significa che l'utente ha svolto una sola issue;
  *  L'utente viene inserito nel file `passiveUsers.txt`
  *  Viene creato il dataset `users1.csv` sottraendo dal dataset `users.csv` gli utenti presenti nel file `passiveUsers.txt`;  

  Tutto questo grazie alla funzione `extract_single_issue()`;
  Una volta creato il dataset `users1.csv` viene chiamata la funzione `extract_issue()`.  
  In questa funzione vengono analizzati tutti gli utenti del dataset `users1.csv`.  
  Per ciascun utente:  
    *  Ci si ricava i **commenti** in ciascun commit fatto dall'utente;  
    *  Dai commenti si ricavano le **pull request** che chiudone le issue svolte dall'utente grazie alla funzione `extract_prs()`;
    *  Da ciascuna pull request si ricava la **issue** chiusa;
    *  Viene creato un **dizionario** con **id**: *nome utente*, **issues**: *tutte le issue svolte dall'utene*;
    *  Vengono caricati tutti i dizionari nel file `ActiveUsers.json`;  
    
  Adesso bisogna creare un file JSON contenente le *labels* di ciascuna issue contenuta nel file `ActiveUsers.json`.  
  Grazie alla funzione `extract_labels()` si creerà il file `ActiveUsersLabels.json` con **id**: *nome utente*, **labels**: *tutte le etichette delle issue svolte dall'utene*.  
  I file `ActiveUsers.json` e `ActiveUsersLabels.json` sono presenti nella cartella `FileJSON`



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

## Funzioni utilizzate
Il programma utilizzerà le seguenti funzioni:  
- [create_dataset()](#`create_dataset(result, key1, key2)`)
- 
### `create_dataset(result, key1, key2)`  
### `extract_pr_numbers(html_url, repository)`
### `extract_pr_owner(pr_number, repository)`
### `extract_commit_information(pr_owner, pr_number, repository, html)`
### `extract_prs(html_url, user)`
### `extract_issue(html_url, users, prs)`
### `extact_labels(html_url)`
