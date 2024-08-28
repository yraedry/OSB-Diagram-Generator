import os
from src.services.osb_local_repos_services import Services
from src.services.operations.github_operations import GithubOperations

def main() -> None:
    # service = Services(os.getcwd())
    # service.get_services_files()
    
    github = GithubOperations() 
    github.get_github_repositories()
if __name__ == "__main__":
    main()


