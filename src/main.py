import function
import pandas as pd 

if __name__ == '__main__':

    df = pd.read_csv('Dataset/tesi42.csv')
    number = 1

    for index, row in df.iterrows():
        repo = str(row['repository_url'])
        html_url = str(row['html_url'])
        repository = repo[29:]
        print(f'analizzo {number} : {html_url}')
        pr_number = function.extract_pr_numbers(html_url, repository)
        if (pr_number != 0):
            pr_owner = function.extract_pr_owner(pr_number, repository)
            if(pr_owner != 0):
                commit_numbers = function.extract_commit_information(pr_owner, pr_number, repository,html_url)
        number += 1
    print("finish")