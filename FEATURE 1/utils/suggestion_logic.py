def generate_suggestions(input_data, predicted_bill):
    suggestions = []
    reasons = []

    units = input_data["units_used"]
    peak = input_data["peak_hours_usage"]
    lighting = input_data["lighting_type"]
    appliances = input_data["appliance_count"]

    # High usage detection
    if units > 350:
        reasons.append("High total electricity usage detected")
        suggestions.append("Reduce unnecessary appliance usage")

    if peak > 120:
        reasons.append("High peak-hour consumption")
        suggestions.append("Shift heavy appliances to non-peak hours")

    if lighting == "Bulb":
        reasons.append("Inefficient lighting type used")
        suggestions.append("Switch to LED lights to save energy")

    if appliances > 8:
        reasons.append("Too many appliances connected")
        suggestions.append("Unplug unused appliances")

    # Safety fallback
    if not suggestions:
        suggestions.append("Your electricity usage is efficient. Keep it up!")

    return {
        "predicted_bill": int(predicted_bill),
        "reasons": reasons,
        "suggestions": suggestions
    }
