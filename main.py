import os
from services.osb_local_repos_services import Services

def main() -> None:
    service = Services(os.getcwd())
    service.get_services_files()
if __name__ == "__main__":
    main()


