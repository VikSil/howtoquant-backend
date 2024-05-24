new_pbaccount = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "external_name": {"type": "string"},
        "cash_account": {"type": "boolean"},
        "broker_name": {"type": "string"},
        "fund_name": {"type": "string"},
    },
    "required": ["name", "cash_account", "broker_name", "fund_name"],
    "additionalProperties": False,
}


new_strategy = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
    },
    "required": ["name"],
    "additionalProperties": False,
}
