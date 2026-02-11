from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Career metadata: descriptions, roadmaps, courses, salary
CAREER_INFO = {
    'Backend Developer': {
        'description': 'Build server-side logic, APIs, and databases',
        'roadmap': ['Learn Python/JavaScript/Java', 'Understand databases (SQL/NoSQL)', 'Learn frameworks (Flask/Django/Node.js/Spring)', 'Practice API design & REST'],
        'courses': ['Udemy: REST API with Python & Flask', 'Coursera: CS50 Backend Track', 'freeCodeCamp: Backend Development'],
        'salary': '₹6-12 LPA (India) | $90k-150k USD'
    },
    'Frontend Developer': {
        'description': 'Create user interfaces and web experiences',
        'roadmap': ['Master HTML/CSS', 'Learn JavaScript/TypeScript', 'Learn React/Vue/Angular', 'Master responsive design & accessibility'],
        'courses': ['Udemy: The Complete JavaScript Course', 'freeCodeCamp: Responsive Web Design', 'Coursera: React for Beginners'],
        'salary': '₹5-10 LPA (India) | $80k-120k USD'
    },
    'Full Stack Developer': {
        'description': 'Work on both frontend and backend aspects of applications',
        'roadmap': ['Master frontend (HTML/CSS/JS)', 'Learn backend (Python/Node.js/Java)', 'Learn databases & APIs', 'Deploy & DevOps basics'],
        'courses': ['Udemy: MERN Stack Course', 'The Odin Project', 'Codecademy: Full Stack Path'],
        'salary': '₹8-15 LPA (India) | $120k-180k USD'
    },
    'AI/ML Engineer': {
        'description': 'Develop machine learning models and AI applications',
        'roadmap': ['Strong Python foundation', 'Learn Math (Statistics/Linear Algebra)', 'Learn TensorFlow/PyTorch/scikit-learn', 'Practice ML projects on real data'],
        'courses': ['Coursera: Andrew Ng Machine Learning Specialization', 'Fast.ai: Practical Deep Learning', 'freeCodeCamp: ML with Python'],
        'salary': '₹8-20 LPA (India) | $120k-200k USD'
    },
    'Data Scientist': {
        'description': 'Analyze complex data and build predictive models',
        'roadmap': ['Master Python/R', 'Learn statistics & probability', 'Learn ML algorithms & visualization', 'Practice with real datasets'],
        'courses': ['Coursera: Data Science Specialization', 'DataCamp: Data Science with Python', 'Udacity: Data Scientist Nanodegree'],
        'salary': '₹8-18 LPA (India) | $100k-180k USD'
    },
    'Data Analyst': {
        'description': 'Extract insights from data using analysis and visualization',
        'roadmap': ['Learn SQL & databases', 'Master Python/R for data analysis', 'Learn visualization (Tableau/Power BI)', 'Practice business analytics'],
        'courses': ['Coursera: Google Data Analytics Certificate', 'Udemy: Complete SQL + Python for Data', 'DataCamp: Data Analysis path'],
        'salary': '₹6-12 LPA (India) | $70k-130k USD'
    },
    'DevOps Engineer': {
        'description': 'Manage infrastructure, automation, and deployment pipelines',
        'roadmap': ['Learn Linux & shell scripting', 'Master Docker & Kubernetes', 'Learn CI/CD tools (Jenkins/GitHub Actions)', 'Cloud platforms (AWS/Azure/GCP)'],
        'courses': ['Linux Academy: Docker & Kubernetes', 'Udemy: Docker & Kubernetes Complete Guide', 'A Cloud Guru: AWS Solutions Architect'],
        'salary': '₹8-16 LPA (India) | $110k-180k USD'
    },
    'Cloud Architect': {
        'description': 'Design and implement cloud-based solutions and infrastructure',
        'roadmap': ['Learn Linux & networking', 'Master AWS/Azure/GCP', 'Understand scalability & security', 'Learn Infrastructure as Code (Terraform)'],
        'courses': ['Coursera: AWS Certified Solutions Architect', 'Linux Academy: Cloud Architecture', 'A Cloud Guru: Azure Fundamentals'],
        'salary': '₹12-25 LPA (India) | $140k-220k USD'
    },
    'Mobile Developer': {
        'description': 'Build iOS and Android applications',
        'roadmap': ['Learn Java/Kotlin for Android or Swift for iOS', 'Master mobile UI/UX principles', 'Learn Firebase for backend', 'Publish apps to stores'],
        'courses': ['Udemy: Complete Android App Development', 'Coursera: iOS App Development', 'freeCodeCamp: Mobile App Development'],
        'salary': '₹6-14 LPA (India) | $90k-160k USD'
    },
    'Systems Engineer': {
        'description': 'Design and maintain robust system architectures',
        'roadmap': ['Learn C++/Go/Rust', 'Understand operating systems', 'Learn networking & protocols', 'Master performance optimization'],
        'courses': ['Udemy: Systems Programming', 'MIT OpenCourseWare: Advanced Systems', 'Coursera: Computer Networking'],
        'salary': '₹10-18 LPA (India) | $110k-190k USD'
    },
    'Blockchain Developer': {
        'description': 'Build decentralized applications and smart contracts',
        'roadmap': ['Learn Solidity & web3 basics', 'Understand blockchain fundamentals', 'Learn contract development (Ethereum)', 'Practice DApp development'],
        'courses': ['Udemy: Solidity & Ethereum Development', 'Coursera: Blockchain Specialization', 'ConsenSys Ethereum Developer Course'],
        'salary': '₹10-20 LPA (India) | $120k-200k USD'
    },
    'Security Engineer': {
        'description': 'Protect systems and applications from cyber threats',
        'roadmap': ['Learn networking & Linux', 'Master security principles', 'Learn ethical hacking & penetration testing', 'Get certifications (CEH/OSCP)'],
        'courses': ['Udemy: Ethical Hacking & Cybersecurity', 'eLearnSecurity: CEH Certification', 'TryHackMe: Security Training'],
        'salary': '₹8-18 LPA (India) | $100k-180k USD'
    },
    'Game Developer': {
        'description': 'Create interactive games for various platforms',
        'roadmap': ['Learn C# & game engines (Unity)', 'Understand game physics & design', 'Learn graphics & animation', 'Publish games to platforms'],
        'courses': ['Udemy: Complete C# Unity Developer', 'Unity Learn: Game Development', 'Coursera: Game Design & Development'],
        'salary': '₹6-14 LPA (India) | $80k-150k USD'
    }
}


