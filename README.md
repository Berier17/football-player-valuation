# Football Player Valuation Prediction

This project is an end-to-end machine learning solution to predict the market value of football players. The model is trained on data scraped from **Fbref** and **Transfermarkt** (via ScraperFC) and deployed as a live web service using Flask, Docker, and Google Cloud Run.

**Live Service URL:** `https://valuation-api-300316357465.us-central1.run.app/predict`

## 1. Problem Description

The goal of this project is to build a "Moneyball" tool that can objectively estimate a player's market value based on performance metrics rather than hype. By analyzing statistics like **Expected Goals (xG)**, **Starts**, and **Age**, clubs can identify undervalued talent in the transfer market.

This service provides a "predicted market value" (in Euros) for any given player profile, allowing scouts and data analysts to compare a player's asking price against their statistical worth. The model is evaluated using **MAE (Mean Absolute Error)** to prioritize "cash accuracy" over simple correlation.

## 2. Exploratory Data Analysis (EDA)

My analysis (in `notebook.ipynb`) was performed to find the key statistical drivers of market value. I utilized a **Correlation Matrix** and **Scatter Plots** to visualize relationships between on-field performance and financial value.

The analysis revealed that performance metrics are the strongest predictors, but age plays a crucial negative role:

| Feature | Correlation (r) | Insight |
| :--- | :--- | :--- |
| **npxG+xAG** | **0.54** | Strongest correlation. Goal contributions drive value. |
| **Starts** | **0.47** | Playing time is a critical baseline for value. |
| **Age** | **-0.27** | Negative correlation. Older players lose value even with good stats. |

**Key Insights:**
* **The "Moneyball" Trend:** As seen in the scatter plot, there is a clear linear relationship between `npxG+xAG` and Value, though elite outliers (like Haaland) break the scale.
* **Outlier Detection:** The dataset contains significant outliers. Players with values >€7.25M are statistically rare, which skews standard predictions.

## 3. Model Training & Selection

I trained and evaluated **Linear Regression** and **XGBoost** models. While Linear Regression had a decent $R^2$, I selected **XGBoost** as the champion model based on the "Cash is King" business logic.

**Why XGBoost?**
* **MAE (Cash Error):** XGBoost is off by an average of **€948k** per player, whereas Linear Regression is off by **€1.13M**. Over a transfer window of 10 players, XGBoost saves the club nearly **€1.8M** in estimation error.
* **MAPE (Percentage Error):** Linear Regression struggled with lower-value players (68% error). XGBoost (54.9%) was far more robust across the entire squad.

**Feature Importance:**
The XGBoost model prioritized the **Team** feature above all else, indicating that the "club premium" (e.g., playing for a top-tier team) adds significant intangible value, followed closely by Age and Expected Goals.

| Feature | Importance Score |
| :--- | :--- |
| **Team** | **199.0** |
| **Age** | **163.0** |
| **npxG+xAG** | **135.0** |

**Final Performance:**
The final model achieved a Test MAPE of **74.5%**.
* *Note:* This high percentage is driven heavily by "cheap" players (<€1M). For example, if a player is worth €300k and the model predicts €2M (based on their starts), the percentage error is massive, even if the cash difference is small in football terms.

## 4. Reproducibility & Deployment

This project is fully reproducible and deployable.

### To Train the Model:
This will create `model.bin` from scratch using the best parameters.

1.  **Set up a virtual environment and install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run the training script:**
    ```bash
    python train.py
    ```

### To Run the Web Service Locally:
1.  **Run the Flask app:**
    ```bash
    python predict.py
    ```
2.  **Send a request:**
    Open a separate terminal and run `python test.py`.

### To Run with Docker:
1.  **Build the container image:**
    ```bash
    docker build -t valuation-model .
    ```
2.  **Run the container:**
    ```bash
    docker run -p 9696:9696 valuation-model
    ```

## 5. Testing the Deployed Service

You can test the live service by sending a `POST` request to the public URL with a player's JSON profile.

**Service URL:** `https://valuation-api-300316357465.us-central1.run.app/predict`

**Example `test.py`:**

```python
import requests

# This is the public URL for the deployed service
url = '[https://valuation-api-300316357465.us-central1.run.app/predict](https://valuation-api-300316357465.us-central1.run.app/predict)'

# A sample player profile (Stats based on a good Premier League forward)
player = {
    "age": 22,
    "npxg+xag": 8.5,
    "starts": 25,
    "team": "Arsenal", 
    "pos": "Forward"
}
#Answer
{
  "message": "Estimated Value: €10,522,622",
  "predicted_value_euros": 10522622.0
}

response = requests.post(url, json=player)
print(response.json())
