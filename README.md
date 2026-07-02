# Python-PowerBI-Auto-Claim-Litigation-Study
This project is a work sample of insurance business knowledge combined with AI (Gemini), Python coding, and Power BI dashboard design. In this study, I analyzed personal auto injury claim and litigation cost and proposed recommendations to mitigate future risk.

## Data Source
* I wrote prompts in AI (Google Gemini) and run Python code in Anaconda Python Jupyter Notebook to simulate a dataset.
* I built this dashboard with Power BI desktop app (version 2.155).
* I designed a dataset of 4000 rows of injury claims from accident state Connecticut over the last 2 years (2024-2025).
* I referenced an insurance claim dataset published by Mendeley Data for claim amount distribution. (https://data.mendeley.com/datasets/992mh7dk9y/2)

## Target Audience
* Recruiters and data analytics managers.
* The dashboard demonstrates: (1) business knowledge; (2) Power BI skills; (3) senior-level insight

## Power BI - Executive Summary

<img width="710" height="396" alt="dashboard_p0_excutive_summary" src="https://github.com/user-attachments/assets/572d4622-4a6e-4c37-9b2b-30bee8629ba1" />


## Power BI - Liability & Cost
### Metric Definition
* Average claim cycle time: this is measured by the average number of days between claim report date and payout date.
* Average litigation cost: in this study, litigation cost is calculated as 30% of total claim amount.
* Serious Dispute Rate: this shows the percentage of claims with litigation cost over $15000 assuming that complies with the business rule

<img width="713" height="395" alt="dashboard_p1_liability_n_cost" src="https://github.com/user-attachments/assets/9af0dd88-3a16-4477-89f3-46b0768d6331" />


## Power BI - Risk Mitigation
### Metric Definition
* Total Subrogation Recovered Amount: this sums up the total amount recovered from the successful subrogation process.
* Projected Saving Amount with Telematics: assuming the company has a 30% success rate of changing drivers' behaviors using telematics, the company could expect to save X% from total claim payout and litigation cost from those claims of insured 100% at fault.

<img width="711" height="395" alt="dashboard_p2_risk_mitigation" src="https://github.com/user-attachments/assets/577c9264-5334-47be-8417-2ef2d0f073fe" />


## Power BI - Data Model
### Table List
* auto_claim_v2: this table hosts the injury claim records with liability, accident location, claim payout, litigation cost, and duty breach by insured drivers.
*  zipcode_dim_tb: this is a dimension table of Connecticut zipcode with country and city name. This help Power BI to plot the map correctly. Otherwise, Power BI sometimes mistaken a US city with another city with the same name located in Europe or Australia. This table is linked to the zipcode in the "auto_claim_v2"
*  Calendar_TB: this is a time table that enables Power BI to sort date correctly. Otherwise, Power BI would sort Monday through Friday alphabetically... (horrible!)
*  Calculated Measures: this table houses all the aggreated calculation such as average cycle time, average litigation cost, and projected saving of claim payout if Telematics works.
<img width="643" height="389" alt="power_bi_data_model" src="https://github.com/user-attachments/assets/7d4adf14-87bd-4f68-9689-cc77697719a0" />

