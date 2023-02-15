import praw
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import newspaper

reddit = praw.Reddit(client_id='', \
                     client_secret='', \
                     user_agent='', \
                     username='', \
                     password='')

top_posts = reddit.subreddit('cybersecurity').top(time_filter='day', limit=5)

# Email configuration
host = "smtp.gmail.com"
port = 587
username = ""
password = ""
from_email = ""
to_email = ""

# Create message container
msg = MIMEMultipart('alternative')
msg['Subject'] = 'Top 5 Reddit posts of the day'
msg['From'] = from_email
msg['To'] = to_email

# Create HTML content
html = "<html><body>"
for post in top_posts:
    if post.is_self:
        # If the post is a text-based post, use the selftext as the summary
        summary = post.selftext
    else:
        # If the post is a link, download and parse the article using newspaper and use the summary
        # as the post summary
        article = newspaper.Article(post.url)
        article.download()
        article.parse()
        summary = article.summary

    # Add the post information and summary to the email
    html += "<p><b>" + post.title + "</b></p>"
    html += "<p><a href='" + post.url + "'>" + post.url + "</a></p>"
    html += "<p>Link to post: <a href='https://www.reddit.com" + post.permalink + "'>https://www.reddit.com" + post.permalink + "</a></p>"
    html += "<p>Score: " + str(post.score) + "</p>"
    html += "<p><i>" + summary + "</i></p>"
    html += "<br>"
html += "</body></html>"

# Attach HTML content to email message
part = MIMEText(html, 'html')
msg.attach(part)

# Send email
with smtplib.SMTP(host, port) as server:
    server.starttls()
    server.login(username, password)
    server.sendmail(from_email, to_email, msg.as_string())

print("Email sent!")
