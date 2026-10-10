import random
import json
import os
from datetime import datetime

FIRST_NAMES = [
    "Aarav", "Ananya", "Rohan", "Priya", "Aditya", "Sneha", "Vikram", "Isha",
    "Rahul", "Pooja", "Arjun", "Diya", "Karan", "Tanvi", "Siddharth", "Neha",
    "Varun", "Meera", "Kabir", "Riya", "Nikhil", "Shreya", "Aryan", "Anushka",
    "Dev", "Kavya", "Manish", "Divya", "Suresh", "Komal", "Harsh", "Simran"
]

LAST_NAMES = [
    "Sharma", "Verma", "Patel", "Reddy", "Nair", "Iyer", "Choudhury", "Gupta",
    "Singh", "Mehta", "Bose", "Kulkarni", "Deshmukh", "Menon", "Joshi", "Bhat",
    "Rao", "Mishra", "Pandey", "Agarwal", "Chatterjee", "Saxena", "Pillai", "Das"
]

DEPARTMENTS = [
    "Computer Science & Engineering",
    "Artificial Intelligence & Data Science",
    "Information Technology",
    "Electronics & Communication Engineering",
    "Mechanical Engineering"
]

COURSES_BY_DEPT = {
    "Computer Science & Engineering": [
        {"code": "CS301", "name": "Data Structures & Algorithms", "credits": 4, "is_bottleneck": True},
        {"code": "CS302", "name": "Operating Systems", "credits": 4, "is_bottleneck": True},
        {"code": "CS303", "name": "Database Management Systems", "credits": 3, "is_bottleneck": False},
        {"code": "CS304", "name": "Computer Networks", "credits": 3, "is_bottleneck": False},
        {"code": "MA301", "name": "Discrete Mathematics", "credits": 4, "is_bottleneck": True}
    ],
    "Artificial Intelligence & Data Science": [
        {"code": "AI301", "name": "Machine Learning Foundations", "credits": 4, "is_bottleneck": True},
        {"code": "AI302", "name": "Applied Statistics & Probability", "credits": 4, "is_bottleneck": True},
        {"code": "AI303", "name": "Deep Learning Architectures", "credits": 3, "is_bottleneck": False},
        {"code": "AI304", "name": "Data Engineering Pipelines", "credits": 3, "is_bottleneck": False},
        {"code": "CS301", "name": "Data Structures & Algorithms", "credits": 4, "is_bottleneck": True}
    ],
    "Information Technology": [
        {"code": "IT301", "name": "Full-Stack Web Architectures", "credits": 4, "is_bottleneck": False},
        {"code": "IT302", "name": "Cloud Infrastructure & DevOps", "credits": 3, "is_bottleneck": False},
        {"code": "IT303", "name": "Information Security & Cryptography", "credits": 4, "is_bottleneck": True},
        {"code": "CS301", "name": "Data Structures & Algorithms", "credits": 4, "is_bottleneck": True},
        {"code": "CS303", "name": "Database Management Systems", "credits": 3, "is_bottleneck": False}
    ],
    "Electronics & Communication Engineering": [
        {"code": "EC301", "name": "Digital Signal Processing", "credits": 4, "is_bottleneck": True},
        {"code": "EC302", "name": "Electromagnetic Fields & Waves", "credits": 4, "is_bottleneck": True},
        {"code": "EC303", "name": "Microprocessors & Microcontrollers", "credits": 3, "is_bottleneck": False},
        {"code": "EC304", "name": "Analog Integrated Circuits", "credits": 4, "is_bottleneck": True},
        {"code": "MA201", "name": "Engineering Mathematics III", "credits": 4, "is_bottleneck": True}
    ],
    "Mechanical Engineering": [
        {"code": "ME301", "name": "Thermodynamics & Heat Transfer", "credits": 4, "is_bottleneck": True},
        {"code": "ME302", "name": "Fluid Mechanics & Machinery", "credits": 4, "is_bottleneck": True},
        {"code": "ME303", "name": "Mechanics of Solids", "credits": 4, "is_bottleneck": True},
        {"code": "ME304", "name": "Manufacturing Processes", "credits": 3, "is_bottleneck": False},
        {"code": "MA201", "name": "Engineering Mathematics III", "credits": 4, "is_bottleneck": True}
    ]
}

