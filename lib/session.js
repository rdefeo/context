var
  mongoClient = require('mongodb').MongoClient,
  _ = require('underscore');
  
var mongoUri = process.env.MONGOHQ_CONTEXT_URL || "mongodb://localhost/context";

var pushToDoc = function(doc, item){
  if(item && item.data && item.data.type){
    if (!doc[item.data.type]){
      doc[item.data.type] = [];
    }
    var data = item.data;
    data.timestamp = item.timestamp;
    doc[item.data.type].push(data);
  }
  return doc;
}

// for now just data access but will soon be doing some aging of older items
exports.get = function (req, res) {
  console.log("app=context,module=session,function=get,sessionID=%s", req.params.sessionID);
  mongoClient.connect(mongoUri, function (err, db) {
    if (err){
      console.error("app=context,module=session,function=get,resource=mongo,error=%s", err);
    }
    var doc = {};
    db.collection("sessions").find(
      {
        sessionID: req.params.sessionID
      }).toArray(function(err, items) {
        for (i in items) {
          console.dir(items[i]);
          doc = pushToDoc(doc, items[i]);
          
        }
        doc.sessionID= req.params.sessionID
        res.json(doc);
    });
    
  });
};

// TODO: be clever with validatation to not let a load of junk in
exports.post = function (req, res) {
  console.log("app=context,module=session,function=post,uuid=%s,sessionID=%s,data=%s", req.query.uuid, req.params.sessionID, JSON.stringify(req.body));
  if (!req.query.uuid) {
    res.status(412).json({error: "Missing parameter: 'uuid'"});
  }
  if (! _.isArray(req.body)) {
    res.status(412).json({error: "body is not array"});
  }
 
  mongoClient.connect(mongoUri, function (err, db) {
    if (err){
      console.error("app=context,module=session,function=post,resource=mongo,error=%s", err);
    } 
    var docs = [];
    for (i in req.body){
      var data = {}
      data.sessionID = req.params.sessionID;
      data.uuid = req.query.uuid;
      data.timestamp = new Date().toISOString();
      data.data = req.body[i];      
      docs.push(data);
    }     
    
    db.collection("sessions").insert(
      docs,
      function (err, data) {        
        if (err){
          console.error("app=context,module=session,function=post,resource=mongo,error=%s", err);
          throw err;
        }
        res.send(201);
    });      
  });
};