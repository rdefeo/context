__author__ = 'robdefeo'


class Contextualizer(object):
    def contextualize(self, user_id, session_id, detection_result):
        # TODO get global context
        if detection_result is None:
            return {
                "entities": [
                    {
                        "type": "popular",
                        "key": "popular",
                        "weighting": 1.0
                    }
                ]
            }
        else:
            raise NotImplemented("")

        # TODO get user context
        # TODO get user context
        # TODO get detection context