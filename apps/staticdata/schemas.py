new_instrument_request = {
    "type": "object",
    "properties": {
        "ticker": {"type": "string"},
        "service": {"enum": ["polygon.io"]},
    },
    "required": ["ticker", "service"],
    "additionalProperties": False,
}
