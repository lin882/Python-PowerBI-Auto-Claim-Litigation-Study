import pandas as pd
import numpy as np

# Set random seed for consistent data generation
np.random.seed(42)

total_rows = 4000

# ==========================================
# 1. Spatial & Structural Framework (Connecticut Only)
# ==========================================
state_list = ['Connecticut'] * total_rows
system_list = ['No-Fault (PIP)'] * total_rows  # Connecticut operates under a hybrid system context

# Geolocation Matrix (Major transit nodes intersecting I-95, I-84, and I-91 corridors)
ct_geo = [
    ('06103', 'Hartford'), ('06511', 'New Haven'), ('06901', 'Stamford'),
    ('06702', 'Waterbury'), ('06040', 'Manchester'), ('06320', 'New London')
]
zip_list = []
city_list = []
for _ in range(total_rows):
    idx = np.random.randint(0, len(ct_geo))
    zip_list.append(ct_geo[idx][0])
    city_list.append(ct_geo[idx][1])

# Generate unique Claim IDs across 2024-2025
claim_ids = [f"CLM-CT-{np.random.choice(['2024', '2025'])}-{1000+i}" for i in range(total_rows)]

# Random dates distributed across 2024 and 2025
start_date = np.datetime64('2024-01-01')
end_date = np.datetime64('2025-12-31')
days_between = (end_date - start_date).astype(int)
dates_list = start_date + np.random.randint(0, days_between, total_rows)

# Operational Categories
time_categories = ['Public/Business Hours', 'Commute (Peak)', 'Off-Hours/Private Use']
time_list = np.random.choice(time_categories, total_rows, p=[0.5, 0.3, 0.2])
reporting_delay = np.round(np.random.exponential(scale=18, size=total_rows) + 0.5, 1)

# Driver Duty Breach Setup (p matches exact specifications)
breach_categories = [
    'Distracted Driving', 'Speeding', 'Impaired Driving', 'Driving with Defective Equipment',
    'Failure to Adjust to Weather or Road Conditions', 'Improper Lane Usage / Unsafe Lane Changes'
]
breach_probs = [0.15, 0.30, 0.25, 0.08, 0.12, 0.10]
breach_list = np.random.choice(breach_categories, total_rows, p=breach_probs)

# Polarized Liability Distribution Setup (90% are 0 or 100, 10% are 1-99)
# +5% Shift to absolute fault (100%) for high-risk driver breaches
base_liability_choices = np.random.choice(['zero', 'hundred', 'mid'], total_rows, p=[0.45, 0.45, 0.10])
liability_list = []

for i in range(total_rows):
    breach = breach_list[i]
    if breach in ['Distracted Driving', 'Speeding']:
        choice = np.random.choice(['zero', 'hundred', 'mid'], p=[0.41, 0.50, 0.09])
    else:
        choice = base_liability_choices[i]
        
    if choice == 'zero':
        liability_list.append(0.0)
    elif choice == 'hundred':
        liability_list.append(100.0)
    else:
        liability_list.append(np.round(np.random.uniform(1.0, 99.0), 2))

# ==========================================
# 2. Advanced Financial & Dependent Payout Logic
# ==========================================
# Uses a Beta distribution to naturally skew baseline payouts up to $115,000
payout_weights = np.random.beta(a=1.2, b=4.5, size=total_rows)
base_payouts = 100 + payout_weights * (115000 - 100)

liability_payouts = []
insured_liability_percent = np.array(liability_list)

for i in range(total_rows):
    fault = insured_liability_percent[i]
    base_amt = base_payouts[i]
    
    if fault == 0.0:
        # At 0% fault, our liability payout drops, reflecting localized PIP medical mandates.
        # It is bound realistically between a minimum of $100 and a $5,000 baseline cap.
        liability_payouts.append(int(np.random.uniform(100, 5000)))
    else:
        # If we share any fault (1-100%), scale the distribution cleanly up to $115,000
        # Multiplied by the fault ratio so higher fault shifts toward high financial severity
        scaled_amt = base_amt * (fault / 100.0)
        liability_payouts.append(int(np.clip(scaled_amt, 100, 115000)))

liability_payouts = np.array(liability_payouts)

# Feature: litigation_open is flags as 1 when Liability Payout is over $5,000, 0 otherwise
litigation_open = np.where(liability_payouts > 5000, 1, 0)

# Feature: Litigation Cost is fixed at exactly a 30% ratio of the final Liability Payout
litigation_costs = np.round(liability_payouts * 0.30, 0).astype(int)

# ==========================================
# 3. Resolution Timeline Realignment
# ==========================================
# Generates a standard normal curve centered tightly around 700 days, bounded strictly between 500 and 900
resolution_days = np.random.normal(loc=700, scale=80, size=total_rows)
resolution_days = np.clip(resolution_days, 500, 900).astype(int)

# ==========================================
# 4. Strict Subrogation Funnel Modeling
# ==========================================
# Claims are only eligible if corporate fault is low (<50%). 
# From those eligible, exactly 10% proceed to active subrogation. The win rate is fixed at 30%.
subro_outcome = ['N/A'] * total_rows
potential_savings = [0] * total_rows

eligible_indices = np.where(insured_liability_percent < 50)[0]
n_eligible = len(eligible_indices)
n_subro = int(n_eligible * 0.10)  # Exactly 10% of eligible claims enter the pipeline

subro_chosen_indices = np.random.choice(eligible_indices, n_subro, replace=False)

for idx in eligible_indices:
    if idx in subro_chosen_indices:
        is_success = np.random.choice(['Success', 'Failed'], p=[0.30, 0.70])  # 30% success rate
        subro_outcome[idx] = is_success
        if is_success == 'Success':
            # Recovered savings average between 50% and 90% of the initial initial payout
            potential_savings[idx] = int(np.round(liability_payouts[idx] * np.random.uniform(0.5, 0.9)))
    else:
        subro_outcome[idx] = 'N/A'

# Supplementary risk tags
uninsured_third_party = np.random.choice(['Yes', 'No'], total_rows, p=[0.08, 0.92])
crossed_tort = np.random.choice(['Yes', 'No'], total_rows, p=[0.22, 0.78])

# ==========================================
# 5. Data Asset Compilation & Export
# ==========================================
df = pd.DataFrame({
    'Claim_ID': claim_ids,
    'Accident_Date': dates_list,
    'State': state_list,
    'accident_city': city_list,
    'accident_zip_code': zip_list,
    'Legal_System': system_list,
    'Time_of_Day_Category': time_list,
    'driver_duty_breach': breach_list,
    'Reporting_Delay_Hours': reporting_delay,
    'Insured_liability_percent': liability_list,
    'Uninsured_Third_Party': uninsured_third_party,
    'Crossed_Tort_Threshold_MA_CT': crossed_tort,
    'Liability_Payout_USD': liability_payouts,
    'litigation_open': litigation_open,
    'Litigation_Cost_USD': litigation_costs,
    'Resolution_Timeline_Days': resolution_days,
    'Subrogation_Outcome': subro_outcome,
    'Potential_Savings_Recovered_USD': potential_savings
})

# Operational Delay Penalty Rule
delay_mask = df['Reporting_Delay_Hours'] > 48
df.loc[delay_mask, 'Liability_Payout_USD'] *= 1.35
df.loc[delay_mask, 'Litigation_Cost_USD'] *= 1.45


#df.to_csv('auto_claim_v2.csv', index=False)
df.to_excel('auto_claim_v2.xlsx', index=False)

print("Unified data pipeline execution complete! 'auto_claim_vs' successfully generated.")
