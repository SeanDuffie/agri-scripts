import requests

def post_webhook(url: str) -> None:
    """
    Temp Docstring
    """
    # dat = { 'name': 'This is an example for webhook' }
    # requests.post(url, data=json.dumps(dat), headers={'Content-Type': 'application/json'})
    requests.post(url)


