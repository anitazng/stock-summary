import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date
from questrade_api import Questrade

def stock_summary(account_number):
    # call api
    q = Questrade()

    # get account position details
    positions = q.account_positions(account_number)
    position_list = []
    total_pnl = 0
    
    # calculate percentage gain/loss using current stock price
    for position in positions['positions']:
        summary = {}
        
        symbol = position['symbol']
        entry_price = float(position['averageEntryPrice'])
        current_price = float(position['currentPrice'])
        
        percentage_gain_loss = round(((current_price - entry_price)/entry_price)*100, 2)
        summary[symbol] = percentage_gain_loss
        summary['Day P&L'] = position['dayPnl'] # grab pnl for reference
        total_pnl += position['dayPnl']
        
        position_list.append(summary)
    
    return (position_list, str(round(total_pnl, 2)))

    
def send_email(sender, recipient, sender_password, trading_account_number):
    today = date.today()
    position_list = stock_summary(trading_account_number)[0]
    total_pnl = stock_summary(trading_account_number) [1]
    
    formatted_body = ''
    for position in position_list:
        formatted_body += str(position) + '\n'
    
    body = 'Here is your summary for today: \n\n' + formatted_body + '\n\n' + \
           'Total P&L for the day: ' + total_pnl
    msg = MIMEMultipart()
    msg['Subject'] = 'Your Stock Summary: ' + today.strftime('%b-%d-%Y')
    msg['From'] = sender
    msg['To'] = recipient
    msg.attach(MIMEText(body, 'plain'))
    
    # send email
    server = smtplib.SMTP('smtp.office365.com', 587)
    server.ehlo()
    server.starttls()
    server.login(sender, sender_password)
    text = msg.as_string()
    server.sendmail(sender, recipient, text)
    server.quit()
