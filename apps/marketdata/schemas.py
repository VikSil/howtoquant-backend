new_price_request = {
    "type": "object",
    "properties": {
        "tickers": {"type": "array"},
        "date_from": {"type": "string", "format": "date"},
        "date_to": {"type": "string", "format": "date"},
    },
    "required": ["tickers", "date_from", "date_to"],
    "additionalProperties": False,
}

download_save_request = {
    "type": "object",
    "properties": {"download_id": {"type": "integer"}, "options": {"enum": ["missing", "overrideall"]}},
    "required": ["download_id", "options"],
    "additionalProperties": False,
}
