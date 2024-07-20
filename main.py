from services.osb_http_services import OsbHttpService

def main() -> None:
    service = OsbHttpService()
    service.get_services_files('')
    
if __name__ == "__main__":
    main()


