import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date
from questrade_api import Questrade

def stock_price_summary(account_number):
    # call api
    q = Questrade()

    # get account position details
    positions = q.account_positions(account_number)
    position_list = []
    
    # calculate percentage gain/loss using current stock price
    for position in positions['positions']:
        sym_and_percentage_gain_loss = {}
        
        symbol = position['symbol']
        entry_price = float(position['averageEntryPrice'])
        current_price = float(position['currentPrice'])
        
        percentage_gain_loss = round(((current_price - entry_price)/entry_price)*100, 2)
        sym_and_percentage_gain_loss[symbol] = percentage_gain_loss
        sym_and_percentage_gain_loss['Day P&L'] = position['dayPnl'] # grab pnl for reference
        
        position_list.append(sym_and_percentage_gain_loss)
    
    return position_list

    
def send_email(sender, recipient, sender_password, trading_account_number):
    # get today's date
    today = date.today()
    
    formatted_body = ''
    for position in stock_price_summary(trading_account_number):
        formatted_body += str(position) + '\n\n'
    
    body = 'Here is your summary for today: \n\n' + formatted_body + '\n\n'
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
