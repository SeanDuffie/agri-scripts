import requests

def post_webhook(url: str) -> None:
    """ Posts to the specified webhook

    TODO: At the moment the post doesn't contain data, however it can be added in the form of a JSON, example is shown below in commented code.

    Args:
        url (str): Destination URL for webhook
    """
    requests.post(url)

    ## Example for a JSON attached to Post webhook
    # dat = { 'name': 'This is an example for webhook' }
    # requests.post(url, data=json.dumps(dat), headers={'Content-Type': 'application/json'})
