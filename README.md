# NZO Model

## Current TODOs:
- [ ] Connect prices graphs to real data (Google Sheet)
- [ ] Fix `interpolate` function, or use the pandas one
- [ ] Change the design of the input fields
- [ ] Tooltips in Hebrew on each column header

## How to run:
1. Make sure you have a valid `credentials.json` under the `sources/` directory. You can use the template to create one. Full explanation in `sources/README`
2. `pip install -r requirements.txt`   
3. `python app.py`

## Configuring credentials.json
Google sheets api relies on a file called `credentials.json`  

Configure the authentication:

- `cp ./sources/credentials.template.json ./sources/credentials.json`
- in the new file `credentials.json`, set `"client_secret"` to the desired secret
- when running scripts relying on `sheets_api.py`, working directory should be module root (nzo-model)
