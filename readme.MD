[![build status](https://ci.gitlab.com/projects/6619/status.png?ref=master)](https://ci.gitlab.com/projects/6619?ref=master)


curl -d '[{"type":"colour","value":"white","method":"exact"}]' -H "Content-Type: application/json" http://127.0.0.1:5002/session/213243?uuid=12345423


This will have to replace all the matching code in the website,

maybe it should do long polling?

#How it works
Open up a listen request, that will return queued items.
Queued items need a time out

##Listen
###Request
{
    "session_id":,
    "user_id":
}

###Response
New message Id
{
    "latest_message_id":

}


Send a request e.g. new detection, viewed result, etc
##New query

###Request
Either detection response
{

    "timestamp": "2015-03-17T16:23:14.706937",
    "detection_id": "550846e2bf5f60449d35a396",
    "session_id": "session_id",
    "intent": [
        {
            "type": "include",
            "entities":[
                {
                    "type": "style",
                    "key": "heels",
                    "source": "content"
                },
                {
                    "type": "color",
                    "key": "orange",
                    "source": "content"
                },
                {
                    "type": "color",
                    "key": "blue",
                    "source": "content"
                },
                {
                    "type": "style",
                    "key": "high heels",
                    "source": "content"
                },
                {
                    "type": "material",
                    "key": "fur",
                    "source": "content"
                }
            ]
        }
    ],
    "autocorrected_query": "white and blue high heels with fur and orange",
    "non_detections": [ ],
    "version": "1.0.0"
}

###Response


````
{
    "entities": [
        {
            "type": "color",
            "key": "black",
            "weighting": "-0.5"
        }
    ],
    "_id": "context_id",
    "timestamp": "2015-01-01"
}

````
