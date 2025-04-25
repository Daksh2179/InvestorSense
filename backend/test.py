from forecast_rules import generate_forecast

# Simulate input for a blue chip stock with bad sentiment
result = generate_forecast("TSLA", -0.75)
print(result)

# Try a different case
result2 = generate_forecast("PLTR", 0.85)
print(result2)
