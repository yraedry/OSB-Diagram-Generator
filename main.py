import os
from services.osb_local_repos_services import OsbLocalReposService

def main() -> None:
    service = OsbLocalReposService(os.getcwd())
    osb_services = service.get_services_files()
if __name__ == "__main__":
    main()


