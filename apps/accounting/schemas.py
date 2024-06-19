new_book = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "minLength": 1},
        "external_name": {"type": "string"},
        "acct_method": {"type": "string", "minLength": 1},
        "base_ccy": {"type": "string", "minLength": 1},
        "fund_name": {"type": "string", "minLength": 1},
        "default_account": {"type": "string", "minLength": 1},
    },
    "required": ["name", "acct_method", "base_ccy", "fund_name", "default_account"],
    "additionalProperties": False,
}


new_pbaccount = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "minLength": 1},
        "external_name": {"type": "string"},
        "cash_account": {"type": "boolean"},
        "broker_name": {"type": "string", "minLength": 1},
        "fund_name": {"type": "string", "minLength": 1},
    },
    "required": ["name", "cash_account", "broker_name", "fund_name"],
    "additionalProperties": False,
}


new_strategy = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "minLength": 1},
        "description": {"type": "string"},
    },
    "required": ["name"],
    "additionalProperties": False,
}

new_trade = {
    "type": "object",
    "properties":{
        "ticker":{"type": "string"},
        "direction":{"enum": ["B", "S","SS", "BC"]},
        "quantity":{"type": "number", "exclusiveMinimum": 0},
        "price":{"type": "number", "minimum": 0},
        "trade_date":{"type": "string","format": "date"},
        "trade_ccy":{"type": "string"},
        "settle_date":{"type": "string","format": "date"},
        "settle_ccy":{"type": "string"},
        "trade_settle_xrate":{"type": "number", "exclusiveMinimum": 0},
        "settle_base_xrate":{"type": "number", "exclusiveMinimum": 0},
        "book_name":{"type": "string"},
        "strategy_name":{"type": "string"},
        "account_name":{"type": "string"},
        "counterparty":{"type": "string"},      
    },
    "required":["ticker", "direction", "quantity", "price", "book_name", "strategy_name", "counterparty"],
    "additionalProperties": False,
}
