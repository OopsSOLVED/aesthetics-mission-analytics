"""
Generate sample dataset for AESTHETICS MISSION Dashboard demo.
Run: python generate_sample_data.py
Output: sample_leads_data.csv
"""
import pandas as pd
import numpy as np
from datetime import datetime

np.random.seed(42)
n = 500

cities = ["Kozhikode", "Kochi", "Thiruvananthapuram", "Thrissur", "Kannur",
          "Palakkad", "Alappuzha", "Kollam", "Kottayam", "Malappuram"]

city_coords = {
    "Kozhikode": (11.2588, 75.7804), "Kochi": (9.9312, 76.2673),
    "Thiruvananthapuram": (8.5241, 76.9366), "Thrissur": (10.5276, 76.2144),
    "Kannur": (11.8745, 75.3704), "Palakkad": (10.7867, 76.6548),
    "Alappuzha": (9.4981, 76.3388), "Kollam": (8.8932, 76.6141),
    "Kottayam": (9.5916, 76.5222), "Malappuram": (11.0510, 76.0711),
}

sources = ["Google Ads", "Facebook", "Instagram", "Referral", "Website",
           "Walk-in", "WhatsApp", "JustDial", "IndiaMART", "YouTube"]
departments = ["Residential", "Commercial", "Modular Kitchen",
               "Office Interiors", "Renovation"]
persons = ["Arun K", "Priya M", "Rahul S", "Sneha B", "Vijay R",
           "Divya N", "Ajith P", "Meera T", "Suresh L", "Anjali D"]
work_types = ["Modern Kitchen", "Traditional Living Room", "Office Cabin",
              "Bedroom Design", "Bathroom Renovation", "Full Home Interior",
              "Modular Wardrobe", "False Ceiling", "Commercial Space", "Pooja Room"]
business_types = ["Individual", "Small Business", "Corporate", "Builder",
                  "Architect Referral"]
stages = ["Won", "Lost", "Follow-up", "Negotiation", "Site Visit",
          "Quotation Sent", "Design Phase"]

# Kerala first names and surnames for realistic data
first_names = ["Arun", "Priya", "Mohammed", "Lakshmi", "Suresh", "Anjali",
               "Rajesh", "Deepa", "Vijay", "Meera", "Asif", "Kavitha",
               "Rajan", "Sreelatha", "Thomas", "Fathima", "Gopal", "Nisha",
               "Abdul", "Shyamala", "Santhosh", "Rekha", "Manoj", "Suma",
               "Anoop", "Divya", "Sabu", "Smitha", "Babu", "Thankam"]
surnames = ["Nair", "Menon", "Pillai", "Kumar", "Varma", "Das", "Kurup",
            "Panicker", "Namboothiri", "Iyer", "Patel", "Thomas", "George",
            "Joseph", "Abraham", "Khan", "Hassan", "Sharma", "Krishnan", "Warrier"]
businesses = ["Homes", "Builders", "Properties", "Interiors", "Associates",
              "Enterprises", "Constructions", "Developers", "Group", "LLP"]

dates = pd.date_range(start="2023-01-01", end="2025-12-31", periods=n)
chosen_cities = np.random.choice(cities, n)

customer_names = [f"{np.random.choice(first_names)} {np.random.choice(surnames)}" for _ in range(n)]
business_names = [
    f"{np.random.choice(first_names)} {np.random.choice(businesses)}" if np.random.random() > 0.35 else ""
    for _ in range(n)
]

data = {
    "sl_no": range(1, n + 1),
    "date": dates,
    "source_of_leads": np.random.choice(sources, n, p=[0.2, 0.15, 0.12, 0.15, 0.1, 0.08, 0.07, 0.05, 0.05, 0.03]),
    "department": np.random.choice(departments, n, p=[0.35, 0.2, 0.2, 0.15, 0.1]),
    "alloted_person": np.random.choice(persons, n),
    "contact_no": [f"9{np.random.randint(100000000, 999999999)}" for _ in range(n)],
    "customer_name": customer_names,
    "customer_business_name": business_names,
    "business_type": np.random.choice(business_types, n),
    "latitude": [city_coords[c][0] + np.random.uniform(-0.05, 0.05) for c in chosen_cities],
    "longitude": [city_coords[c][1] + np.random.uniform(-0.05, 0.05) for c in chosen_cities],
    "city": chosen_cities,
    "work_requirement": np.random.choice(work_types, n),
    "year": [d.year for d in dates],
    "month": [d.month for d in dates],
    "phone_valid": np.random.choice([True, False], n, p=[0.92, 0.08]),
    "is_duplicate_lead": np.random.choice([True, False], n, p=[0.07, 0.93]),
    "stage_clean_norm": np.random.choice(stages, n, p=[0.25, 0.2, 0.15, 0.12, 0.1, 0.1, 0.08]),
    "final_lead_stage": np.random.choice(stages, n, p=[0.28, 0.18, 0.14, 0.12, 0.1, 0.1, 0.08]),
}

df = pd.DataFrame(data)

# Revenue: higher for Won leads, zero for Lost
revenue = []
for _, row in df.iterrows():
    if row["final_lead_stage"] == "Won":
        revenue.append(np.random.randint(50000, 2500000))
    elif row["final_lead_stage"] == "Lost":
        revenue.append(0)
    else:
        revenue.append(np.random.choice([0, np.random.randint(10000, 500000)]))
df["Revenue"] = revenue

# Format date
df["date"] = df["date"].dt.strftime("%Y-%m-%d")

df.to_csv("sample_leads_data.csv", index=False)
print(f"✅ Generated sample_leads_data.csv with {len(df)} records")
print(f"   Columns: {list(df.columns)}")
print(f"   Total Revenue: ₹{df['Revenue'].sum():,.0f}")
print(f"   Cities: {df['city'].nunique()}")
print(f"   Date Range: {df['date'].min()} to {df['date'].max()}")
