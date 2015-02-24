[ ![Codeship Status for jemboo/context](https://codeship.com/projects/2e74dfe0-9e79-0132-f4bb-0a6e67eb63d6/status?branch=master)](https://codeship.com/projects/64837)

####Environment variables
Run from app directory
````
dokku config:set context MONGOHQ_CONTEXT_URL="mongodb://context:context@dharma.mongohq.com:10064/context"
````



curl -d '[{"type":"colour","value":"white","method":"exact"}]' -H "Content-Type: application/json" http://127.0.0.1:5002/session/213243?uuid=12345423