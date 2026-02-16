def check_aml(amount, country, previous_transactions_count):
    aml_flags = []

    # Rule 1: High value transaction
    if amount > 200000:
        aml_flags.append("High Value Transaction")

    # Rule 2: Foreign transfer
    if country != "India":
        aml_flags.append("Foreign Transfer")

    # Rule 3: Repeated transfers
    if previous_transactions_count >= 3:
        aml_flags.append("Repeated Transfers")

    return aml_flags
