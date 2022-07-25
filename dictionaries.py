from locale import currency


fund_names = {
    "necessary_costs": "🏠 Необхідні витрати",
    "food_and_entertainment": "😋 Їжа та розваги",
    "important_expenditures": "👨‍👩‍👦 Дорогі та важливі покупки",
    "for_future": "🌟 Мабутнє"
}

fund_distribution = {
    "necessary_costs": {"money_value": 300, "currency": "EUR"},
    "food_and_entertainment": {"money_value": 300, "currency": "EUR"},
    "important_expenditures": {"money_value": 600, "currency": "EUR"},
    "for_future": {"money_value": 400, "currency": "EUR"}
}

fund_categories = {
    "necessary_costs": ["flat_rent", 
                        "utilities", 
                        "internet", 
                        "mobile_phone",
                        "1_other"],
    "food_and_entertainment": ["regular_food", 
                               "restaurant_food", 
                               "coffee", 
                               "cinema",
                               "books", 
                               "2_other"],
    "important_expenditures": ["clothes",
                               "electronic_devices",
                               "furniture",
                               "cleaning",
                               "medicine",
                               "baby",
                               "education",
                               "road",
                               "post",
                               "charity",
                               "travelling",
                               "3_other"],
    "for_future":["for_future"]
}


category_fund = {}
for fund in fund_categories:
    for category in fund_categories[fund]:
        category_fund[category] = fund


transaction_name_category = {
    
    "flat_rent":"🏠 Квартплата",
    "utilities":"🏠 Комунальні послуги",
    "internet":"🏠 Інтернет",
    "mobile_phone":"🏠 Тариф за мобільний телефон",
    "1_other":"🏠 Інше",
    
    "regular_food":"😋 Продукти",
    "restaurant_food":"😋 Їжа з ресторанів",
    "coffee":"😋 Кава",
    "cinema":"😋 Кіно",
    "books":"😋 Книги",
    "2_other": "😋 Інше",

    "clothes":"👨‍👩‍👦 Одяг",
    "electronic_devices":"👨‍👩‍👦 Електронна техніка",
    "furniture":"👨‍👩‍👦 Меблі і товари для дому",
    "cleaning":"👨‍👩‍👦 Чистота і прибирання",
    "medicine":"👨‍👩‍👦 Лікування",
    "baby":"👨‍👩‍👦 Вагітність та догляд за дитиною",
    "education":"👨‍👩‍👦 Освіта",
    "road":"👨‍👩‍👦 Дорога",
    "post":"👨‍👩‍👦 Поштові відправлення",
    "charity":"👨‍👩‍👦 Благодійність",
    "travelling":"👨‍👩‍👦 Подорожі та відпустки",
    "3_other": "👨‍👩‍👦 Інше",

    "for_future":"🌟 Майбутнє"
}

