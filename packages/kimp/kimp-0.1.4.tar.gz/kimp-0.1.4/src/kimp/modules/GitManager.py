import os.path
import requests
from git import Repo, GitCommandError


class GitManager:
    def __init__(self, token, username):
        self.token = token
        self.username = username
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }

    def is_connected(self):
        """Check if the provided GitHub token and username are valid."""
        url = "https://api.github.com/user"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            user_data = response.json()
            if user_data.get("login") == self.username:
                print("Token and username are valid.")
                return True
            else:
                print("Token is valid but username does not match.")
                return False
        else:
            print(f"Failed to validate token and username: {response.content}")
            return False

    def repo_exists(self, repo_name):
        """Check if a GitHub repository exists for the authenticated user."""
        url = f"https://api.github.com/user/repos"
        params = {'per_page': 200, 'page': 1}
        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code == 200:
            repos = response.json()
            for repo in repos:
                if repo['name'].lower() == repo_name.lower():
                    print(f"Repository '{repo_name}' already exists.")
                    return True
            return False
        else:
            print(f"Failed to retrieve repositories: {response.content}")
            return False

    def clone_repo(self, repo_name, clone_dir):
        """Clone a repository."""
        repo_url = f"https://{self.username}:{self.token}@github.com/{self.username}/{repo_name}.git"

        if os.path.exists(f"{clone_dir}"):
            return True
        try:
            Repo.clone_from(repo_url, clone_dir)
            return True
        except GitCommandError as e:
            return False

    def pull(self, repo_dir, branch="main"):
        """Pull changes from GitHub."""
        try:
            repo = Repo(repo_dir)
            origin = repo.remote(name='origin')
            origin.pull(branch)
            print(f"Pulled latest changes from branch {branch}.")
            return True
        except GitCommandError as e:
            print(f"Error pulling changes: {e}")
            return False

    def list_repos_starting_with(self, prefix):
        """
        List all repositories that start with a given prefix.

        :param prefix: The prefix string to match repository names.
        :return: A list of repository names that start with the given prefix.
        """
        url = f"https://api.github.com/user/repos"
        params = {'per_page': 200, 'page': 1}
        repos_matching = []

        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code == 200:
            repos = response.json()

            # Filter repositories by prefix
            for repo in repos:
                if repo['name'].startswith(prefix):
                    repos_matching.append(repo['name'])

            # Check if there's a next page of repositories
            if 'next' in response.links:
                url = response.links['next']['url']

        return repos_matching
