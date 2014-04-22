var
  mongoClient = require('mongodb').MongoClient,
  _ = require('underscore'),
  t = require ('../lib/session');
var mongoUri = process.env.MONGOHQ_CONTEXT_URL || "mongodb://localhost/context";

var db;
mongoClient.connect(mongoUri, function (err, connectedDb) {
  if (err){
    console.error("app=context,module=session,function=get,resource=mongo,error=%s", err);
  }
  db = connectedDb;
});

exports.newestUnique = function(items) {
  var mappedWithDateTime = _.map(items, function(item){ 
    item.datetime = new Date(item.timestamp); 
    return item; 
  });
  var sorted = _.sortBy(items, function(item){ return -new Date(item.timestamp).getTime(); });
  // its sorted by something else not what the unique iterator is going to use
  return _.uniq(sorted, false, function(item) { return item.data.type + "_" + item.data.value});
};

exports.groupedMinMax = function(items) {
  var newestUnique = this.newestUnique(items);

  var results = {
    items: newestUnique,
    max: -Infinity,
    min: Infinity
  };

  for (i in newestUnique) {
    var item = newestUnique[i]
    var timestamp = new Date(item.timestamp).getTime();
    if (timestamp > results.max) {
      results.max = timestamp;
    }
    if (timestamp < results.min) {
      results.min = timestamp;
    }
    if (!results.hasOwnProperty(item.data.type)) {
      results[item.data.type] = {
        max: -Infinity,
        min: Infinity        
      }
    }
    if (timestamp > results[item.data.type].max) {
      results[item.data.type].max = timestamp;
    }
    if (timestamp < results[item.data.type].min) {
      results[item.data.type].min = timestamp;
    }    
  }
  
  return results;
};
 
exports.processItems = function(items) {
  var minMaxResults = this.groupedMinMax(items);
  
  var ageScores = _.map(minMaxResults.items, function(item){
    var categoryAgeScore = ((minMaxResults[item.data.type].min == minMaxResults[item.data.type].max) ? 1 : ((new Date(item.timestamp).getTime() - minMaxResults[item.data.type].min) / (minMaxResults[item.data.type].max - minMaxResults[item.data.type].min))) + 1;
    
    return {
      ageScore: categoryAgeScore,
      type: item.data.type,
      value: item.data.value
    };
  })
  // an alternative is a summary object
  // var result = _.reduce(ageScores, function(memo, item){ 
  //   if (!memo.hasOwnProperty(item.type)){
  //     memo[item.type] = {};
  //   }
  //   memo[item.type][item.value] = item.ageScore;
  //   return memo;
  // }, {});

  return ageScores;
};

exports.get = function (req, res) {
  console.log("app=context,module=session,function=get,sessionID=%s", req.params.sessionID);

  var doc = {};
  db.collection("sessions").find(
    {
      sessionID: req.params.sessionID
    }).toArray(function(err, items) {

      var doc = t.processItems(items)
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