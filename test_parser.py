from parsers.resume_parser import ResumeParser

# Test the parser with a sample resume
parser = ResumeParser("data/samples/resumes/resume1.pdf")
result = parser.parse()
print(result)