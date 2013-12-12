var 
  express = require('express'),
  session = require('./lib/session')
  
var app = express();

app.use(express.json());
app.use(express.urlencoded());
app.use(express.compress());

app.get('/status', function(req, res) {
  res.json({
    self: "up",
    version: pjson.version
  });
});

app.get('/session/:sessionID', session.get);
app.post('/session/:sessionID', session.post);


var port = process.env.PORT || 5002;
app.listen(port, function() {
  console.log("app=context,port=%d,mode=%s,action=started", port, app.settings.env);
});