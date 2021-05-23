from O365 import Account
# the default protocol will be Microsoft Graph
# the default authentication method will be "on behalf of a user"
from creds import credentials

account = Account(credentials, tenant_id="233b013b-d83e-4f7a-86ff-f2e4e7e6946b")
if account.authenticate(scopes=['basic', 'calendar']):
   print('Authenticated!')