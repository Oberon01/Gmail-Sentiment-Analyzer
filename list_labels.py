from gmail_poll import get_service

def list_labels():
    service = get_service()
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])
    print("Available Gmail Labels:\n")
    for label in labels:
        print(f"{label['name']} → {label['id']}")

if __name__ == "__main__":
    list_labels()
