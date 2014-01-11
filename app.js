var 
  express = require('express'),
  pjson = require('./package.json'),  
  session = require('./lib/session')
  
var app = express();

app.use(express.json());
app.use(express.urlencoded());
app.use(express.compress());

// Add headers
app.use(function (req, res, next) {
    // Website you wish to allow to connect
    // res.setHeader('Access-Control-Allow-Origin', 'http://localhost:8888');
    res.header("Access-Control-Allow-Origin", "*");  
    
    // res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST');
    // Request headers you wish to allow
    res.setHeader('Access-Control-Allow-Headers', 'X-Requested-With,content-type');

    // // Set to true if you need the website to include cookies in the requests sent
    // // to the API (e.g. in case you use sessions)
    // res.setHeader('Access-Control-Allow-Credentials', true);

    // Pass to next layer of middleware
    next();
});

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