# SVG
Progetto per la tesi: Creazione di un bot per i neo contributori di progetti open source in Github  
a cura di: Trotti Francesco [703010]  
  
## Introduzione
Il programma esegue quattro fasi principali presenti in quattro funzioni:  
* **createDataset**: il programma si connette al database e crea un dataset contenete *html_url* e *repository_url* di ogni issue etichettata con *E-easy*;
* **extract_pr_numbers**: viene estratto il numero della pull request che chiude la issue presa in questione;
* **extract_pr_owner**: viene estratto il proprietario della pull request;
* **extract_commit_information**: verrà preso il primo commit fatto dal proprietario della pull request e se coincide con la chiusura della pull request significa che è un *new camer* e quindi verrà inserito nel dataset *users.csv*

## Requisiti fondamentali
Programma realizzato con il linguaggio di programmazione Python. Per eseguire il codice si rchiede un ambiente di sviluppo (ambiente di sviluppo suggerito: Visual Studio Code)  
Relativamente alle librerie esterne importate, vediamo la necessità di installare sulla macchina:
* **pandas**: usato per la manipolazione e l’analisi dei dati;
* **beautifulsoup4**: usato per richiedere la pagina html;
* **pymongo**: usato per accedere ai database;
* **pyGithub**: usato per accedere alla informazioni presenti su GitHub;
* **request**: usato per creare vari tipi di richieste http;   

Per installare le librerie eseguire il comando  
pip install *"nome libreria"* sul terminale.
Una volta installate le librerie eseguire il file ***"main"*** su un IDE.

## Manuale utente
Come prima cosa il programma chiamerà la funzione *create_dataset* presente nel file *createDataset.py*.  
Qui il programma si connetterà al database dove sono presenti tutte le informazioni sulle issue etichettate con *E-easy*.  
Una volta connesso al database il programma andrà a creare il dataset *nome_dataset.csv* dove saranno inseriti *html_url* e *repository_url*.  
Creato il datset può partire il vero e proprio programma.  
Grazie al comando *pd.read_csv('Dataset/nome_dataset.csv')* il programma leggerà il dataset appena creato.
Adesso viene fatto iterare il database e nella variabile:
* **html_url**: ci sarà l'html_url;
* **repository**: verrà estratto il nome completo della repository.

Adesso viene chiamata la funzione *extract_pr_number* presente nel file  *function.py*  
Grazie a questa funzione si ricava il nuemro della pull request che chiude la issue grazie alla libreria *beutifulsoup4*.  
***inserisci immagine***  
Questo numero viene inserito nella variabile *pr_number* restituita dalla funzione.  
  
Adesso viene chiamata la funzione *extract_pr_owner* presente nel file *function.py*  
Adesso ci si connettrà alla piattaforma GitHub grazie alla libreria *github*.  
Si farà l'accesso grazie al *personal access token* e presente nel file *config.py* nella funzione *get_access_token()* che verrà inserito nella variabile *access_toke*.  
Con *Github(access_token, per_page = 100, retry = 20)* viene fatto l'accesso a GitHub.  
Adesso il programma andrà sulla pagina della pull request che chiude la issue e si ricava il proprietario che verrà inserito nella variabile *pr_owner* restituita dalla funzione.  
  
Adesso viene chiamata la funzione *extract_commit_informatio* presente nel file *function.py*  