def generate_student_dataset(num_students=350, seed=42):
    random.seed(seed)
    students = []
    
    for i in range(1, num_students + 1):
        dept = random.choice(DEPARTMENTS)
        year = random.choice([2, 3, 4])  # 2nd, 3rd, 4th year has rich historical trajectory
        sem = (year * 2) - random.choice([0, 1])
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        student_id = f"STU-{2026 - year}-{i:03d}"
        email = f"{first_name.lower()}.{last_name.lower()}{random.randint(10, 99)}@institution.edu"
        
        # Decide latent profile category
        # 16% high risk, 24% medium risk, 60% low risk
        rand_profile = random.random()
        if rand_profile < 0.16:
            profile = "HIGH_RISK"
        elif rand_profile < 0.40:
            profile = "MEDIUM_RISK"
        else:
            profile = "LOW_RISK"

        # Generate metrics aligned with profile
        if profile == "HIGH_RISK":
            attendance_rate = round(random.uniform(50.0, 71.5), 1)
            lab_attendance = round(random.uniform(45.0, 70.0), 1)
            assignment_submission_rate = round(random.uniform(42.0, 68.0), 1)
            lms_logins_weekly = random.randint(1, 4)
            midterm_avg = round(random.uniform(32.0, 56.0), 1)
            current_gpa = round(random.uniform(4.0, 6.1), 2)
            prior_gpa = round(min(10.0, current_gpa + random.uniform(0.7, 1.8)), 2) # Steep GPA drop
            fee_overdue = random.random() < 0.35
            first_gen = random.random() < 0.45
            wellbeing_score = random.randint(2, 5) # 1-10 scale
            risk_label = "High"
            dropout_prob = round(random.uniform(68.0, 94.0), 1)
        elif profile == "MEDIUM_RISK":
            attendance_rate = round(random.uniform(72.0, 79.5), 1)
            lab_attendance = round(random.uniform(70.0, 82.0), 1)
            assignment_submission_rate = round(random.uniform(69.0, 82.0), 1)
            lms_logins_weekly = random.randint(4, 8)
            midterm_avg = round(random.uniform(55.0, 70.0), 1)
            current_gpa = round(random.uniform(6.2, 7.3), 2)
            prior_gpa = round(min(10.0, current_gpa + random.uniform(-0.3, 0.8)), 2)
            fee_overdue = random.random() < 0.15
            first_gen = random.random() < 0.30
            wellbeing_score = random.randint(5, 7)
            risk_label = "Medium"
            dropout_prob = round(random.uniform(32.0, 64.0), 1)
        else: # LOW_RISK
            attendance_rate = round(random.uniform(82.0, 98.0), 1)
            lab_attendance = round(random.uniform(85.0, 99.0), 1)
            assignment_submission_rate = round(random.uniform(85.0, 100.0), 1)
            lms_logins_weekly = random.randint(9, 22)
            midterm_avg = round(random.uniform(72.0, 96.0), 1)
            current_gpa = round(random.uniform(7.5, 9.8), 2)
            prior_gpa = round(min(10.0, max(6.0, current_gpa + random.uniform(-0.4, 0.4))), 2)
            fee_overdue = False
            first_gen = random.random() < 0.20
            wellbeing_score = random.randint(7, 10)
            risk_label = "Low"
            dropout_prob = round(random.uniform(4.0, 24.0), 1)

        # Generate semester GPA trajectory
        gpa_history = []
        base_gpa = prior_gpa
        for s in range(1, sem):
            jitter = round(random.uniform(-0.4, 0.4), 2)
            hist_val = max(4.0, min(10.0, round(base_gpa + jitter * (s - sem + 1), 2)))
            gpa_history.append({"semester": f"Sem {s}", "gpa": hist_val})
        gpa_history.append({"semester": f"Sem {sem}", "gpa": current_gpa})

        # Course grades & attendance breakdown
        dept_courses = COURSES_BY_DEPT.get(dept, COURSES_BY_DEPT["Computer Science & Engineering"])
        enrolled_courses = []
        for c in dept_courses:
            if profile == "HIGH_RISK":
                c_score = round(random.uniform(30.0, 60.0), 1)
                c_att = round(random.uniform(45.0, 75.0), 1)
            elif profile == "MEDIUM_RISK":
                c_score = round(random.uniform(58.0, 74.0), 1)
                c_att = round(random.uniform(70.0, 84.0), 1)
            else:
                c_score = round(random.uniform(75.0, 97.0), 1)
                c_att = round(random.uniform(82.0, 99.0), 1)
            
            enrolled_courses.append({
                "code": c["code"],
                "name": c["name"],
                "credits": c["credits"],
                "is_bottleneck": c["is_bottleneck"],
                "current_score": c_score,
                "attendance": c_att,
                "assignments_done": f"{int(c_att/20)}/5"
            })

        # Compute Explainable AI (XAI) risk factors
        top_risk_factors = []
        if attendance_rate < 75.0:
            top_risk_factors.append(f"Low overall attendance ({attendance_rate}%, statutory threshold 75%)")
        if (prior_gpa - current_gpa) >= 0.7:
            top_risk_factors.append(f"Steep GPA drop of {round(prior_gpa - current_gpa, 2)} pts since last semester")
        if assignment_submission_rate < 70.0:
            top_risk_factors.append(f"High LMS non-compliance ({assignment_submission_rate}% assignment submissions)")
        if lms_logins_weekly <= 4:
            top_risk_factors.append(f"Digital disengagement: Only {lms_logins_weekly} LMS logins/week")
        if midterm_avg < 50.0:
            top_risk_factors.append(f"Critical mid-term shortfall (Average score: {midterm_avg}%)")
        if wellbeing_score <= 4:
            top_risk_factors.append(f"Sentiment pulse warning: High stress/low wellbeing score ({wellbeing_score}/10)")
        if fee_overdue:
            top_risk_factors.append("Administrative fee clearance overdue (socio-economic stress factor)")
            
        if not top_risk_factors:
            top_risk_factors.append("Consistent academic progression across all parameters")

        students.append({
            "id": student_id,
            "name": f"{first_name} {last_name}",
            "email": email,
            "phone": f"+91 {random.randint(70000, 99999)} {random.randint(10000, 99999)}",
            "department": dept,
            "year": year,
            "semester": sem,
            "avatar_color": random.choice(["#3B82F6", "#10B981", "#8B5CF6", "#F59E0B", "#EC4899", "#06B6D4"]),
            "metrics": {
                "attendance_rate": attendance_rate,
                "lab_attendance": lab_attendance,
                "assignment_submission_rate": assignment_submission_rate,
                "lms_logins_weekly": lms_logins_weekly,
                "midterm_avg": midterm_avg,
                "current_gpa": current_gpa,
                "prior_gpa": prior_gpa,
                "gpa_delta": round(current_gpa - prior_gpa, 2),
                "fee_overdue": fee_overdue,
                "first_gen": first_gen,
                "wellbeing_score": wellbeing_score
            },
            "risk_assessment": {
                "level": risk_label,
                "dropout_probability": dropout_prob,
                "top_risk_factors": top_risk_factors[:3] # Top 3 Explainable AI reasons
            },
            "gpa_trajectory": gpa_history,
            "courses": enrolled_courses,
            "interventions": [
                {
                    "date": "2026-09-15",
                    "type": "Midterm Check-in",
                    "status": "Completed" if profile == "LOW_RISK" else "Pending Review",
                    "advisor": "Dr. S. Ramanathan"
                }
            ] if profile != "LOW_RISK" else []
        })

    return students

def save_default_dataset(filepath="app/data/students_db.json"):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    dataset = generate_student_dataset(num_students=360)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2)
    print(f"Dataset generated with {len(dataset)} student records at {filepath}")
    return dataset

if __name__ == "__main__":
    save_default_dataset()
