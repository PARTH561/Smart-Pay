def calculate_risk(amount, device_change, otp_failures):
    score = 0

    # High amount risk
    if amount > 100000:
        score += 40
    elif amount > 50000:
        score += 25

    # Device change risk
    if device_change:
        score += 30

    # OTP failure risk
    if otp_failures >= 3:
        score += 30
    elif otp_failures == 2:
        score += 15

    # Categorize risk
    if score >= 70:
        category = "High"
    elif score >= 40:
        category = "Medium"
    else:
        category = "Low"

    return score, category
