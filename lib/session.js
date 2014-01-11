var
  mongoClient = require('mongodb').MongoClient,
  _ = require('underscore');
  
var mongoUri = process.env.MONGOHQ_CONTEXT_URL || "mongodb://localhost/context";

var db;
mongoClient.connect(mongoUri, function (err, connectedDb) {
  if (err){
    console.error("app=context,module=session,function=get,resource=mongo,error=%s", err);
  }
  db = connectedDb;
});
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
exports.newestUnique = function(items) {
  var sorted = _.sortBy(items, function(item){ return -new Date(item.timestamp).getTime(); });
  // its sorted by something else not what the unique iterator is going to use
  return _.uniq(sorted, false, function(item) { return item.data.type + "_" + item.data.value});
}
exports.processItems = function(items) {
  var min = new Date(_.min(items, function(item){ return new Date(item.timestamp).getTime(); }).timestamp).getTime();
  var max = new Date(_.max(items, function(item){ return new Date(item.timestamp).getTime(); }).timestamp).getTime();
  
  for(i in items){
    var item = items[i];
    item.ageScore = ((min == max) ? 0.5 : ((new Date(item.timestamp).getTime() - min) / (max - min)));
  }
  return items;
};
// for now just data access but will soon be doing some aging of older items
exports.get = function (req, res) {
  console.log("app=context,module=session,function=get,sessionID=%s", req.params.sessionID);

  var doc = {};
  db.collection("sessions").find(
    {
      sessionID: req.params.sessionID
    }).toArray(function(err, items) {
      console.dir(items);
      for (i in items) {
        doc = pushToDoc(doc, items[i]);          
      }
      var docKeys = _.keys(doc);
      for (docKeyCounter in docKeys){
        var min = new Date(_.min(doc[docKeys[docKeyCounter]], function(item){ return new Date(item.timestamp).getTime(); }).timestamp).getTime();
        var max = new Date(_.max(doc[docKeys[docKeyCounter]], function(item){ return new Date(item.timestamp).getTime(); }).timestamp).getTime();
        
        for (i in doc[docKeys[docKeyCounter]]){
          var item = doc[docKeys[docKeyCounter]][i];
          item.ageScore = ((min == max) ? 0.5 : ((new Date(item.timestamp).getTime() - min) / (max - min))) + 1;
        }
        // min.equals(max) ? 0.5 : (originalStrength - min) / (max - min);
        
      }
      
      doc.sessionID= req.params.sessionID
      res.json(doc);
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

};