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
- [extract_issues](#extract_issues)
- [extact_labels](#extact_labels)


### `create_dataset`  
* **Parametri**
  * `result`: prende dal database solo i campi *html_url* e *repository_url*;
  * `key1`: *html_url*
  * `key2`: *repository_url*
* **Codice**  
 Questa funzione crea un DataFrame vuoto chiamato `df_project`.  
 Successivamente, per ogni elemento user presente nella lista `result`, controlla se contiene due chiavi, `key1` e `key2`. Se entrambe le chiavi sono presenti, il codice aggiunge una nuova riga al DataFrame `df_project` con i valori dell'URL HTML e dell'URL del repository estratti dalla lista user.  
 Infine, il DataFrame viene esportato in un file CSV chiamato `retentionIssues.csv`, utilizzando la funzione `to_csv()` di Pandas.  
  ```python
  # Crea un DataFrame vuoto chiamato df_project
    df_project = pd.DataFrame()

    # Per ogni elemento user presente nella lista result, controlla se contiene le chiavi key1 e key2
    for user in result:
        if (key1 in user and key2 in user):
            # Aggiunge una nuova riga al DataFrame df_project con i valori dell'URL HTML e dell'URL del repository estratti dalla lista user
            df_project = df_project.append({
                'html_url': user.__getitem__("html_url"),
                'repository_url': user.__getitem__("repository_url")
            }, ignore_index = True)

    # Esporta il DataFrame in un file CSV chiamato retentionIssues.csv
    # La funzione to_csv() di Pandas viene utilizzata per questo scopo
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
  * `pr_number` : numero della pull request
  * `repository` : nome completo della repository
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
 Variabile `pr_owner` contenete il proprietario della pull request.  
   
   
### `extract_commit_information`  
* **Parametri**
  * `pr_owner` : proprietario della pull request
  * `pr_number`: numero della pull request
  * `repository`: nome completo della repository
  * `html_url`: URL della issue
* **Codice**  
 Il codice ha lo scopo di verificare se una particolare Pull Request su GitHub è stato chiuso tramite un commit dell'autore della pull request.  
 Viene prima costruito l'URL del commit da controllare, quindi viene effettuata una richiesta HTTP alla pagina del commit e si cerca un link nella pagina che corrisponde all'URL della pull request in questione.  
 Se il link viene trovato, si aggiunge l'autore della pull request ad un file CSV.  
 In caso di errori (come limite di rate o problemi di connessione), il codice gestisce questi errori e riprova dopo un certo intervallo di tempo.  
  ```python
  #creazione URL della pull request
  url = "https://github.com/" + repository + "/pull/" + str(pr_number)
  #Inizializzazione lista vuota che conterrà le date dei commit
  data_list = []
  #Ciclo while infinito
  while True:
      try:
          # Creazione oggetto Github con access token e impostazioni di pagina e ritentativi
          g = Github(access_token, per_page = 100, retry = 20)
          # Ottenimento repository specifico tramite nome
          repo = g.get_repo(repository)
          # Ottenimento di tutti i commit dell'autore specificato nella Pull Request
          all_commits = repo.get_commits(author=pr_owner)
          # Ciclo for per inserire le date dei commit nella lista
          for commit in all_commits:
              data_commit = commit.commit.author.date
              data_list.append(data_commit)

          # Controllo che la lista contenga almeno un elemento
          if (len(data_list) > 0):
              # Estrazione della data del primo commit
              data_first_commit = data_list[-1]

              # Ciclo for sui commit dell'autore
              for commit in all_commits:
                  # Controllo se la data del commit è uguale alla data del primo commit
                  if commit.commit.author.date == data_first_commit:
                      # Creazione dell'URL della pagina del commit tramite l'identità del commit
                      html_url = "https://github.com/" + repository + "/commit/" + commit._identity
                      # Richiesta GET all'URL del commit
                      response = requests.get(html_url)
                      response.raise_for_status()
                      # Parsing della risposta con BeautifulSoup
                      soup = BeautifulSoup(response.text, 'html.parser')
                      # Estrazione di tutti i tag "a" presenti nella pagina del commit
                      tags = soup.find_all("a")

                      # Ciclo for sui tag "a"
                      for tag in tags:
                          # Estrazione del valore dell'attributo href
                          link = str(tag.get('href'))
                          # Controllo se l'URL della Pull Request corrisponde all'URL presente nel tag "a"
                          if url == link:
                              # Lettura del file CSV contenente i dati degli utenti e creazione di un DataFrame
                              df_project = pd.read_csv('Dataset/users.csv')
                              # Aggiunta delle informazioni dell'autore al DataFrame
                              df_project = df_project.append({
                                  'name' : pr_owner,
                                  'html_url':html
                              },ignore_index = True)
                              # Scrittura del DataFrame nel file CSV
                              df_project.to_csv('Dataset/users.csv', encoding='utf-8', index=False)
                              # Uscita dal ciclo for sui tag "a"
                              break
      #Gestione delle eccezioni
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
      break
   ```
* **Risultato**  
 Dataset `user.csv` contenente il nome degli utenti che hanno svolto la issue del database come prima issue nel repository e l'URL della issue.  
   
### `extract_single_issue`
* **Parametri**  
  * `html_url` : URL della issue
  * `user` : username di chi ha svolta la issue
* **Codice**  
 Questa funzione si occupa di verificare se un utente Github ha effettivamente contribuito ad una pull request specifica.  
 In dettaglio, il codice estrae il nome del repository e il numero di PR dall'url fornito, accede al repository e alla PR specificati, ottiene tutti i commit associati alla PR e quelli associati all'utente specificato, e confronta questi ultimi per verificare se l'utente ha effettivamente contribuito alla PR.  
 Se la verifica è positiva, il nome dell'utente viene scritto sul file di testo `passiveUsers.txt`.  
 In caso di errori (come limite di rate o problemi di connessione), il codice gestisce questi errori e riprova dopo un certo intervallo di tempo.
  ```python
   # inizializza due insiemi vuoti
    list1 = set()
    list2 = set()

    # estrai il nome del repository e il numero di PR dall'html_url
    repository = extract_repository(html_url)
    number = extract_number(html_url)

    # continua il loop finché il codice all'interno del loop non viene interrotto
    while True:
        try:
            # autentica con Github usando l'access token e imposta la dimensione della pagina e il numero di tentativi di riprova
            g = Github(access_token, per_page=100, retry=20)

            # ottieni il repository specificato dal nome
            repo = g.get_repo(repository)

            # estrai il numero della PR dall'url
            pr_number = extract_pr_numbers(html_url, repository) 

            # ottieni la PR specificata dal numero e dal repository
            pr = repo.get_pull(number=pr_number)

            # ottieni tutti i commit associati alla PR
            commit_pr = pr.get_commits()

            # inizializza un contatore
            count = 0

            # per ogni commit, controlla se l'autore è l'utente specificato e aggiungi l'url del commit all'insieme lista1
            for commit in commit_pr:
                if (commit.author is not None):
                    if (commit.author.login == user):
                        count += 1
                        list1.add(commit.html_url)

            # ottieni tutti i commit associati all'utente specificato e conta il loro numero
            all_commits = repo.get_commits(author=user)
            number = all_commits.totalCount

            # per ogni commit, aggiungi l'url del commit all'insieme lista2
            for c in all_commits:
                list2.add(c.html_url)

            # se il numero di commit associati all'utente specificato corrisponde al numero di commit associati alla PR e l'insieme lista1 è uguale all'insieme lista2, scrivi il nome dell'utente su un file di testo
            if (count == number and list1 == list2):
                f = open("Dataset/passiveUsers.txt", "a+")
                f.write(user + "\n") 
                f.close()
                
        # gestisci eventuali eccezioni
        except RateLimitExceededException as e:
            print(e.status)
            print('Limite di velocità superato')
            time.sleep(300)
            continue
        except BadCredentialsException as e:
            print(e.status)
            print('Eccezione credenziali errate')
            break
        except UnknownObjectException as e:
            print(e.status)
            print('Eccezione oggetto sconosciuto')
            break
        except GithubException as e:
            print(e.status)
            print('Eccezione generale')
            break
        except UnboundLocalError as e:
            print(e.status)
            print('Errore di variabile non associata')
            break
        except requests.exceptions.ConnectionError as e:
            print('Limite di riprova superato')
            print(str(e))
            time.sleep(10)
            continue
        except requests.exceptions.Timeout as e:
            print(str(e))
            print('Eccezione timeout')
            time.sleep(10)
            continue
        
        # interrompi il loop
        break
  ```
* **Risultato**  
 File di testo `passiveUsers.txt` contenente l'username degli utenti che hanno svolto una sola issue nella repository.  
   
### `extract_prs`
* **Parametri**  
  * `html_url` : URL della issue
  * `user` : username di chi ha svolta la issue 
* **Codice**  
 Questa funzione estrae il nome del repository dall'url fornito e si connette all'API di Github con un access token specifico.  
 Successivamente, il codice recupera tutti i commit effettuati dall'utente nel repository e per ognuno di essi estrae il messaggio di commit.  
 Se nel messaggio di commit è presente una stringa nel formato "#numero", dove "numero" è un intero, il codice aggiunge il valore di "numero" ad una lista di PR trovate.  
 Infine, il codice gestisce alcune eccezioni che potrebbero essere sollevate durante l'accesso a Github, come il limite di velocità superato, le credenziali errate, oggetti sconosciuti, ecc.  
 Il risultato dell'esecuzione del codice è una lista di interi, dove ogni intero rappresenta il numero di una PR a cui l'utente ha contribuito.  
  ```python
  # Estraggo il nome del repository dall'url
    repository = extract_repository(html_url)
    
    # Creo due liste vuote per memorizzare i commit e le PR
    commit_list = []
    prs = []
    
    # Inizio un loop infinito per gestire le eccezioni
    while True:
        try:
            # Creo un'istanza dell'API di Github
            g = Github(access_token, per_page=100, retry=20)
            
            # Recupero il repository corrispondente al nome
            repo = g.get_repo(repository)
            
            # Recupero tutti i commit effettuati dall'utente nel repository
            all_commits = repo.get_commits(author=user)
            
            # Per ogni commit, estraggo il suo hash
            for c in all_commits:
                commit_list.append(c.sha)
            
            # Inverto l'ordine della lista dei commit, così da analizzare prima quelli più vecchi
            commit_list.reverse()
            
            # Per ogni commit, estraggo i numeri delle PR a cui il commit si riferisce
            for sha in commit_list:
                commit = repo.get_commit(sha)
                message = commit.commit.message
                pattern = r'#\d+' # Espressione regolare per cercare stringhe nel formato "#numero"
                matches = re.findall(pattern, message)
                for match in matches:
                    prs.append(match[1:]) # Aggiungo solo il numero alla lista di PR
            
        # Gestisco le possibili eccezioni sollevate durante la connessione a Github
        except RateLimitExceededException as e:
            print(e.status)
            print('Rate limit exceeded')
            time.sleep(300) # Attendo 5 minuti prima di riprovare
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
            time.sleep(10) # Attendo 10 secondi prima di riprovare
            continue
        except requests.exceptions.Timeout as e:
            print(str(e))
            print('Time out exception')
            time.sleep(10) # Attendo 10 secondi prima di riprovare
            continue
        break
    
    # Restituisco la lista di numeri di PR trovate
    return(prs)
  ```
* **Risultato**  
 Lista `prs` contente i numeri di tutte le pull request di cui l'utente `user` ne è proprietario.  
   
### `extract_issues`
* **Parametri**
  * `html_url` : URL della issue
  * `user` : username di chi ha svolta la issue
  * `prs` : lista contente i numeri di tutte le pull request di cui l'utente `user` ne è proprietario. 
* **Codice**  
  Questa funzione estrae le issue associate ai pull request di un repository Github. Il programma prende in input un link HTML per il repository, un access token per autenticarsi su Github, un nome utente e una lista di numeri di pull request.  
 Il programma scorre i pull request uno alla volta e cerca le issue associate a ciascun pull request. Per ogni pull request, il programma fa una richiesta HTTP per la pagina del pull request su Github e cerca i tag "a" che contengono l'URL delle issue associate al repository. Se il tag contiene un numero di issue, il programma cerca l'oggetto issue corrispondente nel repository e lo aggiunge a una lista di issue. Infine, il programma restituisce la lista delle issue trovate.  
 Il codice gestisce anche eventuali errori di connessione con Github (ad esempio, se la richiesta HTTP fallisce) e il limite di rate (ossia, il numero di richieste HTTP che si possono fare in un certo periodo di tempo).
  ```python
  # Estraiamo il repository dal link HTML fornito come argomento
    repository = extract_repository(html_url)

    # Inizializziamo una lista vuota per le issue
    issue_list = []

    # Scandiamo i pull request uno alla volta
    for pr in prs:
        # Inizializziamo un ciclo while per gestire eventuali errori di connessione
        while True:
            try:
                # Convertiamo il numero del pull request in un intero
                pr_number = int(pr)
                # Creiamo un'istanza di Github, autenticandoci con un access token
                g = Github(access_token, per_page = 100, retry = 20)
                # Prendiamo l'oggetto pull request dal repository
                repo = g.get_repo(repository)
                pr = repo.get_pull(pr_number)

                # Se l'autore del pull request è l'utente specificato
                if pr.user.login == user :

                    # Costruiamo l'URL della pagina del pull request su Github
                    html_url = "https://github.com/" + repository +"/pull/" + str(pr_number)
                    # Facciamo una richiesta HTTP per la pagina del pull request
                    response = requests.get(html_url)

                    # Inizializziamo una variabile per il numero della issue
                    issue_number = 0

                    # Verifichiamo che la richiesta HTTP sia andata a buon fine
                    response.raise_for_status()
                    # Analizziamo il contenuto HTML della pagina del pull request con BeautifulSoup
                    soup = BeautifulSoup(response.text, 'html.parser')
                    # Estraiamo parte dell'URL delle issue dal repository
                    url = "https://github.com/" + repository + "/issues"
                    # Troviamo tutti i tag "a" nella pagina HTML
                    tags = soup.find_all("a")
                    for tag in tags:
                        link = str(tag.get('href'))
                        if url in link:
                            # Estraiamo il numero della issue, che si trova dopo il cancelletto nella stringa del tag
                            number_string = tag.string
                            if (number_string):
                                if (number_string[0] == '#'):                        
                                    issue_number = int(number_string[1:])
                                    # Prendiamo l'oggetto issue dal repository e lo aggiungiamo alla lista delle issue
                                    issue = repo.get_issue(issue_number)
                                    issue_list.append(issue.html_url)
                                    break                                    
            # Gestiamo eventuali errori di connessione
            except RateLimitExceededException as e:
                print(e.status)
                print('Rate limit exceeded')
                time.sleep(300)
                continue
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
            except:
                break
            # Se tutto va bene, usciamo dal ciclo while
            break

    # Restituiamo la lista delle issue
    return(issue_list)
  ```
* **Risultato**  
 Lista `issue_list` contente l'URL di tutte le issue fatte da `user`.  
     
### `extact_labels`
* **Parametri**
  * `html_url`: URL della issue 
* **Codice**  
 Questa funzione restituisce le etichette associate a una specifica issue di un repository Github. Il programma prende in input un link HTML per il repository, un access token per autenticarsi su Github e il numero della issue.  
 Il programma cerca l'oggetto issue corrispondente alla specifica issue nel repository e ne restituisce le etichette. Gli eventuali errori (come il limite di rate o problemi di connessione) vengono gestiti attraverso un blocco try-except, in modo che il programma non si interrompa in caso di errori.  
   ```python
   repository = extract_repository(html_url)  # estrae il nome del repository dal link HTML
   number = extract_number(html_url)  # estrae il numero dell'issue dal link HTML

   while True:
       try:
           g = Github(access_token, per_page=100, retry=20)  # si connette a Github con le credenziali fornite
           repo = g.get_repo(repository)  # prende il repository specificato
           issue = repo.get_issue(number=number)  # cerca l'oggetto issue corrispondente al numero specificato
           labels = str(issue.labels)  # estrae le etichette associate all'issue
           return labels  # restituisce le etichette
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
       break

   ```
* **Risultato**  
 Lista `labels` contenete le etichette di tutte le issue fatte da `user`.  
   
## File  
Il programma è costituito dai seguenti file:
 - [main.py](#mainpy)
 - [config.py](#configpy)
 - [function.py](#functionpy)
 - [datasetRetentionIssue.py](#datasetRetentionIssuepy)
 - [extractUsers.py](#extractUsers-py)
 - [extractPassiveUsers.py](#extractPassiveUsers-py)
 - [extractActiveUsers.py](#extractActiveUsers-py)
 - [extractActiveUsersLabels.py](#extractActiveUsersLabels-py)  


### main.py  
* **Codice**  
  ```python
  import datasetRetentionIssue
  import extractUsers
  import extractActiveUsers
  import extractPassiveUsers
  import extractActiveUsersLabels

  if __name__ == '__main__':

      datasetRetentionIssue.dataset()

      extractUsers.extract_users()

      extractPassiveUsers.extract_passive_users()
      extractActiveUsers.extract_active_users()
      extractActiveUsersLabels.extract_active_users_labels()
  ```
### config.py
* **Codice**  
  ```python
  def get_access_token():
    return "inserisci il tuo personal access token"
  ```
### function.py
* **Codice**  
  ```python
  ```
### datasetRetentionIssue.py  
* **Codice**  
  ```python
  # Librerie
  from pymongo import MongoClient
  import function

  def dataset():
      # Creiamo un oggetto MongoClient per connetterci al database MongoDB
      client = MongoClient('localhost', 'inserisci numero porta')
      # Selezioniamo il database 
      db = client.nome_database
      # Selezioniamo la collezione 
      collection = db.nome_collection

      # Definiamo le chiavi che vogliamo estrarre dalla collezione
      key1 = "html_url"
      key2 = "repository_url"

      # Eseguiamo una query che seleziona solo le chiavi "html_url" e "repository_url" di tutti i documenti della collezione
      result = collection.find({}, {"_id" : 0, "html_url" : 1, "repository_url": 1}, batch_size=20)

      # Richiamiamo la funzione create_dataset dal modulo function
      function.create_dataset(result, key1, key2)
  ```  
* **Risultato**
 Dataset `retentionIssue.csv`.  
 ### extractUsers.py  
 * **Codice**  
  ```python
  import function
  import pandas as pd

  def extract_users():
      # legge il file CSV contenente gli URL delle issue e dei repository associati
      df = pd.read_csv('Dataset/retentionIssue.csv')

      # itera su ogni riga del dataframe
      for index, row in df.iterrows():
          # ottiene il repository come stringa e l'URL dell'issue
          repo = str(row['repository_url'])
          html_url = str(row['html_url'])

          # estrae il numero dell'issue e il nome del repository dall'URL dell'issue
          repository = repo[29:]
          pr_number = function.extract_pr_numbers(html_url, repository)

          # se l'URL dell'issue contiene un numero di pull request
          if (pr_number != 0):
              # estrae il proprietario della pull request
              pr_owner = function.extract_pr_owner(pr_number, repository)

              # se il proprietario esiste, estrae le informazioni sui commit della pull request
              if (pr_owner != 0):
                  function.extract_commit_information(pr_owner, pr_number, repository, html_url)

  ```  
  * **Risultato**  
    Dataset `user.csv`.
 ### extractPassiveUsers.py
 * **Codice**  
  ```python
  #Librerie
  import pandas as pd
  import function

  # Funzione per estrarre gli utenti passivi dal dataset
  def extract_passive_users():
      # Legge il file csv contenente le informazioni sugli utenti
      df = pd.read_csv('Dataset/users.csv')

      # Itera sul dataframe per estrarre le informazioni di ciascun utente
      for index, row in df.iterrows():
          html_url = str(row['html_url'])  # URL del profilo GitHub dell'utente
          user = str(row['name'])  # Nome dell'utente
          
          # Chiama la funzione per estrarre le informazioni sulla singola issue
          function.extract_single_issue()
  ```  
  * **Risultato**  
   File `passiveUsers.txt`
 ### extractActiveUsers.py
 * **Codice**  
  ```python
  #Librerie
  import json
  import pandas as pd
  import function

  def extract_active_users():
      # lista che conterrà le informazioni sulle issue degli utenti attivi
      issue_list = []

      # lettura del dataset contenente i dati degli utenti
      df = pd.read_csv('Dataset/users1.csv')

      # ciclo su ogni riga del dataset
      for index, row in df.iterrows():
          # estrazione dell'html_url e del nome dell'utente
          html_url = str(row['html_url'])
          user = str(row['name'])

          # estrazione dei pr associati all'utente
          prs = function.extract_prs(html_url, user)

          # estrazione delle issue associate ai pr
          issues = function.extract_issues(html_url, user, prs)

          # rimozione delle eventuali issue duplicate
          issues = issues[:]
          unique_list = []
          for i in issues:
              if i not in unique_list:
                  unique_list.append(i)

          # se l'utente ha almeno una issue unica, aggiungi le informazioni alla lista di output
          if (len(unique_list) > 1):
              issue_dict = {"id" : user, "issues" : unique_list}
              issue_list.append(issue_dict)

      # scrittura del risultato su un file JSON
      with open('ActiveUsers.json', 'w') as fp:
          json.dump(issue_list, fp)

  ```  
  * **Risultato**
   File JSON `ActiveUseres.json`
 ### extractActiveUsersLabels.py
 * **Codice**  
  ```python
  #Librerie
  import json
  import function

  def extract_active_users_labels():
      # Apri il file JSON contenente l'elenco degli utenti attivi e le relative issues
      with open('ActiveUsers.json', 'r') as f:
          data = json.load(f)

      dictionaries = []
      # Itera su ogni dizionario dell'elenco per ottenere le label associate alle issues di ogni utente
      for dizionario in data:
          labels_list = []
          user = dizionario['id']
          issues = dizionario['issues']
          for i in issues:
              # Estrai le label dalle issues utilizzando una funzione di supporto
              labels = function.extract_labels(i)
              labels_list.append(labels)
          # Costruisci un dizionario contenente l'utente e le sue label e aggiungilo alla lista di dizionari
          labels_dict = {"id" : user, "labels" : labels_list}
          dictionaries.append(labels_dict)
      # Salva la lista di dizionari in un nuovo file JSON
      with open('ActiveUsersLabels.json', 'w') as fp:
          json.dump(dictionaries, fp)
  
  ```  
  * **Risultato**
   File JSON `ActiveUseresLabels.json`

## Tabella
| **Nome File** | **Quantità** |
|-----------|---------|
| retentionIssue.csv | 354648 |  
| users.csv | 11167 |
| passiveUsers.txt | 9 |
| users1.csv | 11158 |
| ActiveUsers.json|  2593  | 
| ActiveUseresLabels.json |  2593  | 
