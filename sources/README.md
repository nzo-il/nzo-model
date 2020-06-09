google sheets api relies on a file called credentials.json

configure the authentication:

- `cp ./sources/credentials.template.json ./sources/credentials.json`
- in the new file `credentials.json`, set `"client_secret"` to the desired secret
- when running scripts relying on `sheets_api.py`, working directory should be module root (nzo-model)
