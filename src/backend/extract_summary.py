import re

NEXT_HEADERS = r'(?:summary|experience|skills|education|accomplishments?)'

def grab_section(text, header):
    pattern = rf'''^\s*{header}\s*:?[\r\n]+(.*?)(?=^\s*{NEXT_HEADERS}\s*:?\b | \Z)'''
    m = re.search(pattern, text, re.I | re.M | re.S | re.X)
    return m.group(1).strip() if m else ''

def extract_skills(text):
    skills_raw = grab_section(text, r'skills?')
    skills = [s.strip() for chunk in re.split(r'[\n,]', skills_raw)
              if (s := chunk.strip())]
    return skills

def extract_summary(text):
    summary_raw = grab_section(text, r'summary?')
    summary = [s.strip() for chunk in re.split(r'[\n]', summary_raw)
              if (s := chunk.strip())]
    return summary

def extract_experience(text):
    exp_raw = grab_section(text, r'(?:experience|professional experience|work history)')
    if not exp_raw:
        return []

    # date range:  "Jan 2014 – Present"  /  "01/2014 - 03/2016"  /  "2018 - 2020" / Jan 2024 to Present
    date_pattern = re.compile(
        r'([A-Za-z]{3,9}\s+\d{4}\s*(?:-|—|to)\s*(?:[A-Za-z]{3,9}\s+\d{4}|present|current)|'
        r'\d{1,2}/\d{4}\s*(?:-|—|to)\s*(?:\d{1,2}/\d{4}|present|current)|'
        r'\d{4}\s*(?:-|—|to)\s*(?:\d{4}|present|current))',
        re.I
    )

    parts = date_pattern.split(exp_raw)
    jobs = []

    for i in range(1, len(parts), 2):
        date_range = parts[i].strip()
        job_chunk = parts[i + 1].strip()

        if not job_chunk:
            continue

        lines = [ln.strip() for ln in job_chunk.splitlines() if ln.strip()]
        company_title = lines[0] if lines else ''

        if '—' in company_title or '–' in company_title or '-' in company_title:
            sep = '—' if '—' in company_title else ('–' if '–' in company_title else '-')
            company, _, after = company_title.partition(sep)
            company = company.strip()
            words = after.strip().split()
            location = ' '.join(words[:2]) if len(words) >= 2 else ''
            job_title = ' '.join(words[2:]) if len(words) > 2 else ''
        else:
            company, location, job_title = company_title, '', ''

        responsibilities = lines[1:] if len(lines) > 1 else []

        jobs.append({
            'date_range': date_range,
            'company': company,
            'location': location,
            'job_title': job_title,
            'responsibilities': responsibilities
        })

    return jobs

def extract_education(text):
    education_raw = grab_section(text, r'education')
    return [ln.strip() for ln in education_raw.splitlines() if ln.strip()]

def parse_resume(text):
    result = {
        'skills': extract_skills(text),
        'summary': extract_summary(text),
        'experience': extract_experience(text),
        'education': extract_education(text)
    }
    return result

def print_parse_result(parsed_data):
    print("=== RESUME PARSING RESULT ===\n\n")
    
    print("SKILLS:\n")
    for skill in parsed_data['skills']:
        print(f"• {skill}")
    print("\n")
    
    print("SUMMARY:\n")
    for summary_line in parsed_data['summary']:
        print(f"{summary_line}")
    print("\n")
    
    print("EXPERIENCE:\n")
    for job in parsed_data['experience']:
        print(f"\n{job['date_range']}")
        print(f"{job['company']}")
        if job['location']:
            print(f"{job['location']}")
        if job['job_title']:
            print(f"{job['job_title']}")
        
        if job['responsibilities']:
            print("Responsibilities:\n")
            for resp in job['responsibilities']:
                print(f"   • {resp}")

    print("EDUCATION: ")
    for education_line in parsed_data['education']:
        print(f"{education_line}")
    print("\n")

