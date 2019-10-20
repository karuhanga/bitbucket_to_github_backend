import subprocess

import requests

from bitbucket_github.models import User, Progress

GITHUB_ENDPOINT = 'https://api.github.com'
BITBUCKET_ENDPOINT = 'https://api.bitbucket.org/2.0'


def cmd(string):
    return subprocess.run(string.split())


def copy_to_github(user, repo_slug):
    progress, created = Progress.objects.get_or_create(user=user, repo_slug=repo_slug)
    progress.queueing = False
    progress.running = True
    progress.save()

    def log(info):
        progress.message = info
        progress.save()

    try:
        log(f'Copying {repo_slug}...')

        # get profiles
        log('\tFetching profiles...')
        bitbucket_profile = requests.get(f'{BITBUCKET_ENDPOINT}/user?access_token=${user.bitbucket_token}').json()
        github_profile = requests.get(url=f'{GITHUB_ENDPOINT}/user',
                                      headers={'Authorization': f'token {user.github_token}'})

        # get repo
        log('\tFetching repo information...')
        repo = requests.get(
            f'{BITBUCKET_ENDPOINT}/repositories/{bitbucket_profile["username"]}/{repo_slug}?access_token=${user.bitbucket_token}').json()

        user_working_dir = bitbucket_profile["username"]
        repo_working_dir = f'{bitbucket_profile["username"]}/{repo_slug}'

        cmd(f'mkdir {user_working_dir}')
        cmd(f'mkdir {repo_working_dir}')

        # clone
        log('\tCloning repo...')
        clone_link = repo['links']['clone'][0]['href'].replace(bitbucket_profile['username'],
                                                               f'x-token-auth:{user.bitbucket_token}', 1)
        cmd(f"git -C {user_working_dir} clone {clone_link}")

        # create repo
        create_repo_response = requests.post(f'{GITHUB_ENDPOINT}/user/repos', json={
            'name': repo['name'],
            'private': repo['is_private'],
            'description': repo['description'],
        }, headers={'Authorization': f'token {user.github_token}'}).json()

        github_repo_git_link = create_repo_response['clone_url'].replace('https://', f'https://{user.github_token}@', 1)

        # push to new repo
        log('\tPushing code to Github repo...')
        cmd(f"git -C {repo_working_dir} push {github_repo_git_link}")

        # cleanup
        log('\tCleaning up...')
        cmd(f'rm -rf {repo_working_dir}')

        log('Done.')
    except Exception:
        log("Failed to copy repo. Please retry.")
    finally:
        progress.running = False
        progress.save()


def run(repo_slug='andela-interview-code'):
    copy_to_github(User.objects.all()[0], repo_slug)
