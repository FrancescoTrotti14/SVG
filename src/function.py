#LIBRERIE
from github import Github, RateLimitExceededException, BadCredentialsException, BadAttributeException, \
    GithubException, UnknownObjectException, BadUserAgentException
from bs4 import BeautifulSoup
import time
import requests
import config
import pandas as pd

access_token = config.get_access_token()

def extract_pr_numbers(html_url, repository) : 
    pr_number = 0  
    response = requests.get(html_url)
    try:
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        #Ricavo parte dell'url che starà nell'href
        url = "https://github.com/" + repository + "/pull"
        #Trovo tutti i tag "a"
        tags = soup.find_all("a")
        for tag in tags:
            link = str(tag.get('href'))
            if url in link:
                #ricavo il numero della pullrequest compreso di cancelletto
                number_string = tag.string
                if (number_string):
                    if (number_string[0] == '#'):
                        try:
                            pr_number = int(number_string[1:])
                            break
                        except ValueError:
                            pr_number = 0
                        break
                    else:
                        pr_number = 0
                else:
                    pr_number = 0
    except requests.exceptions.HTTPError:
        pr_number = 0
    return pr_number

def extract_pr_owner(pr_number, repository):
    pr_owner = 0
    while True:
        try:
            g = Github(access_token, per_page = 100, retry = 20)
            repo = g.get_repo(repository)
            #Trovo la pull request interessata
            pr = repo.get_pull(number=pr_number)
            #Estraggo l'autore
            pr_owner = pr.user.login   
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
    return pr_owner

def extract_commit_information(pr_owner, pr_number, repository, html):
    #Ricavo url che starà nell'href
    url = "https://github.com/" + repository + "/pull/" + str(pr_number)
    #Lista di date dei commit
    data_list = []
    count = 0
    while True:
        try:
            g = Github(access_token, per_page = 100, retry = 20)
            repo = g.get_repo(repository)
            #Ricavo tutti i commit dell'autore
            all_commits = repo.get_commits(author=pr_owner)
            for commit in all_commits:
                count += 1
                #Ricavo la data del commit e lo aggiungo alla lista
                data_commit = commit.commit.author.date
                data_list.append(data_commit)
            #Trovo la data del primo commit
            if (len(data_list) > 0):
                data_first_commit = data_list[-1]
                #Vado sulla pagina del primo commit e controllo se chiude la pull request analizzata prima
                for commit in all_commits:
                    if commit.commit.author.date == data_first_commit:
                        html_url = "https://github.com/" + repository + "/commit/" + commit._identity
                        response = requests.get(html_url)
                        response.raise_for_status()
                        soup = BeautifulSoup(response.text, 'html.parser')
                        tags = soup.find_all("a")
                        for tag in tags:
                            link = str(tag.get('href'))
                            if url == link:
                                df_project = pd.read_csv('Dataset/users2.csv')
                                df_project = df_project.append({
                                    'name' : pr_owner,
                                    'html_url':html
                                },ignore_index = True)
                                df_project.to_csv('Dataset/users2.csv', encoding='utf-8', index=False)
                                break
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
    return count