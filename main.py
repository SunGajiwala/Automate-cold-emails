import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import psycopg2
import credentials as cred

dbname=cred.dbname
user=cred.user
password=cred.password

try:
    connection = psycopg2.connect(
        dbname = dbname,
        user= user,
        password = password,
        host="localhost",
        port="5432"
    )
    cursor = connection.cursor()
except Exception as e:
        print(f"Error: {e}")

sql_query = """
Select * from users where created_at >= '2024-04-01' and name like 'Sun%'
"""
df = pd.read_sql(sql_query,connection)
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Email configuration
email_address = cred.email_address
email_password = cred.email_password
smtp_server = 'smtp.gmail.com'
smtp_port = 587

# Compose Email
subject = "Exploring job Opportunities"
body_template = """
Dear {name},

I trust this message finds you thriving. My name is Sun Gajiwala, and I am reaching out with great anticipation regarding potential career prospects within your distinguished organization.

Currently steering the data engineering efforts at K P Sanghvi Inc., I bring over 3+ years of hands-on experience in sculpting data landscapes to uncover actionable insights. My journey further advanced with the acquisition of a Master's degree in Data Science in May 2023, igniting a passion for the boundless possibilities at the intersection of data and innovation.

The prospect of joining forces with {company} resonates deeply with me, not only for its trailblazing reputation but also for its unwavering dedication. Enthusiastic about driving transformation through data-driven strategies, I am eager to contribute my expertise to fueling your organization's journey towards excellence.

Attached is my resume for your perusal, offering a glimpse into my professional trajectory. Additionally, I invite you to delve deeper into my journey via my LinkedIn profile: https://www.linkedin.com/in/sun-gajiwala/

I am keen to explore potential synergies and discuss how my skills align with the dynamic needs of your team. Would you be open to a conversation at your earliest convenience? I am eager to exchange insights and explore the avenues where our paths might converge.

Thank you for considering my application. I am eagerly looking forward to the possibility of embarking on this exciting journey with {company}.

Warm regards,

Sun Gajiwala
sungajiwala54@gmail.com
+1 2038091938
"""

# Setup SMTP server
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
server.login(email_address, email_password)

# Iterate through data and send emails
# Iterate through data and send emails
for index, row in df.iterrows():
    recipient_name = row['name']
    recipient_email = row['email']
    recipient_company = row['company']

    if not recipient_email:
        print(f"Skipping {recipient_name} due to missing email address.")
        continue

    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = recipient_email
    msg['Subject'] = subject

    body = body_template.format(name=recipient_name,company = recipient_company)
    msg.attach(MIMEText(body, 'plain'))

    # Attach resume
    resume_path = cred.resume_path
    with open(resume_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header(
        'Content-Disposition',
        f'attachment; filename=resume.pdf'
    )
    msg.attach(part)

    try:
        # Send email
        server.sendmail(email_address, recipient_email, msg.as_string())
        print(f"Email sent to {recipient_name} at {recipient_email}.")
    except Exception as e:
        print(f"Failed to send email to {recipient_name} at {recipient_email}: {str(e)}")

# Quit server
server.quit()