def recommend_careers(skills, skill_level='Beginner'):
    """
    Recommend careers based on skills and level.
    skill_level: 'Beginner', 'Intermediate', 'Advanced'
    """
    skills_set = set(skills or [])
    careers = set()

    if not skills_set:
        return []

    # Programming Language Base Mappings
    if 'Python' in skills_set:
        careers.update(['Backend Developer', 'AI/ML Engineer', 'Data Analyst', 'Data Scientist'])

    if 'JavaScript' in skills_set:
        careers.add('Frontend Developer')
        if 'Node.js' in skills_set:
            careers.add('Backend Developer')

    if 'TypeScript' in skills_set:
        careers.update(['Frontend Developer', 'Backend Developer'])

    if 'Java' in skills_set:
        careers.update(['Backend Developer', 'Mobile Developer', 'Systems Engineer'])

    if 'C++' in skills_set or 'Rust' in skills_set or 'Go' in skills_set:
        careers.update(['Systems Engineer', 'Backend Developer'])

    if 'C#' in skills_set:
        careers.update(['Game Developer', 'Backend Developer', 'Mobile Developer'])

    if 'Swift' in skills_set or 'Kotlin' in skills_set:
        careers.add('Mobile Developer')

    if 'Solidity' in skills_set:
        careers.add('Blockchain Developer')

    if 'PHP' in skills_set:
        careers.add('Backend Developer')

    # Frontend Skills
    if 'HTML' in skills_set and 'CSS' in skills_set:
        careers.add('Frontend Developer')

    if 'React' in skills_set or 'Angular' in skills_set or 'Vue' in skills_set:
        careers.add('Frontend Developer')

    if 'Webpack' in skills_set or 'Bootstrap' in skills_set:
        careers.add('Frontend Developer')

    # Backend Frameworks
    if 'Django' in skills_set or 'Flask' in skills_set:
        careers.add('Backend Developer')

    if 'Spring Boot' in skills_set or 'Express.js' in skills_set:
        careers.add('Backend Developer')

    # Data & ML Skills
    if 'SQL' in skills_set:
        careers.update(['Data Analyst', 'Backend Developer', 'Data Scientist'])

    if 'NoSQL' in skills_set or 'MongoDB' in skills_set:
        careers.update(['Backend Developer', 'Data Analyst'])

    if 'Tableau' in skills_set or 'Power BI' in skills_set:
        careers.add('Data Analyst')

    if 'Machine Learning' in skills_set or 'TensorFlow' in skills_set or 'PyTorch' in skills_set:
        careers.update(['AI/ML Engineer', 'Data Scientist'])

    if 'scikit-learn' in skills_set or 'Pandas' in skills_set or 'NumPy' in skills_set:
        careers.update(['Data Scientist', 'Data Analyst'])

    # DevOps & Cloud Skills
    if 'Docker' in skills_set or 'Kubernetes' in skills_set:
        careers.add('DevOps Engineer')

    if 'AWS' in skills_set or 'Azure' in skills_set or 'GCP' in skills_set:
        careers.update(['DevOps Engineer', 'Cloud Architect'])

    if 'Terraform' in skills_set or 'Ansible' in skills_set:
        careers.add('DevOps Engineer')

    if 'CI/CD' in skills_set or 'Jenkins' in skills_set or 'GitHub Actions' in skills_set:
        careers.add('DevOps Engineer')

    # Linux & System Skills
    if 'Linux' in skills_set or 'bash' in skills_set:
        careers.update(['DevOps Engineer', 'Systems Engineer', 'Security Engineer'])

    # Security Skills
    if 'Cybersecurity' in skills_set or 'Networking' in skills_set:
        careers.add('Security Engineer')

    if 'Ethical Hacking' in skills_set or 'Penetration Testing' in skills_set:
        careers.add('Security Engineer')

    # Game Development
    if 'Unity' in skills_set or 'Unreal' in skills_set:
        careers.add('Game Developer')

    # Combination rules
    if {'HTML', 'CSS', 'JavaScript'}.issubset(skills_set):
        careers.add('Frontend Developer')

    if 'JavaScript' in skills_set and ('Node.js' in skills_set or 'Express.js' in skills_set):
        careers.add('Backend Developer')

    if {'HTML', 'CSS', 'JavaScript', 'Python'}.issubset(skills_set) or \
       {'HTML', 'CSS', 'JavaScript', 'Node.js'}.issubset(skills_set):
        careers.add('Full Stack Developer')

    if 'SQL' in skills_set and 'Python' in skills_set:
        careers.update(['Data Analyst', 'Backend Developer'])

    if 'Machine Learning' in skills_set and 'Python' in skills_set:
        careers.update(['AI/ML Engineer', 'Data Scientist'])

    # Advanced level unlocks premium roles
    if skill_level == 'Advanced':
        if 'Python' in skills_set:
            careers.add('AI/ML Engineer')
        if 'Docker' in skills_set or 'Kubernetes' in skills_set:
            careers.add('Cloud Architect')
        if 'Cybersecurity' in skills_set:
            careers.add('Security Engineer')

    return sorted(careers)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/recommend', methods=['POST'])
def recommend():
    payload = request.get_json(silent=True) or {}
    skills = payload.get('skills', [])
    skill_level = payload.get('skillLevel', 'Beginner')
    
    careers = recommend_careers(skills, skill_level)
    
    # Enrich with career details
    recommendations = []
    for career in careers:
        info = CAREER_INFO.get(career, {})
        recommendations.append({
            'name': career,
            'description': info.get('description', ''),
            'roadmap': info.get('roadmap', []),
            'courses': info.get('courses', []),
            'salary': info.get('salary', '')
        })
    
    return jsonify({
        'skills': skills,
        'skillLevel': skill_level,
        'careers': recommendations,
    })


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
