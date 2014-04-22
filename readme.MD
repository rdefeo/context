####Environment variables
Run from app directory
````
dokku config:set context MONGOHQ_CONTEXT_URL="mongodb://context:context@dharma.mongohq.com:10064/context"
````



curl -d '[{"type":"colour","value":"white","method":"exact"}]' -H "Content-Type: application/json" http://127.0.0.1:5002/session/213243?uuid=12345423