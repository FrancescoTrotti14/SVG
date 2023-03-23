# retention-issues
Progetto per la tesi: **Creazione di un bot per i neo contributori di progetti open source in Github**  
a cura di: Trotti Francesco [703010]  
  
## Introduzione
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
  Ora il programma creerà un dataset contenente l' ***html_url*** e il ***repository_url*** di ciascuna issue presente nel Database appena importato su **MongoDB**.  
  Il dataset in questione è presente nella cartella `Dataset` con il nome di `retention-issue.csv`

* **Estrazione utenti**: In questa fase viene analizzata ciascuna issue presente nel dataset `retention-issue.csv`.  
L'obbiettivo di questa fase è capire l'utente che ha lavorato alla issue presa in questione e capire se la issue analizzata è la **prima** issue svolta dall'utente in questa **repository**.  
Quindi per ciascuna issue bisognerà:  
  * Trovare la **pull request** che chiude l'issue;
  * Trovare il **proprietario** della **pull request**;  
  * Trovare tutti i **commit** fatti dall'utente nella **repository**;  
  * Controllare che il **primo committ** chiuda la **pull request** analizzata;  
  * Salvare l'**utente** nel caso si verifichi il passo precedente;

  Ciascun utente verrà salvato all'interno del dataset `users.csv`.  
  Il dataset `users.csv` conterrà in **name** il nome dell'utente e in **html_url** l'url della prima issue svolta nella repository.
  
* **Fase 3**

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
Una volta installate le librerie eseguire il file `main.py`.

## Manuale utente
Come prima cosa il programma chiamerà la funzione `create_dataset` presente nel file `createDataset.py`.  
Qui il programma si connetterà al database dove sono presenti tutte le informazioni sulle issue etichettate con `E-easy`.  
Una volta connesso al database il programma andrà a creare il dataset *retention-issue.csv* dove saranno inseriti `html_url` e `repository_url`.  
Creato il datset può partire il vero e proprio programma.  
Grazie al comando `pd.read_csv('Dataset/retention-issue.csv')` il programma leggerà il dataset appena creato.
Adesso viene fatto iterare il database e nella variabile:
* `html_url`: ci sarà l'html_url;
* `repository`: verrà estratto il nome completo della repository.

Adesso viene chiamata la funzione `extract_pr_number` presente nel file  `function.py`  
Grazie a questa funzione si ricava il nuemro della pull request che chiude la issue grazie alla libreria `beutifulsoup4`.  
Questo numero viene inserito nella variabile `pr_number` restituita dalla funzione.  
  
Adesso viene chiamata la funzione `extract_pr_owner` presente nel file `function.py`  
Adesso ci si connettrà alla piattaforma GitHub grazie alla libreria `github`.  
Si farà l'accesso grazie al *personal access token* e presente nel file `config.py` nella funzione `get_access_token()` che verrà inserito nella variabile `access_token`.  
Con `Github(access_token, per_page = 100, retry = 20)` viene fatto l'accesso a GitHub.  
Adesso il programma andrà sulla pagina della pull request che chiude la issue e si ricava il proprietario che verrà inserito nella variabile `pr_owner` restituita dalla funzione.  
  
Adesso viene chiamata la funzione *extract_commit_informatio* presente nel file `function.py`  
Qui si recuperano tutti i commit dell'autore che ha chiuso la pull request.  
Viene preso in particolare il primo commit effettuato dall'utente e se questo coincide con la chiusura della pull request richiamata nella funzione precedente, il nome utente dell'autore e l'url html vengono salvati in un dataset chiamato `users.csv`. 


