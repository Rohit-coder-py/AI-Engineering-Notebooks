<h2 style="font-size:30px; color:#1E3A8A; border-bottom:2px solid #DBEAFE; padding-bottom:7px;">
    <strong>Dataset Column Descriptions</strong>
</h2>

<h3 style="color:#1D4ED8;">Demographic & Personal Information</h3>

<div style="background:linear-gradient(135deg,#EFF6FF,#F5F3FF); border-left:5px solid #2563EB; padding:14px 18px; border-radius:8px; line-height:1.9;">

<strong>person_id:</strong> Unique identifier assigned to each person in the dataset. It is used to distinguish individual records and should generally <strong>not be used as a predictive feature</strong>.<br><br>

<strong>age:</strong> Age of the person in years.<br><br>
<strong>sex:</strong> Sex category of the person, such as Male, Female, or Other.<br><br>
<strong>region:</strong> Geographic region where the person is located, such as North, South, East, West, or Central.<br><br>
<strong>urban_rural:</strong> Classification of the person's residential area, such as Urban, Suburban, or Rural.<br><br>
<strong>income:</strong> Approximate annual income of the person.<br><br>
<strong>education:</strong> Highest education level attained by the person, such as High School, Some College, Bachelor's, Master's, or Doctorate.<br><br>
<strong>marital_status:</strong> Marital status of the person.<br><br>
<strong>employment_status:</strong> Employment category or current employment condition of the person.<br><br>
<strong>household_size:</strong> Total number of people living in the person's household.<br><br>
<strong>dependents:</strong> Number of financially or otherwise dependent individuals associated with the person.

</div>

<h3 style="color:#15803D;">Health & Lifestyle Information</h3>

<div style="background:linear-gradient(135deg,#F0FDF4,#ECFDF5); border-left:5px solid #16A34A; padding:14px 18px; border-radius:8px; line-height:1.9;">

<strong>bmi:</strong> Body Mass Index (BMI), representing the person's weight relative to their height.<br><br>
<strong>smoker:</strong> Indicates whether the person is a smoker. This is an important lifestyle and health-risk factor.<br><br>
<strong>alcohol_freq:</strong> Frequency of alcohol consumption, such as occasional, weekly, or daily. This column contains missing values for some records.<br><br>
<strong>visits_last_year:</strong> Number of healthcare or medical visits made by the person during the previous year.<br><br>
<strong>hospitalizations_last_3yrs:</strong> Number of times the person was hospitalized during the previous three years.<br><br>
<strong>days_hospitalized_last_3yrs:</strong> Total number of days the person spent hospitalized during the previous three years.<br><br>
<strong>medication_count:</strong> Number of medications currently associated with the person's medical treatment.

</div>

<h3 style="color:#991B1B;">Clinical Measurements</h3>

<div style="background:linear-gradient(135deg,#FEF2F2,#FFF1F2); border-left:5px solid #DC2626; padding:14px 18px; border-radius:8px; line-height:1.9;">

<strong>systolic_bp:</strong> Systolic blood pressure measurement, representing the pressure in the arteries when the heart contracts.<br><br>
<strong>diastolic_bp:</strong> Diastolic blood pressure measurement, representing the pressure in the arteries when the heart relaxes.<br><br>
<strong>ldl:</strong> Low-Density Lipoprotein (LDL) cholesterol level.<br><br>
<strong>hba1c:</strong> HbA1c measurement, representing average blood glucose levels over a period of approximately two to three months.

</div>

<h3 style="color:#7E22CE;">Insurance Policy Information</h3>

<div style="background:linear-gradient(135deg,#FAF5FF,#F5F3FF); border-left:5px solid #9333EA; padding:14px 18px; border-radius:8px; line-height:1.9;">

<strong>plan_type:</strong> Type of insurance plan selected by the person.<br><br>
<strong>network_tier:</strong> Tier or level of the healthcare provider network associated with the insurance plan.<br><br>
<strong>deductible:</strong> Amount the insured person is generally responsible for paying before insurance coverage begins according to the policy terms.<br><br>
<strong>copay:</strong> Fixed amount paid by the insured person for a covered healthcare service.<br><br>
<strong>policy_term_years:</strong> Duration of the insurance policy in years.<br><br>
<strong>policy_changes_last_2yrs:</strong> Number of changes made to the person's insurance policy during the previous two years.<br><br>
<strong>provider_quality:</strong> Numerical score representing the quality or rating of the healthcare provider/network.<br><br>
<strong>risk_score:</strong> Numerical score representing the estimated healthcare risk associated with the person. Higher values indicate greater estimated risk.

