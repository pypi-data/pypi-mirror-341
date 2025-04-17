
def get_param_from_repo(repos, repo_name='homepage'):
    if repos:
        for repo in repos:
            if 'clone_url' in repo:
                if (repo['fork'] == False):
                    return repo[repo_name]
    return None