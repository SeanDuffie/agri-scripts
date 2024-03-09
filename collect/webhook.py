""" @file       webhook.py
    @author     Sean Duffie
    @brief      Enables user to connect a Smart Plug to a lamp and activate it as a camera "flash"

    This requires an IFTTT account and a very simple script, later I will replace this with a
    hardware relay to avoid unnecessary third party applications and internet dependency.

    This function may also be useful in the future for further expansion with sending webhooks
    over the Flask webpage.
"""
import requests


def post_webhook(url: str) -> bool:
    """ Posts to the specified webhook

    TODO: At the moment the post doesn't contain data, however it can be added in the form of a JSON, example is shown below in commented code.

    Args:
        url (str): Destination URL for webhook

    Returns:
        bool: Returns False if there was an error
    """
    try:
        requests.post(url=url, data=None, headers=None, timeout=10)

        ## Example for a JSON attached to Post webhook
        # dat = { 'name': 'This is an example for webhook' }
        # requests.post(url, data=json.dumps(dat), headers={'Content-Type': 'application/json'})
        return True
    except requests.exceptions.ConnectionError:
        return False

if __name__ == "__main__":
    dest_url = input("Type or copy/paste URL of IFTTT webhook here: ")
    post_webhook(dest_url)
