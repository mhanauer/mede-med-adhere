
import streamlit as st
import pandas as pd
import numpy as np

# Generate a dataframe with the required columns
data = {
    'member_id': range(1, 101),
    'age': np.random.randint(18, 85, size=100),
    'gender': np.random.choice(['Male', 'Female'], 100),
    'allowed_pmpm': np.random.uniform(100, 5000, size=100)
}

df = pd.DataFrame(data)

# Define a list of real chronic conditions
chronic_conditions = [
    'Diabetes', 'Hypertension', 'Chronic Kidney Disease', 'Asthma', 
    'COPD', 'Heart Failure', 'Depression', 'Arthritis'
]

# Assign real chronic condition names to the dataframe
df['chronic_condition'] = np.random.choice(chronic_conditions, 100)

# Calculate the 75th percentile for allowed_pmpm
high_cost_threshold = np.percentile(df['allowed_pmpm'], 75)

# Add a column for current high cost claimant based on the 75th percentile
df['current_high_cost_claimant'] = df['allowed_pmpm'] > high_cost_threshold

# Add a column for current medication adherence
np.random.seed(42)  # For reproducibility
df['current_med_adherence'] = np.random.rand(100)

# Calculate the 25th percentile for medication adherence
low_med_adherence_threshold = np.percentile(df['current_med_adherence'], 25)

# Add a column for current non-medication adherence based on the 25th percentile
df['current_non_med_adherence'] = df['current_med_adherence'] < low_med_adherence_threshold

# Add a column for predicted medication adherence
df['predicted_med_adherence'] = np.random.rand(100)

# Define criteria for categorizing claimants based on medication adherence
def categorize_claimant(row):
    if row['current_non_med_adherence'] and row['predicted_med_adherence'] > 0.5:
        return 'Impactable low medication adherence'
    elif row['current_non_med_adherence'] and row['predicted_med_adherence'] < 0.5:
        return 'Unavoidable low medication adherence'
    elif not row['current_non_med_adherence'] and row['predicted_med_adherence'] < 0.5:
        return 'Future low medication adherence'
    else:
        return 'Stable high medication adherence'

df['claimant_category'] = df.apply(categorize_claimant, axis=1)

# Round the medication adherence values for better readability
df['current_med_adherence'] = df['current_med_adherence'].round(2)
df['predicted_med_adherence'] = df['predicted_med_adherence'].round(2)

# Streamlit application
st.title('Medication Adherence Risk Prediction')

st.markdown("""

Current non-medication adherence: Members who are in the bottom 25th percentile for current medication adherence. These members are considered non-adherent based on current data.

Below is the medication adherence prediction demo. We predict the probability of a member adhering to their medication (e.g., picking up their medication). We created four categories to help users identify which members are impactable:

Impactable low medication adherence: Currently not adhering to medication; however, predicted to take their medication. Users should target these members as they are likely to take their medication.

Unavoidable low medication adherence: Members who are non-adherent and predicted to stay non-adherent. These are members users may want to consider ignoring since there is little opportunity for improvement.

Future low medication adherence: Members who are currently adhering to medication, however, are predicted to drop. Users may want to target these members as they could decrease medication adherence in the future.

Stable high medication adherence: Members with current high medication adherence and predicted to stay high. No intervention with these members is likely necessary.

""")

# Select chronic condition
chronic_condition = st.selectbox('Select Chronic Condition', options=chronic_conditions)

# Select medication adherence category
med_adherence_categories = [
    'Impactable low medication adherence', 'Unavoidable low medication adherence', 
    'Future low medication adherence', 'Stable high medication adherence'
]
med_adherence_category = st.selectbox('Select Medication Adherence Category', options=med_adherence_categories)

# Filter the dataframe based on selections
filtered_df = df[(df['chronic_condition'] == chronic_condition) & (df['claimant_category'] == med_adherence_category)]

# Display the filtered dataframe
st.dataframe(filtered_df)
