# 📊 ניתוח נתוני מסחר אלקטרוני | E-commerce Data Analysis

## סקירת הפרויקט

פרויקט מתקדם לניתוח נתוני מסחר אלקטרוני באמצעות Python, הכולל עיבוד נתונים, ניתוח התנהגות לקוחות, מדדי ביצוע עסקיים (KPIs) ופיתוח Dashboard אינטראקטיבי באמצעות Streamlit.

הפרויקט מבוסס על נתוני Olist Brazilian E-Commerce Dataset ומטרתו להפיק תובנות עסקיות שיסייעו בהבנת דפוסי הרכישה, ערך הלקוחות וריכוז ההכנסות.

## מטרות הפרויקט

- ניתוח ביצועי מכירות והזמנות.
- זיהוי דפוסי רכישה של לקוחות.
- פילוח לקוחות באמצעות RFM Analysis.
- ניתוח ערך לקוח (Customer Value).
- בחינת ריכוז ההכנסות באמצעות Pareto Analysis.
- מדידת נאמנות לקוחות ורכישות חוזרות.
- הצגת תוצאות באמצעות Dashboard אינטראקטיבי.

## טכנולוגיות וכלים

| טכנולוגיה | שימוש |
| Python | עיבוד וניתוח נתונים |
| Pandas | ניקוי, מיזוג וניתוח טבלאות |
| Jupyter Notebook | ביצוע הניתוחים ותיעודם |
| Streamlit | פיתוח Dashboard אינטראקטיבי |
| Plotly | יצירת תרשימים אינטראקטיביים |
| VS Code | סביבת פיתוח |
| GitHub | ניהול גרסאות והצגת הפרויקט |

## מדדי ביצוע מרכזיים (KPIs)

| מדד | תוצאה |
| Total Product Sales | R$ 13,591,643.70 |
| Total Orders | 96,478 |
| Total Customers | 93,358 |
| Repeat Purchase Rate | 3.00% |
| Average Purchase Frequency | 1.03 |

## תובנות עסקיות מרכזיות

**נאמנות לקוחות:** מרבית הלקוחות ביצעו רכישה אחת בלבד, ושיעור הרכישות החוזרות עומד על כ־3%.

**ריכוז הכנסות:** כ־20% מהלקוחות אחראים לכ־56.62% מההכנסות בניתוח ריכוז ההכנסות.

**לקוחות בעלי ערך גבוה:** קבוצת VIP Customers אחראית לכ־62.53% מההכנסות במסגרת ניתוח פילוח ערך הלקוחות.

## Dashboard אינטראקטיבי

ה-Dashboard כולל חמישה אזורי ניתוח מרכזיים:

1. Business Overview
2. Customer Segmentation
3. Customer Value
4. Revenue Concentration
5. Customer Loyalty

## תיעוד הפרויקט

תיעוד מפורט של תהליכי העבודה, שיטות הניתוח והקוד נמצא בתיקיית `notebooks/doc`.

## הפעלת ה-Dashboard

לאחר התקנת התלויות הדרושות, ניתן להפעיל את ה-Dashboard באמצעות:

streamlit run dashboard/app.py
```

## סיכום

הפרויקט מדגים תהליך עבודה אנליטי הכולל עיבוד נתונים, ניתוח לקוחות, חישוב מדדים עסקיים והנגשת תובנות באמצעות ממשק אינטראקטיבי.





## צילומי מסך של ה-Dashboard

### Business Overview
![Business Overview](images/business_overview.png)

### Customer Segmentation
![Customer Segmentation](images/customer_segmentation.png)

### Customer Value
![Customer Value](images/customer_value.png)

### Revenue Concentration
![Revenue Concentration](images/revenue_concentration.png)

### Customer Loyalty
![Customer Loyalty](images/customer_loyalty.png)