# ניתוח נתוני מסחר אלקטרוני | E-Commerce Data Analysis

## סקירת הפרויקט

פרויקט Data Analysis מתקדם המבוסס על Olist Brazilian E-Commerce Dataset, במטרה לנתח ביצועים עסקיים, התנהגות לקוחות, הכנסות ונאמנות לקוחות באמצעות Python.

הפרויקט כולל תהליכי Data Exploration, Data Validation, Customer Segmentation, RFM Analysis וניתוח ריכוז הכנסות, לצד Dashboard אינטראקטיבי שפותח באמצעות Streamlit.

## טכנולוגיות וכלים

- Python
- Pandas ו-NumPy
- Jupyter Notebook
- Matplotlib ו-Seaborn
- Plotly
- Streamlit
- Git ו-GitHub

## מדדים עסקיים מרכזיים

| מדד | תוצאה |
|---|---:|
| מספר הזמנות שסופקו | 96,478 |
| מספר לקוחות ייחודיים | 93,358 |
| סך מכירות מוצרים — כלל ההזמנות | R$ 13,591,643.70 |
| שיעור רכישה חוזרת | 3.00% |
| תדירות רכישה ממוצעת | 1.03 |

## ניתוחים מרכזיים

### Customer Segmentation

פילוח לקוחות באמצעות מודל RFM, המבוסס על Recency, Frequency ו-Monetary.

### Customer Value

חלוקת לקוחות לארבע קבוצות ערך: Low Value, Medium Value, High Value ו-VIP Customers.

### Revenue Concentration

ניתוח התפלגות ההכנסות בין קבוצות לקוחות וזיהוי ריכוז ההכנסות.

### Customer Loyalty

בחינת לקוחות שרכשו פעם אחת לעומת לקוחות חוזרים, לצורך זיהוי הזדמנויות לשיפור שימור הלקוחות.

## Dashboard

הפרויקט כולל Dashboard אינטראקטיבי המציג חמישה תחומי ניתוח:

1. Business Overview
2. Customer Segmentation
3. Customer Value
4. Revenue Concentration
5. Customer Loyalty

## הרצת הפרויקט

התקנת הספריות:

```bash
pip install -r requirements.txt
```

הפעלת לוח המחוונים:

```bash
streamlit run dashboard/app.py
```

## תיעוד נוסף

- `notebooks/01_Data_Exploration.ipynb` — מחברת ניתוח הנתונים.
- `notebooks/doc/01_Project_Documentation.md` — תיעוד הפרויקט.
- `reports/02_Data_Validation_Report.md` — דוח בדיקות איכות הנתונים.
- `reports/03_Project_Summary.md` — סיכום הפרויקט.

## מקור הנתונים

Olist Brazilian E-Commerce Dataset.

קובצי המקור נשמרים בתיקיית `DATA/RAW` ואינם נכללים במאגר GitHub.