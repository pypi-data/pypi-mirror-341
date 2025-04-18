import click
import requests


@click.command()
@click.option("--token_url", default="https://testpads.constantvzw.org/oauth2/token") # https://provider.com/oauth2/token
@click.option("--client_id", default="murtaugh")
@click.option("--client_secret", default="mlmpass")
def main(token_url, client_id, client_secret):
    from oauthlib.oauth2 import BackendApplicationClient
    from requests_oauthlib import OAuth2Session

    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url=token_url, client_id=client_id,
            client_secret=client_secret)
    print (token)

    # data = {'grant_type': 'client_credentials', 'client_id': 'client_credentials', 'client_secret':'client_credentials'}
    # resp = requests.post(
    #     "http://localhost:9001/oidc/token",
    #     headers={'content-type': 'application/x-www-form-urlencoded', },
    #     data=data
    # )
    # print (resp)


    # curl --request POST --url '' --header 'content-type: application/x-www-form-urlencoded' --data grant_type=client_credentials --data client_id=client_credentials --data client_secret=client_credentials
