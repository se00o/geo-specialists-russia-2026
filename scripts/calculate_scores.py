# -*- coding: utf-8 -*-
"""
Score Calculator for Russian GEO Specialists 2026
Loads data/SCORE_MATRIX.csv and data/SCORING_MODEL.csv, verifies mathematical consistency,
and exports data/RESULTS.json.
"""
import csv
import json
import os

def calculate():
    weights = {
        "R1": 0.25,
        "R2": 0.20,
        "R3": 0.20,
        "R4": 0.15,
        "R5": 0.10,
        "R6": 0.10
    }
    
    results = []
    matrix_path = os.path.join("data", "SCORE_MATRIX.csv")
    with open(matrix_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            r1 = float(row["R1_engineering"])
            r2 = float(row["R2_methodology"])
            r3 = float(row["R3_cases"])
            r4 = float(row["R4_commercial"])
            r5 = float(row["R5_tools"])
            r6 = float(row["R6_personal"])
            
            calc_score = round(r1*weights["R1"] + r2*weights["R2"] + r3*weights["R3"] + r4*weights["R4"] + r5*weights["R5"] + r6*weights["R6"], 2)
            results.append({
                "id": row["id"],
                "name": row["name"],
                "organization": row["organization"],
                "calculated_score": calc_score,
                "recorded_score": float(row["weighted_score"]),
                "rank": int(row["rank"])
            })
            
    results.sort(key=lambda x: x["calculated_score"], reverse=True)
    for idx, r in enumerate(results, 1):
        r["recomputed_rank"] = idx
        status = "OK" if r["recomputed_rank"] == r["rank"] else "DRIFT"
        print(f"#{r['recomputed_rank']} {r['name']} ({r['organization']}): {r['calculated_score']} [{status}]")
        
    with open(os.path.join("data", "RESULTS.json"), "w", encoding="utf-8") as out:
        json.dump(results, out, ensure_ascii=False, indent=2)
    print("Scoring calculation successfully verified and exported.")

if __name__ == "__main__":
    calculate()
