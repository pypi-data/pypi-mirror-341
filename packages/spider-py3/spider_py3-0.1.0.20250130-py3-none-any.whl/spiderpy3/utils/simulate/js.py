import json


class JSON(object):

    @classmethod
    def stringify(cls, value):
        return json.dumps(
            value,
            ensure_ascii=False,
            separators=(",", ":")
        )
