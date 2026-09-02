import subprocess

import pandas as pd
import streamlit as st

# --- Đường dẫn cố định trong container ---
ENROLLMENT_CSV = "/app/data/processed/Enrollment.csv"
COURSE_CSV = "/app/data/processed/Course.csv"
STUDENT_CSV = "/app/data/processed/Student.csv"

JOB1_DIR = "/app/src/jobs/course_name_student_pass_fail_count"
JOB2_DIR = "/app/src/jobs/student_list_by_course_gender_score_range"


def run_pipeline(cmd):
    """Chạy 1 lệnh shell (pipe mapper | sort | reducer), trả về stdout dạng text."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        st.error(f"Lỗi khi chạy job:\n{result.stderr}")
        return ""
    return result.stdout


@st.cache_data
def load_job1():
    """Job: đếm số lượng Pass/Fail (letter grade) theo từng môn học."""
    cmd = f"cat {COURSE_CSV} {ENROLLMENT_CSV} | python3 {JOB1_DIR}/mapper.py | sort | python3 {JOB1_DIR}/reducer.py"
    output = run_pipeline(cmd)

    rows = []
    for line in output.strip().split("\n"):
        if not line:
            continue
        course_name, grade, count = line.split("\t")
        rows.append({"Course": course_name, "Grade": grade, "Count": int(count)})

    return pd.DataFrame(rows)


@st.cache_data
def load_job2():
    """Job: danh sách sinh viên theo môn học, giới tính, khoảng điểm."""
    cmd = f"cat {ENROLLMENT_CSV} | python3 {JOB2_DIR}/mapper.py | sort | python3 {JOB2_DIR}/reducer.py"
    output = run_pipeline(cmd)

    rows = []
    for line in output.strip().split("\n"):
        if not line:
            continue
        course_name, gender, score_range, students_str = line.split("\t")
        students = [s.strip() for s in students_str.split(",")]
        rows.append(
            {
                "Course": course_name,
                "Gender": gender,
                "ScoreRange": score_range,
                "StudentCount": len(students),
                "Students": students_str,
            }
        )

    return pd.DataFrame(rows)


# ============================================================
# UI
# ============================================================

st.set_page_config(page_title="Student Data Analytics", layout="wide")
st.title("📊 Student Data Analytics — Dashboard")

tab1, tab2 = st.tabs(
    ["✅ Pass/Fail theo môn học", "👥 Danh sách sinh viên theo môn/giới tính/khoảng điểm"]
)

# ------------------------------------------------------------
# TAB 1: Pass/Fail count theo môn
# ------------------------------------------------------------
with tab1:
    st.subheader("Số lượng điểm chữ (A/B/C/D/F) theo từng môn học")

    col_a, col_b = st.columns([1, 4])
    with col_a:
        if st.button("🔄 Chạy lại job", key="rerun_job1"):
            load_job1.clear()

    df1 = load_job1()

    if df1.empty:
        st.warning("Không có dữ liệu. Kiểm tra lại job hoặc dữ liệu nguồn.")
    else:
        courses = sorted(df1["Course"].unique())
        selected_courses = st.multiselect(
            "Lọc theo môn học", courses, default=courses[:5], key="filter_job1_courses"
        )

        filtered_df1 = df1[df1["Course"].isin(selected_courses)] if selected_courses else df1

        st.dataframe(filtered_df1, use_container_width=True)

        # Biểu đồ: pivot Course x Grade
        pivot = filtered_df1.pivot_table(
            index="Course", columns="Grade", values="Count", fill_value=0
        )
        st.bar_chart(pivot)

# ------------------------------------------------------------
# TAB 2: Danh sách sinh viên theo môn/giới tính/khoảng điểm
# ------------------------------------------------------------
with tab2:
    st.subheader("Danh sách sinh viên theo điều kiện lọc")

    col_a, col_b = st.columns([1, 4])
    with col_a:
        if st.button("🔄 Chạy lại job", key="rerun_job2"):
            load_job2.clear()

    df2 = load_job2()

    if df2.empty:
        st.warning("Không có dữ liệu. Kiểm tra lại job hoặc dữ liệu nguồn.")
    else:
        col1, col2, col3 = st.columns(3)

        with col1:
            course_filter = st.selectbox(
                "Môn học", ["Tất cả"] + sorted(df2["Course"].unique().tolist())
            )
        with col2:
            gender_filter = st.selectbox("Giới tính", ["Tất cả", "Male", "Female"])
        with col3:
            score_range_filter = st.selectbox(
                "Khoảng điểm", ["Tất cả", "0-2", "2-4", "4-6", "6-8", "8-10"]
            )

        filtered_df2 = df2.copy()
        if course_filter != "Tất cả":
            filtered_df2 = filtered_df2[filtered_df2["Course"] == course_filter]
        if gender_filter != "Tất cả":
            filtered_df2 = filtered_df2[filtered_df2["Gender"] == gender_filter]
        if score_range_filter != "Tất cả":
            filtered_df2 = filtered_df2[filtered_df2["ScoreRange"] == score_range_filter]

        st.dataframe(
            filtered_df2[["Course", "Gender", "ScoreRange", "StudentCount", "Students"]],
            use_container_width=True,
        )

        st.metric("Tổng số sinh viên (theo bộ lọc hiện tại)", int(filtered_df2["StudentCount"].sum()))