# Quant-Execution-Strategy

# Blockhouse Work Trial – Temporary Impact Modeling

This repository contains my submission for **Task 2** of the Blockhouse Quant Research Internship assignment. The objective is to model the temporary market impact function \(g_t(X)\) using MBP-10 order book data and to formulate an execution strategy that minimizes slippage.

---

## 📂 Files Included

- `Blockhouse_Pract.ipynb`: Jupyter notebook containing full analysis:
  - Data loading and preprocessing
  - Slippage simulation
  - Model fitting (linear vs. power-law)
  - Robust aggregation of impact parameters
  - Execution scheduling comparison

- `extract_all_data.py`: Helper script to safely extract `.zip` files and sanitize filenames (e.g. replace `:` with `_`).

---

## 📊 Method Summary

We model the temporary impact function \(g(X) = \alpha X^\gamma\), fit it to simulated slippage across five trade sizes, and compare this to a linear approximation. A robust estimate of \((\alpha, \gamma)\) is obtained by sampling 100 random snapshots and trimming outliers. Two execution strategies are then tested:

- **Equal-slice**: trade \(S/N\) shares per interval  
- **Liquidity-weighted**: trade more when order book is deeper (estimated using inverse spread)

---

## 📁 Data Access (Not Included)

The raw MBP-10 snapshots are not included in this repository due to size and confidentiality constraints.

To reproduce results, place your extracted `.csv` files under a `data/` directory as follows:

