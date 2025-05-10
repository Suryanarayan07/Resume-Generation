import streamlit as st
from weasyprint import HTML, CSS
from io import BytesIO

# Initialize session state with default values
def initialize_session_state():
    defaults = {
        'personal_info': {
            'name': 'Alex Johnson',
            'email': 'alex.johnson@example.com',
            'phone': '(555) 123-4567',
            'linkedin': 'linkedin.com/in/alexjohnson',
            'summary': 'Experienced software engineer with 5+ years in full-stack development. Specialized in building scalable web applications and optimizing system performance.'
        },
        'education': [{
            'degree': 'M.S. Computer Science',
            'institution': 'Stanford University',
            'year': '2016-2018',
            'achievements': 'Graduated with honors, GPA: 3.8'
        }],
        'work_experience': [{
            'position': 'Senior Software Engineer',
            'company': 'TechCorp',
            'duration': '2020-Present',
            'responsibilities': [
                'Led team developing SaaS platform with 50k+ users',
                'Reduced API response time by 40% through optimization'
            ]
        }],
        'skills': [
            {'name': 'Python', 'level': 'Expert'},
            {'name': 'JavaScript', 'level': 'Advanced'},
            {'name': 'Cloud Architecture', 'level': 'Advanced'}
        ],
        'projects': [{
            'name': 'AI Resume Analyzer',
            'description': 'Built NLP system to match resumes with job descriptions',
            'technologies': 'Python, TensorFlow, NLTK'
        }],
        'certifications': [{
            'name': 'AWS Certified Solutions Architect',
            'issuer': 'Amazon Web Services',
            'year': '2022'
        }]
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Personal Information Section
def personal_info_section():
    st.header("🧑‍💼 Personal Information")
    with st.expander("Edit Personal Details", expanded=True):
        info = st.session_state.personal_info
        cols = st.columns(2)
        
        with cols[0]:
            info['name'] = st.text_input("Full Name", value=info['name'])
            info['email'] = st.text_input("Email", value=info['email'])
        
        with cols[1]:
            info['phone'] = st.text_input("Phone", value=info['phone'])
            info['linkedin'] = st.text_input("LinkedIn", value=info['linkedin'])
        
        info['summary'] = st.text_area("Professional Summary", 
                                     value=info['summary'],
                                     height=100)

# Education Section
def education_section():
    st.header("🎓 Education")
    with st.expander("Add/Edit Education", expanded=True):
        for i, edu in enumerate(st.session_state.education):
            st.subheader(f"Education #{i+1}")
            
            cols = st.columns([2, 1])
            with cols[0]:
                edu['degree'] = st.text_input("Degree", value=edu['degree'], key=f"degree_{i}")
            with cols[1]:
                edu['institution'] = st.text_input("Institution", value=edu['institution'], key=f"institution_{i}")
            
            cols = st.columns([1, 1, 2])
            with cols[0]:
                edu['year'] = st.text_input("Year", value=edu['year'], key=f"year_{i}")
            with cols[1]:
                edu['gpa'] = st.text_input("GPA", value=edu.get('gpa', ''), key=f"gpa_{i}")
            
            edu['achievements'] = st.text_area("Achievements", value=edu['achievements'], key=f"achievements_{i}")
            
            if st.button(f"Remove Education #{i+1}", key=f"remove_edu_{i}"):
                st.session_state.education.pop(i)
                st.rerun()
        
        if st.button("➕ Add Education"):
            st.session_state.education.append({
                'degree': '',
                'institution': '',
                'year': '',
                'achievements': ''
            })
            st.rerun()

# Work Experience Section
def experience_section():
    st.header("💼 Work Experience")
    with st.expander("Add/Edit Experience", expanded=True):
        for i, exp in enumerate(st.session_state.work_experience):
            st.subheader(f"Experience #{i+1}")
            
            cols = st.columns([2, 2])
            with cols[0]:
                exp['position'] = st.text_input("Position", value=exp['position'], key=f"position_{i}")
            with cols[1]:
                exp['company'] = st.text_input("Company", value=exp['company'], key=f"company_{i}")
            
            exp['duration'] = st.text_input("Duration", value=exp['duration'], key=f"duration_{i}")
            
            st.write("Responsibilities:")
            for j, resp in enumerate(exp['responsibilities']):
                cols = st.columns([4, 1])
                with cols[0]:
                    exp['responsibilities'][j] = st.text_input(
                        f"Responsibility #{j+1}", 
                        value=resp,
                        key=f"resp_{i}_{j}"
                    )
            
            if st.button("➕ Add Responsibility", key=f"add_resp_{i}"):
                exp['responsibilities'].append("")
                st.rerun()
            
            if st.button(f"Remove Experience #{i+1}", key=f"remove_exp_{i}"):
                st.session_state.work_experience.pop(i)
                st.rerun()
        
        if st.button("➕ Add Experience"):
            st.session_state.work_experience.append({
                'position': '',
                'company': '',
                'duration': '',
                'responsibilities': ['']
            })
            st.rerun()

# Skills Section
def skills_section():
    st.header("🛠️ Skills")
    with st.expander("Add/Edit Skills", expanded=True):
        for i, skill in enumerate(st.session_state.skills):
            cols = st.columns([3, 2, 1])
            with cols[0]:
                skill['name'] = st.text_input("Skill", value=skill['name'], key=f"skill_name_{i}")
            with cols[1]:
                skill['level'] = st.selectbox(
                    "Level",
                    ["Beginner", "Intermediate", "Advanced", "Expert"],
                    index=["Beginner", "Intermediate", "Advanced", "Expert"].index(
                        skill.get('level', 'Intermediate')
                    ),
                    key=f"skill_level_{i}"
                )
            with cols[2]:
                if st.button("❌", key=f"remove_skill_{i}"):
                    st.session_state.skills.pop(i)
                    st.rerun()
        
        if st.button("➕ Add Skill"):
            st.session_state.skills.append({'name': '', 'level': 'Intermediate'})
            st.rerun()

# Projects Section
def projects_section():
    st.header("📂 Projects")
    with st.expander("Add/Edit Projects", expanded=True):
        for i, project in enumerate(st.session_state.projects):
            st.subheader(f"Project #{i+1}")
            
            project['name'] = st.text_input("Name", value=project['name'], key=f"project_name_{i}")
            
            project['description'] = st.text_area("Description", 
                                                value=project.get('description', ''),
                                                height=100,
                                                key=f"project_desc_{i}")
            
            project['technologies'] = st.text_input("Technologies", 
                                                  value=project.get('technologies', ''),
                                                  key=f"project_tech_{i}")
            
            if st.button(f"Remove Project #{i+1}", key=f"remove_project_{i}"):
                st.session_state.projects.pop(i)
                st.rerun()
        
        if st.button("➕ Add Project"):
            st.session_state.projects.append({
                'name': '',
                'description': '',
                'technologies': ''
            })
            st.rerun()

# Certifications Section
def certifications_section():
    st.header("🏆 Certifications")
    with st.expander("Add/Edit Certifications", expanded=True):
        for i, cert in enumerate(st.session_state.certifications):
            st.subheader(f"Certification #{i+1}")
            
            cols = st.columns([3, 2, 1])
            with cols[0]:
                cert['name'] = st.text_input("Name", value=cert['name'], key=f"cert_name_{i}")
            with cols[1]:
                cert['issuer'] = st.text_input("Issuer", value=cert.get('issuer', ''), key=f"cert_issuer_{i}")
            with cols[2]:
                cert['year'] = st.text_input("Year", value=cert.get('year', ''), key=f"cert_year_{i}")
            
            if st.button(f"Remove Certification #{i+1}", key=f"remove_cert_{i}"):
                st.session_state.certifications.pop(i)
                st.rerun()
        
        if st.button("➕ Add Certification"):
            st.session_state.certifications.append({
                'name': '',
                'issuer': '',
                'year': ''
            })
            st.rerun()

def generate_designer_pdf():
    """Generate a single-page, two-column professional PDF resume"""
    css = CSS(string='''
    @page {
        size: A4;
        margin: 0;
    }
    body {
        font-family: 'Helvetica', sans-serif;
        line-height: 1.5;
        color: #333;
        margin: 0;
        padding: 0;
        display: flex;
        min-height: 29.7cm;
    }
    .resume-container {
        display: flex;
        width: 100%;
        height: 100%;
    }
    .sidebar {
        width: 35%;
        background: #2E86C1;
        color: white;
        padding: 2rem 1.5rem;
    }
    .main-content {
        width: 65%;
        padding: 2rem 1.5rem;
    }
    .header {
        margin-bottom: 1.5rem;
    }
    h1 {
        font-size: 1.8rem;
        margin: 0 0 0.5rem 0;
        color: white;
    }
    .contact-info {
        font-size: 0.9rem;
        margin-bottom: 1rem;
        color: white;
    }
    h2 {
        font-size: 1.3rem;
        margin: 1.5rem 0 0.8rem 0;
        color: white;
        border-bottom: 2px solid rgba(255,255,255,0.3);
        padding-bottom: 0.3rem;
    }
    .main-content h2 {
        color: #2E86C1;
        border-bottom: 2px solid #2E86C1;
    }
    .skill-item {
        margin-bottom: 1rem;
    }
    .skill-name {
        font-weight: bold;
        margin-bottom: 0.3rem;
        color: white;
    }
    .skill-bar {
        height: 6px;
        background: rgba(255,255,255,0.2);
        border-radius: 3px;
        overflow: hidden;
    }
    .skill-level {
        height: 100%;
        background: white;
    }
    .experience-item {
        margin-bottom: 1.5rem;
    }
    .job-title {
        font-weight: bold;
        font-size: 1.1rem;
    }
    .company-duration {
        font-style: italic;
        margin: 0.2rem 0;
        color: #666;
    }
    ul {
        padding-left: 1.2rem;
        margin: 0.5rem 0;
    }
    li {
        margin-bottom: 0.3rem;
    }
    .compact-section {
        margin-bottom: 1rem;
    }
    .white-text {
        color: white;
    }
    ''')

    # Skill level mapping
    skill_levels = {
        'Beginner': '30%',
        'Intermediate': '60%',
        'Advanced': '80%',
        'Expert': '100%'
    }

    # Build HTML content
    html_content = f"""
    <div class="resume-container">
        <div class="sidebar">
            <div class="header">
                <h1>{st.session_state.personal_info['name']}</h1>
                <div class="contact-info">
                    {st.session_state.personal_info['email']}<br>
                    {st.session_state.personal_info['phone']}<br>
                    {st.session_state.personal_info['linkedin']}
                </div>
            </div>

            <h2>Professional Summary</h2>
            <div class="white-text">{st.session_state.personal_info['summary']}</div>

            <h2>Skills</h2>
            {"".join([
                f'<div class="skill-item">'
                f'<div class="skill-name">{skill["name"]}</div>'
                f'<div class="skill-bar">'
                f'<div class="skill-level" style="width:{skill_levels.get(skill["level"], "50%")}"></div>'
                f'</div></div>'
                for skill in st.session_state.skills
            ])}

            <h2>Certifications</h2>
            {"".join([
                f'<div class="compact-section white-text">'
                f'<strong>{cert["name"]}</strong><br>'
                f'{cert.get("issuer", "")} ({cert.get("year", "")})'
                f'</div>'
                for cert in st.session_state.certifications
            ])}
        </div>

        <div class="main-content">
            <h2>Professional Experience</h2>
            {"".join([
                f'<div class="experience-item">'
                f'<div class="job-title">{exp["position"]}</div>'
                f'<div class="company-duration">{exp["company"]} | {exp["duration"]}</div>'
                f'<ul>{"".join([f"<li>{resp}</li>" for resp in exp["responsibilities"]])}</ul>'
                f'</div>'
                for exp in st.session_state.work_experience
            ])}

            <h2>Education</h2>
            {"".join([
                f'<div class="experience-item">'
                f'<div class="job-title">{edu["degree"]}</div>'
                f'<div class="company-duration">{edu["institution"]} | {edu["year"]}</div>'
                f'<div>{edu.get("achievements", "")}</div>'
                f'</div>'
                for edu in st.session_state.education
            ])}

            <h2>Projects</h2>
            {"".join([
                f'<div class="experience-item">'
                f'<div class="job-title">{project["name"]}</div>'
                f'<div>{project.get("description", "")}</div>'
                f'<div><em>Technologies: {project.get("technologies", "")}</em></div>'
                f'</div>'
                for project in st.session_state.projects
            ])}
        </div>
    </div>
    """

    # Generate PDF
    pdf_bytes = HTML(string=html_content).write_pdf(
        stylesheets=[css],
        presentational_hints=True
    )
    return BytesIO(pdf_bytes)

def generate_resume():
    st.header("📄 Generate Resume")
    
    if st.button("✨ Generate Professional PDF", type="primary"):
        with st.spinner("Creating your single-page resume..."):
            try:
                pdf_buffer = generate_designer_pdf()
                
                st.success("Professional resume generated!")
                st.download_button(
                    label="⬇️ Download PDF",
                    data=pdf_buffer,
                    file_name="professional_resume.pdf",
                    mime="application/pdf"
                )
                
            except Exception as e:
                st.error(f"Failed to generate PDF: {str(e)}")

def main():
    st.set_page_config(
        page_title="Professional Resume Builder",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    if 'initialized' not in st.session_state:
        initialize_session_state()
        st.session_state.initialized = True
    
    # Sidebar with actions
    with st.sidebar:
        st.title("Resume Builder")
        st.markdown("Build your perfect resume")
        
        if st.button("🔄 Reset to Defaults"):
            initialize_session_state()
            st.rerun()
    
    # Main content sections
    personal_info_section()
    education_section()
    experience_section()
    skills_section()
    projects_section()
    certifications_section()
    
    generate_resume()

if __name__ == "__main__":
    main()
