from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# --- YOUR LOGIC CLASS ---
class ApplianceAdvisor:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)
        self.family_map = {
            'Small': {
                'Refrigerator': 'Single Door', 'Washing Machine': 'Semi-Automatic',
                'Air Conditioner': 'Window', 'Smart TV': 'LED', 'Water Purifier': 'Gravity/Non-Electric'
            },
            'Medium': {
                'Refrigerator': 'Double Door', 'Washing Machine': 'Top Load',
                'Air Conditioner': 'Split Non-Inverter', 'Smart TV': 'QLED', 'Water Purifier': 'UV + UF'
            },
            'Large': {
                'Refrigerator': 'Side-by-Side', 'Washing Machine': 'Front Load',
                'Air Conditioner': 'Split Inverter', 'Smart TV': 'OLED', 'Water Purifier': 'RO + UV + MTDS'
            }
        }

    def suggest(self, appliances_needed, family_size, usage_level, total_budget):
        suggestions = []
        for category in appliances_needed:
            cat_df = self.df[self.df['Category'] == category].copy()
            preferred_sub_type = self.family_map.get(family_size, {}).get(category)
            
            if preferred_sub_type and preferred_sub_type in cat_df['Sub_Type'].values:
                cat_df = cat_df[cat_df['Sub_Type'] == preferred_sub_type]
            
            if usage_level == 'Heavy':
                cat_df = cat_df.sort_values(by=['Star_Rating', 'Annual_kWh'], ascending=[False, True])
                reason = "Heavy usage: High star-rating prioritized for long-term savings."
            elif usage_level == 'Medium':
                cat_df = cat_df.sort_values(by=['Star_Rating', 'Price_INR'], ascending=[False, True])
                reason = "Medium usage: Balanced efficiency and price."
            else:
                cat_df = cat_df.sort_values(by='Price_INR', ascending=True)
                reason = "Light usage: Value-focused model selected."

            if not cat_df.empty:
                match = cat_df.iloc[0].to_dict()
                match['Reason'] = reason
                suggestions.append(match)

        total_cost = sum(item['Price_INR'] for item in suggestions)
        
        # Budget Check
        if total_cost > total_budget:
            suggestions = sorted(suggestions, key=lambda x: x['Price_INR'], reverse=True)
            for i, item in enumerate(suggestions):
                if total_cost <= total_budget: break
                alt_df = self.df[(self.df['Category'] == item['Category']) & (self.df['Use_Case'] == 'Value for Money')]
                if not alt_df.empty:
                    cheapest_alt = alt_df.sort_values(by='Price_INR').iloc[0].to_dict()
                    if cheapest_alt['Price_INR'] < item['Price_INR']:
                        total_cost -= (item['Price_INR'] - cheapest_alt['Price_INR'])
                        cheapest_alt['Reason'] = "Budget optimized: Swapped to a Value-for-Money model."
                        suggestions[i] = cheapest_alt
        
        return suggestions, total_cost

# --- FLASK ROUTES ---
advisor = ApplianceAdvisor('Indian_Home_2026_Total.csv')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_suggestion', methods=['POST'])
def get_suggestion():
    data = request.json
    # Convert budget to integer safely
    user_budget = int(data.get('budget', 150000))
    
    suggestions, total_cost = advisor.suggest(
        data['appliances'], 
        data['familySize'], 
        data['usageLevel'], 
        user_budget
    )
    return jsonify({'suggestions': suggestions, 'total_cost': total_cost})

if __name__ == '__main__':
    app.run(debug=True)
    
    
    
    
# --- Example Execution ---
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
print(f"BUDGET STATUS: {'Within Budget' if final_price <= budget else 'Exceeds Budget'}")