new_instrument = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "minLength": 1},
        "long_name": {"type": "string"},
        "class_name": {"type": "string", "minLength": 1},
        "domicile": {"type": "string", "minLength": 1},
        "ccy": {"type": "string", "minLength": 1},
        "ticker": {"type": "string", "minLength": 1},
        "ticker_type": {"type": "string", "minLength": 1},
        "issuer_name": {"type": "string", "minLength": 1},
    },
    "required": ["name", "class_name", "ccy", "issuer_name"],
    "additionalProperties": False,
}

new_instrument_request = {
    "type": "object",
    "properties": {
        "ticker": {"type": "string", "minLength": 1},
        "service": {"enum": ["polygon.io"]},
    },
    "required": ["ticker", "service"],
    "additionalProperties": False,
}

new_organization = {
    "type": "object",
    "properties": {
        "org_type": {"type": "string", "minLength": 1},
        "name": {"type": "string", "minLength": 1},
        "long_name": {"type": "string"},
        "description": {"type": "string"},
        "owner_org": {"type": "string", "minLength": 1},
        "owner_org_type": {"type": "string", "minLength": 1},
    },
    "required": ["org_type", "name"],
    "additionalProperties": False,
}
