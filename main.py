import os
from src.services.osb_local_repos_services import Services
from src.routes.github_routes import GithubRoutes

def main() -> None:
    # service = Services(os.getcwd())
    # service.get_services_files()
    
    github = GithubRoutes("https://api.github.com")
    github.get_all_github_repos()
if __name__ == "__main__":
    main()