if __name__ == "__main__":
    text = """FOOD PREP CHEF
Skills
Highly skilled in cooking and preparing a variety of cuisines
Inborn ability to explore new cooking avenues
Thorough understanding of sanitation needs of the kitchen
Operate kitchen equipment such as ovens and grills for cooking purposes
Maintain knowledge of all recipes so that the Head Chef's place can be filled in effectively in case of absenteeism
Summary
Exceptional culinary insight.
Knowledge of standard food preparation
Ability to work in a high volume environment
Chef in preparing exceptional meals
Motivated food serving professional with 5+ years food and beverage experience in casual and fine dining.
Highlights
Kitchen productivity
Basic knife skills Sandwich preparation experience
Uses proper sanitation practices Knowledge of basic food preparation
Able to regularly lift/move up to 25-50 lbs Food handling knowledge
Preparation of various food items Italian cuisine
Good personal hygiene American cuisine
Team-oriented Ethnic foods preparation
Well groomed Plate presentation skills
High level of cleanly kitchen maintenance Banquet operations and off-site catering expert
Team-oriented
Accomplishments
Serve Safe 2015
Seasoned and cooked food according to recipes or personal judgment and experience.
Ensured consistent high quality of plate presentation.
Maintained contact with kitchen staff, management, serving staff and customers.
Baked, roasted, broiled, and steamed meats, fish, vegetables and other foods.
Supported all kitchen operations when chef was absent.
Experience
09/2010 - 04/2011
Company Name ï¼​ City , State Food Prep Chef
Followed all established restaurant practices and procedures.
Carefully maintained sanitation, health and safety standards in all work areas.
Prepared items according to written or verbal orders, working on several different orders simultaneously.
06/2011 - 11/2012
Company Name ï¼​ City , State Cook
Followed all established restaurant practices and procedures.
Maintained a neat, well groomed appearance including impeccable personal hygiene, hair restraint and minimal jewelry that
met company standards.
Closely followed standard procedures for safe food preparation, assembly and presentation to ensure customer satisfaction.
Cut and chopped food items and cooked on a grill or in fryers.
12/2012 - 03/2013
Company Name ï¼​ City , State Cook
Operated large-volume cooking equipment such as grills, deep-fat fryers and griddles.
Took necessary steps to meet customer needs and effectively resolve food or service issues.
Served fresh, hot food with a smile in a timely manner.
Accurately measured ingredients required for specific food items.
Followed all established restaurant practices and procedures.
02/2013 - 06/2013
Company Name ï¼​ City , State Cook
Assisted co-workers.Assisted co-workers.
Cooked food properly and in a timely fashion, using safety precautions
Weighed, measured, and mixed ingredients according to recipes using various kitchen utensils and equipment
Cleaned and prepared various foods for cooking or serving
06/2014 - 11/2014
Company Name ï¼​ City , State Chef
Developed strategies to enhance catering and retail food service revenue and productivity goals.
Prepared healthy, enjoyable breakfasts and dinners for diners.
Effectively managed and assisted kitchen staff in producing food for banquets, catered events and member dining areas.
Effectively used items in stock to decrease waste and profit loss.
Ensured consistent high quality of plate presentation
Seasoned and cooked food according to recipes or personal judgment and experience
Created and explored new cuisines
Instructed cooks and other workers in the preparation, cooking, garnishing, and presentation of food
Cooked food properly and in a timely fashion, using safety precautions
Used all food handling standards
01/2014 - 12/2014
Company Name ï¼​ City , State Food Service Cook /Temp
Assisted co-workers.
Performed kitchen maintenance for a private facility.
Responsible for daily set up of five stations.
Stocked and rotated products, stocked supplies, and paper goods in a timely basis
Stored clean equipment and utensils
Supervised and coordinated activities of cooks and workers engaged in food preparation
Used all food handling standards
Cleaned, cut, and cooked meat, fish, or poultry
Complied with scheduled kitchen sanitation and ensured all standards and practices were met
Cooked food properly and in a timely fashion, using safety precautions
01/2015 - 05/2015
Company Name ï¼​ City , State Line Cook
Consistently verified that kitchen staff followed all recipes and portioned serving guidelines correctly.
Consistently kept a clean and safe environment by adhering to all federal, state and local sanitation and safety requirements.
Communicated clearly and positively with co-workers and management.
Worked well with teammates and openly invited coaching from the management team.
Followed all established restaurant practices and procedures.
Education
2011
William M Davies Career & Tech ï¼​ City , State , USA High School Diploma : Culinary/ Auto Body
Courses in Hospitality and Restaurant Management
Classes in Restaurant and Facility Operations
Basic Vocational : Prep Cook
Courses in: Food Preparation, Kitchen Management,Patisserie and Confectionery, International Cuisine"""
    parsed_data = parse_resume(text)
    print_parse_result(parsed_data)
    
