# ⚡ Washington County-Level EV Forecast Tool  
### Part of the *Tesla EV Growth Strategy · Washington EV Hub*

This repository contains the **County-Level Forecast Tool (`ev_forecast_app`)**, which generates individualized EV adoption and registration forecasts for each Washington county. It is integrated into the full EV Hub ecosystem shown below.

---

## 🧩 Site Flow & Architecture Overview

```
                         +----------------------+
                         |       Home Hub       |
                         +----------+-----------+
                                    |
            +-----------------------+-----------------------+
            |                                               |
    +-------v-----------------------+       +---------------v----------------------+
    |     Statewide Forecast Tool   |       |     County-Level Forecast Tool      |
    |         (ev_render_app)       |       |         (ev_forecast_app)           |
    +---------------+---------------+       +------------------+-------------------+
                    |                                          |
                    +----------------------+-------------------+
                                           |
                                 +---------v----------+
                                 |     Forecast       |
                                 |      Results       |
                                 | (EV Registrations  |
                                 |    & Adoption)     |
                                 +--------------------+
```

---

## 🌐 Access the Full EV Growth Strategy Hub  
👉 **Tesla EV Growth Strategy · Washington EV Hub**  
https://home-page-ev.onrender.com/

---

## 🔥 Why This Tool Matters

EV adoption varies dramatically across Washington counties due to differences in:

- Population density  
- Existing charging availability  
- Urban vs rural drive patterns  
- Infrastructure buildout timing  
- Local policy readiness  

This County-Level tool reveals **how each county responds to incremental charging infrastructure**, helping identify:

- Counties at highest risk of falling behind  
- Where each new charger yields the **largest EV adoption increase**  
- Whether counties meet **2030–2050 climate mandates**  
- High-value areas for infrastructure investment  
- Comparative ROI between counties  
- Population-based resource allocation strategies  

---

## 🛠 How the County Model Works

For each Washington county, the model evaluates:

- Baseline EV registrations (2024 actuals)  
- Existing Supercharger  
- County population and density tier  
- Best-fit formula curves:
  - **EV Registrations vs. Superchargers** (`EVs_vs_SC_Formula`)
  - **EV Adoption Rate vs. Superchargers** (`Adopt_vs_SC_Formula`)

Using these formulas, the tool:

1. Computes nonlinear EV growth as charger count increases  
2. Applies monotonic logistic/polynomial fits  
3. Generates county-specific growth curves through 2050  
4. Visualizes curves using `chart.png`  
5. Returns projected adoption & registration results to the user  

---

## 📁 Repository Structure

```
ev_forecast_app/
│
├── app.py                       
├── templates/
│     ├── index.html                       
│
├── static/
│     ├── map.png                
│     └── chart.png
│     └── County-level formula.xlsx           
│   
│
└── README.md
```

---

## ▶️ Run Locally

```bash
git clone https://github.com/<yourname>/ev_forecast_app.git
cd ev_forecast_app
pip install -r requirements.txt
flask run
```

Local app runs at:  
**http://127.0.0.1:5000**

---

## 🚀 Deploy to Render

**Build Command**
```
pip install -r requirements.txt
```

**Start Command**
```
gunicorn app:app
```

---
