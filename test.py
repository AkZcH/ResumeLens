from parsers.jd_pipeline import parse_jd_pipeline

jd_text = """
We are hiring a Backend Developer for Bangalore Office.
Responsibilities include developing REST APIs, writing SQL queries,
working with AWS, Docker, and collaborating with product managers.
Preferred experience: 2+ years, knowledge of Node.js or Python.
"""

result = parse_jd_pipeline(jd_text)

print(result)
