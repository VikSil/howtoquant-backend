new_instrument_request = {
    "type": "object",
    "properties": {
        "ticker": {"type": "string"},
        "service": {"enum": ["polygon.io"]},
    },
    "required": ["ticker", "service"],
    "additionalProperties": False,
}
 
new_organization = {
    "type": "object",
    "properties": {
        "org_type": {"type": "string"},
        "name": {"type": "string"},
        "long_name": {"type": "string"},
        "description": {"type": "string"},
    },
    "required": ["org_type","name"],
    "additionalProperties": False,
}
