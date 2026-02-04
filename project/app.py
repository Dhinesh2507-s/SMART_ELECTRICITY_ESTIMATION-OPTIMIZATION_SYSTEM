import pandas as pd

class ApplianceAdvisor:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)
        
        # Mapping Family Size to Sub_Types (Capacity Logic)
        self.family_map = {
            'Small': {
                'Refrigerator': 'Single Door',
                'Washing Machine': 'Semi-Automatic',
                'Air Conditioner': 'Window',
                'Mixer Grinder': 'Standard 3-Jar',
                'Water Purifier': 'Gravity/Non-Electric',
                'Smart TV': 'LED'
            },
            'Medium': {
                'Refrigerator': 'Double Door',
                'Washing Machine': 'Top Load',
                'Air Conditioner': 'Split Non-Inverter',
                'Mixer Grinder': 'Juicer Mixer (JMG)',
                'Water Purifier': 'UV + UF',
                'Smart TV': 'QLED'
            },
            'Large': {
                'Refrigerator': 'Side-by-Side',
                'Washing Machine': 'Front Load',
                'Air Conditioner': 'Split Inverter',
                'Mixer Grinder': 'Food Processor',
                'Water Purifier': 'RO + UV + MTDS',
                'Smart TV': 'OLED'
            }
        }

    def suggest(self, appliances_needed, family_size, usage_level, total_budget):
        suggestions = []
        
        for category in appliances_needed:
            # 1. Filter by Category
            cat_df = self.df[self.df['Category'] == category].copy()
            
            # 2. Filter by Family Size (Sub_Type) if mapping exists
            preferred_sub_type = self.family_map.get(family_size, {}).get(category)
            if preferred_sub_type and preferred_sub_type in cat_df['Sub_Type'].values:
                cat_df = cat_df[cat_df['Sub_Type'] == preferred_sub_type]
            
            # 3. Filter/Sort by Usage Level
            if usage_level == 'Heavy':
                # Prioritize Energy Savers and High Star Rating
                cat_df = cat_df.sort_values(by=['Star_Rating', 'Annual_kWh'], ascending=[False, True])
                reason = "Heavy usage detected: Prioritized high star-rating and low energy consumption (ROI focused)."
            elif usage_level == 'Medium':
                cat_df = cat_df.sort_values(by=['Star_Rating', 'Price_INR'], ascending=[False, True])
                reason = "Balanced usage: Optimized for mid-range efficiency and cost."
            else: # Light
                cat_df = cat_df.sort_values(by='Price_INR', ascending=True)
                reason = "Light usage: Prioritized lower initial purchase price (Value for Money)."

            # Select the top match
            if not cat_df.empty:
                match = cat_df.iloc[0].to_dict()
                match['Reason'] = reason
                suggestions.append(match)

        # 4. Budget Check & Optimization
        total_cost = sum(item['Price_INR'] for item in suggestions)
        if total_cost > total_budget:
            # Optimization logic: swap most expensive items for cheaper alternatives until budget fits
            suggestions = sorted(suggestions, key=lambda x: x['Price_INR'], reverse=True)
            for i, item in enumerate(suggestions):
                if total_cost <= total_budget:
                    break
                
                # Try to find a 'Value for Money' alternative in the same category
                alt_df = self.df[(self.df['Category'] == item['Category']) & 
                                 (self.df['Use_Case'] == 'Value for Money')]
                if not alt_df.empty:
                    cheapest_alt = alt_df.sort_values(by='Price_INR').iloc[0].to_dict()
                    if cheapest_alt['Price_INR'] < item['Price_INR']:
                        total_cost -= (item['Price_INR'] - cheapest_alt['Price_INR'])
                        cheapest_alt['Reason'] = "Budget constraint: Swapped to a Value-for-Money model."
                        suggestions[i] = cheapest_alt

        return suggestions, total_cost

"""# --- Example Execution ---
advisor = ApplianceAdvisor('Indian_Home_2026_Total.csv')

# User Inputs
needed = ['Refrigerator', 'Air Conditioner', 'Ceiling Fan', 'Washing Machine']
f_size = 'Medium'
u_level = 'Heavy'
budget = 120000

results, final_price = advisor.suggest(needed, f_size, u_level, budget)

print(f"--- Suggestion Strategy for {f_size} Family ({u_level} Usage) ---")
for r in results:
    print(f"\nAppliance: {r['Category']} ({r['Sub_Type']})")
    print(f"Brand: {r['Brand']} | Star Rating: {r['Star_Rating']}*")
    print(f"Price: ₹{r['Price_INR']:,} | Annual Power: {r['Annual_kWh']} kWh")
    print(f"Logic: {r['Reason']}")

print(f"\nTOTAL ESTIMATED QUOTE: ₹{final_price:,}")
print(f"BUDGET STATUS: {'Within Budget' if final_price <= budget else 'Exceeds Budget'}")"""