currencyNameToSymbol = {
    "USD": "$",
    "EUR": "€",
    "BRL": "R$",
    "CNY": "¥",
    "INR": "₹",
    "MYR": "RM",
    "PLN": "zł",
    "KRW": "₩",
    "THB": "฿",
    "GBP": "£",
    "HKD": "HK$"
}

supportedCurrencies = list(currencyNameToSymbol.keys())

currencySymbolToName = {
    "$": "USD",
    "€": "EUR",
    "R$": "BRL",
    "¥": "CNY",
    "₹": "INR",
    "RM": "MYR",
    "zł": "PLN",
    "₩": "KRW",
    "฿": "THB",
    "£": "GBP",
    "HK$": "HKD"
}

supportedCurrencySymbols = list(currencySymbolToName.keys())

currencySymbolToLocale = {
    "$": "en_US",
    "€": "fr_FR",
    "R$": "pt_BR",
    "¥": "zh_CN",
    "₹": "en_IN",
    "RM": "en_MY",
    "zł": "pl_PL",
    "₩": "ko_KR",
    "฿": "th_TH",
    "£": "en_GB",
    "HK$": "zh_HK"
}

currencyNameToLocale = {
    "USD": "en_US",
    "EUR": "fr_FR",
    "BRL": "pt_BR",
    "CNY": "zh_CN",
    "INR": "en_IN",
    "MYR": "en_MY",
    "PLN": "pl_PL",
    "KRW": "ko_KR",
    "THB": "th_TH",
    "GBP": "en_GB",
    "HKD": "zh_HK"
}
