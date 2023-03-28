# retention-issues
Progetto per la tesi: **Creazione di un bot per i neo contributori di progetti open source in Github**  
a cura di: **Trotti Francesco [703010]**  

## Indice
 - [Introduzione](#Introduzione)
 - [Requisiti fondamentali](#Requisiti-fondamentali)
 - [Presentazione](#Presentazione)
 - [Funzioni utilizzate](#Funzioni-utilizzate)
 - [File](#File)
 
## Introduzione
L'obbiettivo di questo programma è quello di 
 
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


## Funzioni utilizzate
Il programma utilizzerà le seguenti funzioni:  
- [create_dataset](#create_dataset)
- [extract_pr_numbers](#extract_pr_numbers)
- [extract_pr_owner](#extract_pr_owner)
- [extract_commit_information](#extract_commit_information)
- [extract_single_issue](#extract_single_issue)
- [extract_prs](#extract_prs)
- [extract_issue](#extract_issue)
- [extact_labels](#extact_labels)


### `create_dataset`  
* **Parametri**
  * `result`: prende dal database solo i campi *html_url* e *repository_url*;
  * `key1`: *html_url*
  * `key2`: *repository_url*
* **Codice**  
 Creo un nuovo DataFrame vuoto e lo assegno alla variabile `df_project`  
   ```python
    df_project = pd.DataFrame() 
    ```  
    Trovo, se presenti, *html_url* e *repository_url* per ogni elemento del database  
    ```python
    for user in result:
        if (key1 in user and key2 in user):
            df_project = df_project.append({
                'html_url': user.__getitem__("html_url"),
                'repository_url': user.__getitem__("repository_url")
            }, ignore_index = True) 
     ```
   Inserisco nel dataset `retentionIssue.csv`    
   ```python
   df_project.to_csv('Dataset/retentionIssues.csv', sep=',', encoding='utf-8', index=False) 
   ```  
* **Risultato**  
   Dataset `retentionIssue.csv`
      
### `extract_pr_numbers`  
* **Parametri**
  * `html_url` : url della issue
  * `repository` : nome intero della repository dove è presente la issue
* **Codice**  
La funzione cerca di estrarre il numero della pull request da una pagina HTML di Github e restituisce 0 se non riesce a trovarlo o se si verifica un errore nella richiesta HTTP  
  ```python
  pr_number = 0  # Inizializza la variabile "pr_number" a 0.
  response = requests.get(html_url)  # Esegue una richiesta HTTP GET all'URL specificato dalla variabile "html_url" utilizzando la libreria "requests".
  try:  # Verifica se la richiesta è andata a buon fine utilizzando la funzione "raise_for_status()". Se si, il codice continua a eseguire, altrimenti "pr_number" viene impostato a 0.
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')  # Utilizza la libreria "BeautifulSoup" per analizzare l'HTML della pagina ricevuta dalla richiesta.
    url = "https://github.com/" + repository + "/pull"  # Crea una stringa di base dell'URL della pull request utilizzando la variabile "repository".
    tags = soup.find_all("a")  # Trova tutti i tag "a" nell'HTML della pagina.
    for tag in tags:  # Scansiona tutti i tag "a" e cerca un tag che abbia un attributo "href" che contenga l'URL della pull request. Se lo trova, memorizza la stringa contenente il numero della pull request (che potrebbe essere nel formato "#1" o "pull/1") nella variabile "number_string".
        link = str(tag.get('href'))
        if url in link:
            number_string = tag.string
            if (number_string):  # Se "number_string" non è vuota e inizia con il carattere "#", estrae il numero della pull request come una stringa e lo converte in un intero. Imposta la variabile "pr_number" con questo valore e termina il ciclo "for".
                if (number_string[0] == '#'):
                    try:
                        pr_number = int(number_string[1:])
                        break
                    except ValueError:
                        pr_number = 0
                        break
                else:  # Se "number_string" è vuota, non inizia con il carattere "#" o non può essere convertita in un intero, imposta "pr_number" a 0 e termina il ciclo "for".
                    pr_number = 0
            else:
                pr_number = 0
    # Se non viene trovato alcun tag "a" con l'URL della pull request, imposta "pr_number" a 0.
    if pr_number == 0:
        pr_number = 0
  except requests.exceptions.HTTPError:  # Se la richiesta HTTP non va a buon fine (ad esempio, se la pagina non esiste o se il server restituisce un errore), imposta "pr_number" a 0.
    pr_number = 0
  # Restituisce "pr_number".
  return pr_number
  ```
 * **Risultato**  
  Variabile `pr_number` contente il numero della pull request che chiude la issue.
### `extract_pr_owner`  
* **Parametri**
* **Codice**  
  La funzione cerca di recuperare l'autore di una pull request su Github, a partire dal numero di tale pull request (`pr_number`) e dal nome del repository (`repository`), utilizzando la libreria `PyGithub`.  
  La funzione inizia un ciclo **while** infinito per effettuare la richiesta di recupero dell'autore della pull request tramite la creazione di un'istanza dell'oggetto `Github` utilizzando il token di accesso fornito (`access_token`).  
  Se la chiamata alle API di Github è andata a buon fine, esce dal ciclo **while** e restituisce il login dell'autore della pull request recuperato (`pr_owner`).  
  Se si verifica un'eccezione durante la richiesta, la funzione gestisce l'eccezione e ripete il ciclo **while** per effettuare un nuovo tentativo di recupero dell'autore della pull request.  
  ```python
  pr_owner = 0  # Inizializza la variabile 'pr_owner' a 0

  # Inizia un ciclo while infinito per recuperare l'autore della pull request
  while True:
    try:
        # Crea un oggetto 'Github' con il token di accesso fornito
        g = Github(access_token, per_page=100, retry=20)

        # Recupera l'oggetto 'Repository' corrispondente al nome fornito
        repo = g.get_repo(repository)

        # Recupera l'oggetto 'PullRequest' corrispondente al numero fornito
        pr = repo.get_pull(number=pr_number)

        # Recupera il login dell'autore della pull request
        pr_owner = pr.user.login

    # Gestisce possibili eccezioni che possono verificarsi durante il recupero dei dati
    except RateLimitExceededException as e:
        print(e.status)
        print('Rate limit exceeded')
        time.sleep(300)
        continue
    except BadCredentialsException as e:
        print(e.status)
        print('Bad credentials exception')
        break
    except UnknownObjectException as e:
        print(e.status)
        print('Unknown object exception')
        break
    except GithubException as e:
        print(e.status)
        print('General exception')
        break
    except UnboundLocalError as e:
        print(e.status)
        print('UnboundLocalError')
        break
    except requests.exceptions.ConnectionError as e:
        print('Retries limit exceeded')
        print(str(e))
        time.sleep(10)
        continue
    except requests.exceptions.Timeout as e:
        print(str(e))
        print('Time out exception')
        time.sleep(10)
        continue

    # Se la chiamata alle API di Github è andata a buon fine, esce dal ciclo while
    break

  # Restituisce il valore dell'autore della pull request recuperato
  return pr_owner

  ```
* **Risultato**  
### `extract_commit_information`
### `extract_single_issue`
### `extract_prs`
### `extract_issue`
### `extact_labels`


## File
| **Nome File** | **Quantità** |
|-----------|---------|
| retentionIssue.csv | 354648 |  
| users.csv | 11167 |
| passiveUsers.txt | 9 |
| users1.csv | 11158 |
| ActiveUsers.json|  2593  | 
| ActiveUseresLabels.json |  2593  | 



