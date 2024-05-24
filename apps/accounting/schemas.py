new_book = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "external_name": {"type": "string"},
        "acct_method": {"type": "string"},
        "base_ccy": {"type": "string"},
        "fund_name": {"type": "string"},
        "default_account": {"type": "string"},
    },
    "required": ["name", "acct_method", "base_ccy", "fund_name", "default_account"],
    "additionalProperties": False,
}


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
