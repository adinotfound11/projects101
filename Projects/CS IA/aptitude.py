import matplotlib.pyplot as plt
from fpdf import FPDF
import pandas as pd
import numpy as np

interest_areas = ['Realistic', 'Investigative', 'Artistic', 'Social', 'Enterprising', 'Conventional']
scores = {}

print("Enter your RIASEC scores (0–100):")
for area in interest_areas:
    while True:
        try:
            val = int(input(f"{area}: "))
            if 0 <= val <= 100:
                scores[area] = val
                break
            else:
                print("Please enter a number between 0 and 100.")
        except:
            print("Invalid input. Please enter an integer.")

sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
top_score = sorted_scores[0][1]
top_areas = [area for area, score in sorted_scores if score == top_score]

career_suggestions = {
    'Realistic': ['Engineer', 'Chef', 'Mechanic', 'Carpenter', 'Pilot'],
    'Investigative': ['Scientist', 'Doctor', 'Data Analyst', 'Researcher', 'Pharmacist'],
    'Artistic': ['Graphic Designer', 'Writer', 'Musician', 'Architect', 'Animator'],
    'Social': ['Teacher', 'Therapist', 'Nurse', 'Counselor', 'Social Worker'],
    'Enterprising': ['Entrepreneur', 'Manager', 'Sales Executive', 'Lawyer', 'Marketer'],
    'Conventional': ['Accountant', 'Bank Clerk', 'Data Entry Specialist', 'Auditor', 'Office Manager']
}

personality_summary = {
    'Realistic': "You enjoy hands-on tasks, building, fixing, and working with tools or machines.",
    'Investigative': "You like exploring ideas, researching, analyzing, and solving complex problems.",
    'Artistic': "You prefer creative expression, imagination, and working in unstructured environments.",
    'Social': "You are supportive, communicative, and enjoy helping others through teaching or healing.",
    'Enterprising': "You are persuasive, energetic, and thrive in leadership or business roles.",
    'Conventional': "You appreciate structure, order, and enjoy working with data, numbers, or procedures."
}

career_output = ""
summary_output = ""
for area in top_areas:
    recs = ', '.join(career_suggestions[area])
    desc = personality_summary[area]
    career_output += f"{area}: {recs}\n"
    summary_output += f"{area}: {desc}\n"

valid_scores = {k: v for k, v in scores.items() if isinstance(v, int) and v > 0}
labels = list(valid_scores.keys())
values = list(valid_scores.values())

if valid_scores:
    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, color='teal')
    plt.title("RIASEC Scores - Bar Chart")
    plt.ylabel("Score")
    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig("bar_chart.png")
    plt.close()

    plt.figure(figsize=(7, 7))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title("RIASEC Score Distribution - Pie Chart")
    plt.tight_layout()
    plt.savefig("pie_chart.png")
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.hist(values, bins=6, color='purple', edgecolor='black')
    plt.title("RIASEC Score Histogram")
    plt.xlabel("Score")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig("histogram.png")
    plt.close()

    categories = list(scores.keys())
    N = len(categories)
    values_radar = [scores[cat] for cat in categories]
    values_radar += values_radar[:1]
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    plt.figure(figsize=(7, 7))
    ax = plt.subplot(111, polar=True)
    plt.xticks(angles[:-1], categories)
    ax.plot(angles, values_radar, linewidth=2, linestyle='solid')
    ax.fill(angles, values_radar, 'skyblue', alpha=0.4)
    plt.title("RIASEC Radar Chart")
    plt.tight_layout()
    plt.savefig("radar_chart.png")
    plt.close()

    avg_scores = {'Realistic': 55, 'Investigative': 60, 'Artistic': 50, 'Social': 65, 'Enterprising': 58, 'Conventional': 52}
    plt.figure(figsize=(10, 6))
    plt.plot(list(avg_scores.keys()), list(avg_scores.values()), label='National Average', linestyle='--', marker='o')
    plt.plot(list(scores.keys()), list(scores.values()), label='Your Scores', linestyle='-', marker='s')
    plt.title("RIASEC: You vs National Average")
    plt.ylabel("Score")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("comparison_chart.png")
    plt.close()

df = pd.DataFrame(list(scores.items()), columns=["Interest Area", "Score"])
df.to_csv("RIASEC_scores.csv", index=False)

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(200, 10, "RIASEC Assessment Report", ln=True, align='C')
pdf.set_font("Arial", size=12)
pdf.ln(5)

pdf.cell(200, 10, "Your RIASEC Scores:", ln=True)
for area, score in scores.items():
    pdf.cell(200, 10, f"{area}: {score}", ln=True)

pdf.ln(5)
pdf.cell(200, 10, "Top Career Recommendations:", ln=True)
for area in top_areas:
    pdf.multi_cell(0, 10, f"{area}: {', '.join(career_suggestions[area])}")

pdf.ln(5)
pdf.cell(200, 10, "Personality Summary:", ln=True)
for area in top_areas:
    pdf.multi_cell(0, 10, f"{area}: {personality_summary[area]}")

pdf.ln(5)
pdf.cell(200, 10, "Insight Summary:", ln=True)
pdf.multi_cell(0, 10, f"Top Interest Area(s): {', '.join(top_areas)}")
pdf.multi_cell(0, 10, f"Middle Area: {sorted_scores[len(sorted_scores)//2][0]}")
pdf.multi_cell(0, 10, f"Lowest Area: {sorted_scores[-1][0]}")

pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, "Charts and Visuals", ln=True)

pdf.image("bar_chart.png", x=10, w=180)
pdf.ln(10)
pdf.image("pie_chart.png", x=10, w=180)
pdf.ln(10)
pdf.image("histogram.png", x=10, w=180)
pdf.ln(10)
pdf.image("radar_chart.png", x=10, w=180)
pdf.ln(10)
pdf.image("comparison_chart.png", x=10, w=180)

pdf.output("RIASEC_Complete_Report.pdf")
print("\n✔️ Report saved as 'RIASEC_Complete_Report.pdf'")