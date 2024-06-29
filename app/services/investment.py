from datetime import datetime


def process_investments(target, source) -> list:
    updated_source = list()
    for obj in source:
        if target.fully_invested:
            break

        target_amount = target.full_amount - target.invested_amount
        obj_amount = obj.full_amount - obj.invested_amount

        if (target_amount > obj_amount):
            amount = obj_amount
        else:
            amount = target_amount

        target.invested_amount += amount
        if target.invested_amount == target.full_amount:
            target.fully_invested = True
            target.close_date = datetime.now()

        obj.invested_amount += amount
        if obj.invested_amount == obj.full_amount:
            obj.fully_invested = True
            obj.close_date = datetime.now()
        updated_source.append(obj)

    return [target, *updated_source]
