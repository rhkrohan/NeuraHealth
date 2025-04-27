# NeuraHealth 

![image](https://github.com/user-attachments/assets/298025f5-cd7c-44d8-99ff-23e44de9ea45)

## Problem Statement

In today's healthcare environment, patients often face significant delays and high costs when seeking medical diagnoses, particularly in the United States. Long wait times for doctor appointments and expensive consultations make timely medical care difficult for many individuals. Additionally, many non-serious cases unnecessarily burden healthcare providers, leading to inefficient use of medical resources.

Our AI Healthcare System aims to address these challenges by providing fast, cost-effective, and accessible preliminary diagnoses for critical health conditions, starting with brain tumors, diabetes, and pneumonia. The system is designed to:

- Reduce the time and expense associated with traditional diagnostic processes.
- Screen out non-serious cases, allowing healthcare professionals to focus on patients needing urgent care.
- Assist doctors by instantly providing examination results, enhancing decision-making and improving patient outcomes.

This project is an evolving concept, with plans to integrate additional diagnostic capabilities and expand the system's functionality to serve a broader range of medical needs.

## Vision Statement

Our vision is to revolutionize the healthcare experience by harnessing the power of AI to make early diagnosis faster, more affordable, and more accessible for everyone. By providing intelligent, reliable, and instant diagnostic support, we aim to empower patients and assist healthcare professionals, ultimately improving global health outcomes and reducing strain on medical systems.

## Future Scope

- **Expansion of Diagnoses**: Integrate additional AI models to detect a wider range of diseases and medical conditions beyond brain tumors, diabetes, and pneumonia.
- **Integration with Medical Facilities**: Collaborate with hospitals, clinics, and telehealth services to incorporate the system into real-world healthcare workflows.
- **Mobile Application Development**: Launch a patient-friendly mobile app to make preliminary diagnoses accessible anytime, anywhere.
- **Continuous Model Improvement**: Regularly update AI models based on new medical research, patient feedback, and clinical data to enhance accuracy and reliability.
- **Data Privacy and Security**: Implement advanced data protection protocols to ensure patient confidentiality and compliance with healthcare regulations (e.g., HIPAA).
- **Global Accessibility**: Optimize the system for use in under-resourced regions where access to professional medical care is limited.

## Model Overview:

### Brain Tumor Detection;
The Brain Tumor Detection model leverages a Convolutional Neural Network (CNN) to classify brain MRI images into two categories: "tumor" and "healthy." This approach addresses the limitations of traditional manual diagnosis by offering a fast, accurate, and scalable solution. The system follows a structured workflow to ensure high reliability and clinical relevance:

- **Dataset Preparation:**
  - MRI images are labeled as either "tumor" or "healthy."
  - Images undergo preprocessing steps including resizing, normalization, and data augmentation to enhance generalization.

- **CNN Architecture:**
  - Multiple convolutional layers extract hierarchical features such as edges, textures, and complex patterns.
  - Max-pooling layers reduce spatial dimensions, improving computational efficiency.
  - Fully connected dense layers interpret the extracted features for final classification.
  - Softmax activation in the output layer provides class probabilities.

- **Training Strategy:**
  - Model trained over **25 epochs** with a balanced split into training, validation, and testing datasets.
  - Techniques such as **dropout** and **batch normalization** were used to prevent overfitting and stabilize learning.

- **Performance Metrics:**
  - **Training Accuracy:** 97.95%
  - **Validation Accuracy:** 91.08%
  - **Training Loss:** 0.0716
  - **Validation Loss:** 0.2556

By automating brain tumor detection, this model significantly reduces diagnosis time, supports radiologists with quick decision-making, and improves patient outcomes through earlier treatment interventions.

### Diabetes Analysis Prediction;

The Diabetes Analysis Prediction model predicts the likelihood of diabetes using several regression models based on a Kaggle dataset with 521 observations and 16 symptoms. After preprocessing (categorical encoding using `OrdinalEncoder`) and splitting the data (80:20), five models were trained: Multiple Linear Regression, Polynomial Regression (degree 2), Support Vector Regression (SVR), Decision Tree Regression, and Random Forest Regression. The models were evaluated based on R² score and a custom accuracy function to identify the most effective technique for prediction.

- **Dataset:** 521 observations, 16 categorical symptom features
- **Preprocessing:** Encoding "Yes"/"No" to 1/0, train-test split (80:20)
- **Models Used:** 
  - Multiple Linear Regression
  - Polynomial Regression
  - Support Vector Regression (SVR)
  - Decision Tree Regression
  - Random Forest Regression
- **Evaluation Metrics:** R² score, prediction accuracy (%)
- **Key Findings:** 
  - SVR achieved the highest R² score (0.9461) and 100% accuracy
  - Decision Tree Regression also performed strongly (R² = 0.878, 97.11% accuracy)
  - Polynomial and Multiple Linear Regression models showed lower performance
- **Conclusion:** SVR is the most effective model for this dataset, capturing complex relationships in the features, while Decision Tree Regression offers a strong interpretable alternative.
