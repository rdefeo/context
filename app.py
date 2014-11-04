# import traceback
# from flask import Flask, jsonify, request, abort
# # from flask.ext.cors import cross_origin
# from bson.objectid import ObjectId
#
# app = Flask(__name__)
#
# @app.route('/session/<sessionID>/', methods = ['POST'])
# # @cross_origin()
# def post(sessionID):
#   try:
#     uuid = request.args.get("uuid")
#     body = request.get_json(force=True)
#
#     if not uuid or not sessionID or not type(body) == list:
#       resp = jsonify({
#         "status": "error",
#         "message": "missing param(s) / body",
#         "uuid": uuid,
#         "body": body
#       })
#       resp.status_code = 412
#       return resp
#     else:
#       pass
#   # console.log("app=context,module=session,function=post,uuid=%s,sessionID=%s,data=%s", req.query.uuid, req.params.sessionID, JSON.stringify(req.body));
#   # if (!req.query.uuid) {
#   #   res.status(412).json({error: "Missing parameter: 'uuid'"});
#   # }
#   # if (! _.isArray(req.body)) {
#   #   res.status(412).json({error: "body is not array"});
#   # }
#   except Exception,e:
#     print "error=%s" % (traceback.format_exc())
#     resp = jsonify({
#       "status": "error",
#       "exception": traceback.format_exc()
#     })
#     resp.status_code = 500
#     return resp
#
#
# if __name__ == '__main__':
#   app.run(host='0.0.0.0', debug=True)