</div>

<h3 style="color:#A16207;">Medical Cost & Insurance Financial Information</h3>

<div style="background:linear-gradient(135deg,#FEFCE8,#FFFBEB); border-left:5px solid #EAB308; padding:14px 18px; border-radius:8px; line-height:1.9;">

<strong>annual_medical_cost:</strong> Total medical/healthcare expenditure associated with the person over a year. <strong>This is the target variable for our Medical Insurance Cost Predictor ANN project.</strong><br><br>
<strong>annual_premium:</strong> Total insurance premium paid or charged for the person over one year.<br><br>
<strong>monthly_premium:</strong> Monthly insurance premium associated with the person's insurance policy.<br><br>
<strong>claims_count:</strong> Total number of insurance/medical claims associated with the person.<br><br>
<strong>avg_claim_amount:</strong> Average monetary amount associated with the person's individual claims.<br><br>
<strong>total_claims_paid:</strong> Total amount paid across the person's insurance/medical claims.

</div>

<h3 style="color:#0F766E;">Chronic Medical Conditions</h3>

<div style="background:linear-gradient(135deg,#F0FDFA,#ECFEFF); border-left:5px solid #0D9488; padding:14px 18px; border-radius:8px; line-height:1.9;">

<strong>chronic_count:</strong> Total number of chronic medical conditions associated with the person.<br><br>
<strong>hypertension:</strong> Binary indicator showing whether the person has hypertension. `1` indicates presence and `0` indicates absence.<br><br>
<strong>diabetes:</strong> Binary indicator showing whether the person has diabetes. `1` indicates presence and `0` indicates absence.<br><br>
<strong>asthma:</strong> Binary indicator showing whether the person has asthma. `1` indicates presence and `0` indicates absence.<br><br>
<strong>copd:</strong> Binary indicator showing whether the person has Chronic Obstructive Pulmonary Disease (COPD). `1` indicates presence and `0` indicates absence.<br><br>
<strong>cardiovascular_disease:</strong> Binary indicator showing whether the person has a cardiovascular disease. `1` indicates presence and `0` indicates absence.<br><br>
<strong>cancer_history:</strong> Binary indicator showing whether the person has a history of cancer. `1` indicates a previous history and `0` indicates no recorded history.<br><br>
<strong>kidney_disease:</strong> Binary indicator showing whether the person has kidney disease. `1` indicates presence and `0` indicates absence.<br><br>
<strong>liver_disease:</strong> Binary indicator showing whether the person has liver disease. `1` indicates presence and `0` indicates absence.<br><br>
<strong>arthritis:</strong> Binary indicator showing whether the person has arthritis. `1` indicates presence and `0` indicates absence.<br><br>
<strong>mental_health:</strong> Binary indicator showing whether the person has a recorded mental-health-related condition. `1` indicates presence and `0` indicates absence.

</div>

<h3 style="color:#C2410C;">Medical Procedure Information</h3>

<div style="background:linear-gradient(135deg,#FFF7ED,#FFEDD5); border-left:5px solid #F97316; padding:14px 18px; border-radius:8px; line-height:1.9;">

<strong>proc_imaging_count:</strong> Number of medical imaging procedures associated with the person.<br><br>
<strong>proc_surgery_count:</strong> Number of surgical procedures associated with the person.<br><br>
<strong>proc_physio_count:</strong> Number of physiotherapy procedures or sessions associated with the person.<br><br>
<strong>proc_consult_count:</strong> Number of medical consultations associated with the person.<br><br>
<strong>proc_lab_count:</strong> Number of laboratory/diagnostic tests associated with the person.<br><br>
<strong>is_high_risk:</strong> Binary indicator identifying whether the person is classified as high risk based on the dataset's risk criteria. `1` indicates high risk and `0` indicates not high risk.<br><br>
<strong>had_major_procedure:</strong> Binary indicator showing whether the person underwent a major medical procedure. `1` indicates that a major procedure occurred and `0` indicates that it did not.

</div>