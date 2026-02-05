import pandas as pd
import numpy as np
import random

# Complete Sub-Type Configuration
appliance_config = {
    'Air Conditioner': [('Split Inverter', 48000), ('Split Non-Inverter', 38000), ('Window', 32000)],
    'Refrigerator': [('Double Door', 32000), ('Single Door', 18000), ('Side-by-Side', 85000)],
    'Washing Machine': [('Front Load', 35000), ('Top Load', 22000), ('Semi-Automatic', 14000)],
    'Smart TV': [('OLED', 110000), ('QLED', 55000), ('LED', 24000)],
    'Ceiling Fan': [('BLDC Motor', 3500), ('Induction Motor', 1800)],
    'LED Light': [('Smart LED', 800), ('Batten/Tube', 450), ('Panel Light', 600)],
    'Microwave Oven': [('Convection', 16000), ('Grill', 11000), ('Solo', 7000)],
    'Water Purifier': [('RO + UV + MTDS', 15000), ('UV + UF', 9000), ('Gravity/Non-Electric', 3000)],
    'Mixer Grinder': [('Food Processor', 9000), ('Juicer Mixer (JMG)', 5500), ('Standard 3-Jar', 3500)]
}

brands = ['LG', 'Samsung', 'Daikin', 'Havells', 'Philips', 'Bosch', 'Atomberg', 'Pureit', 'Preethi']
data = []

for i in range(1, 501):
    cat = random.choice(list(appliance_config.keys()))
    sub_type, base_price = random.choice(appliance_config[cat])
    brand = random.choice(brands)
    stars = random.choice([3, 4, 5])
    
    # 2026 Energy Logic: Annual kWh Estimate
    # (High stars = Lower kWh; Complex appliances = Higher kWh)
    efficiency_factor = (6 - stars) * 0.15 
    kwh_est = (base_price / 100) * efficiency_factor
    
    # Adjusting price for 2026 inflation & Star Rating premium
    final_price = base_price * (1 + (stars - 3) * 0.08) + random.randint(-500, 1500)

    data.append({
        'Appliance_ID': f"IND-2026-{i:03}",
        'Category': cat,
        'Sub_Type': sub_type,
        'Brand': brand,
        'Star_Rating': stars,
        'Price_INR': round(final_price, -1),
        'Annual_kWh': round(kwh_est, 1),
        'Use_Case': "Energy Saver" if stars == 5 else "Value for Money",
        'Investment_Type': "One-time Premium" if stars == 5 or 'BLDC' in sub_type or 'Inverter' in sub_type else "Standard"
    })

df = pd.DataFrame(data)
df.to_csv('Indian_Home_2026_Total.csv', index=False)
print("500-row Master Dataset Generated!")