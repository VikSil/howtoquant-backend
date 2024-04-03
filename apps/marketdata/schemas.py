new_price_request = {
    "type": "object",
    "properties": {
        "ticker": {"type": "string"},
        "date_from": {"type": "string", "format": "date"},
        "date_to": {"type": "string", "format": "date"},
    },
    "required": [
        "ticker",
        "date_from",
        "date_to"
    ],
    "additionalProperties":False
}
