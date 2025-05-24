import os

# Database configuration
DB_USERNAME = os.getenv('DB_USERNAME', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME', 'mydb')

# Application configuration
SECRET_KEY = os.getenv('SECRET_KEY', 'asdf#FGSgvasgf$5$WGT')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Email configuration
SMTP_SERVER = os.getenv('SMTP_SERVER', '')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SMTP_USERNAME = os.getenv('SMTP_USERNAME', '')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
DEFAULT_SENDER = os.getenv('DEFAULT_SENDER', 'notifications@i9robotica.com')
