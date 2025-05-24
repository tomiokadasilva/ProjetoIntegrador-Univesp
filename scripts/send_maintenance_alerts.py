import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import os
import sys
import argparse

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.customer import Customer
from src.models.user import db
from flask import Flask

def create_app():
    """Create a Flask app instance for script execution"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USERNAME', 'root')}:{os.getenv('DB_PASSWORD', 'password')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME', 'mydb')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

def send_email(recipient, subject, body, smtp_server, smtp_port, smtp_user, smtp_password):
    """Send email using SMTP"""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = recipient
        msg['Subject'] = subject
        
        # Attach body
        msg.attach(MIMEText(body, 'html'))
        
        # Connect to server and send
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()
        
        print(f"Email sent successfully to {recipient}")
        return True
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False

def get_maintenance_alerts(days_threshold=30):
    """Get customers with upcoming maintenance"""
    today = datetime.now().date()
    customers = Customer.query.all()
    
    alerts = []
    for customer in customers:
        maintenance_date = customer.get_maintenance_date()
        days_until_maintenance = (maintenance_date - today).days
        
        if days_until_maintenance <= days_threshold:
            alerts.append({
                'customer': customer,
                'maintenance_date': maintenance_date,
                'days_until_maintenance': days_until_maintenance,
                'status': 'Overdue' if days_until_maintenance < 0 else 'Due Soon'
            })
    
    # Sort by urgency (most urgent first)
    alerts.sort(key=lambda x: x['days_until_maintenance'])
    return alerts

def generate_alert_email(alerts, company_name="i9Robótica"):
    """Generate HTML email content for maintenance alerts"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            .header {{ background-color: #4CAF50; color: white; padding: 10px; text-align: center; }}
            .content {{ padding: 20px; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
            .overdue {{ color: red; font-weight: bold; }}
            .due-soon {{ color: orange; font-weight: bold; }}
            .footer {{ margin-top: 20px; font-size: 12px; color: #666; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h2>{company_name} - Maintenance Alerts</h2>
        </div>
        <div class="content">
            <p>The following customers require maintenance attention:</p>
            
            <table>
                <tr>
                    <th>Customer</th>
                    <th>Phone</th>
                    <th>Address</th>
                    <th>Installation Date</th>
                    <th>Maintenance Date</th>
                    <th>Status</th>
                </tr>
    """
    
    for alert in alerts:
        customer = alert['customer']
        status_class = "overdue" if alert['days_until_maintenance'] < 0 else "due-soon"
        
        html += f"""
                <tr>
                    <td>{customer.name}</td>
                    <td>{customer.phone}</td>
                    <td>{customer.address}</td>
                    <td>{customer.installation_date.strftime('%Y-%m-%d')}</td>
                    <td>{alert['maintenance_date'].strftime('%Y-%m-%d')}</td>
                    <td class="{status_class}">{alert['status']} ({alert['days_until_maintenance']} days)</td>
                </tr>
        """
    
    html += f"""
            </table>
            
            <div class="footer">
                <p>This is an automated message from the {company_name} Customer Management System.</p>
                <p>Generated on: {today}</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html

def main():
    """Main function to run the alert script"""
    parser = argparse.ArgumentParser(description='Send maintenance alert emails')
    parser.add_argument('--days', type=int, default=30, help='Days threshold for maintenance alerts')
    parser.add_argument('--recipient', type=str, required=True, help='Email recipient')
    parser.add_argument('--smtp_server', type=str, required=True, help='SMTP server')
    parser.add_argument('--smtp_port', type=int, default=587, help='SMTP port')
    parser.add_argument('--smtp_user', type=str, required=True, help='SMTP username')
    parser.add_argument('--smtp_password', type=str, required=True, help='SMTP password')
    args = parser.parse_args()
    
    # Create and configure Flask app
    app = create_app()
    
    with app.app_context():
        # Get maintenance alerts
        alerts = get_maintenance_alerts(args.days)
        
        if not alerts:
            print("No maintenance alerts found within the specified threshold.")
            return
        
        # Generate email content
        subject = f"i9Robótica - Maintenance Alerts ({len(alerts)} customers)"
        body = generate_alert_email(alerts)
        
        # Send email
        send_email(
            args.recipient,
            subject,
            body,
            args.smtp_server,
            args.smtp_port,
            args.smtp_user,
            args.smtp_password
        )

if __name__ == "__main__":
    main()
