
from sys import stderr
import smtplib
import getpass

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


def print_mean( mean ):
    
    body = \
    """
    The mean value is currently equal to %f.\n
    """ % mean

    print '%s' % body

    return

def setup_server( pwd=None ):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()

    sender = "goodspeedviper@gmail.com"
    pwd='slowbadsnake'
    if pwd is None:
        pwd = getpass.getpass()

    #Next, log in to the server
    try:
        server.login( sender, pwd )
    except smtplib.SMTPAuthenticationError as e:
        stderr.write("""
        Warning: %s was caught while trying to authenticate
        with Gmail""" % (e))
        return None
    
    srvDict = {'server':server,
               'sender':sender}

    return srvDict



def send_mean( mean, recipients ):

    srvDict = setup_server()
    
    # If setup failed, don't email... keep going
    if srvDict is None:
        return

    body = \
    """
    Viper system test:
    The mean value is currently equal to %f.\n
    """ % mean

    msg = MIMEText(body)
    msg['Subject'] = "test message from viper"
    msg['From'] = srvDict['sender']
    msg['To'] = ', '.join(recipients)
    
    try:
        srvDict['server'].sendmail( srvDict['sender'], 
                                    recipients,
                                    msg.as_string() )
    except smtplib.SMTPDataError as e:
        stderr.write("""
        Warning: %s was caught while trying to notify
        of mean = %f""" % (e,mean))

    srvDict['server'].close()

    return


def send_msg( subject, message, recipients, pwd=None ):

    srvDict = setup_server(pwd)
    if srvDict is None:
        print "Not emailing because of gmail issues"
        return

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = srvDict['sender']
    msg['To'] = ', '.join(recipients)

    try:
        srvDict['server'].sendmail( srvDict['sender'], 
                                    recipients,
                                    msg.as_string() )
    except smtplib.SMTPDataError as e:
        stderr.write("""
        Warning: %s was caught while trying to notify
        with the following message:
        %s""" % (e,message))

    srvDict['server'].close()

    return

def send_msg_with_jpg( subject, message, fname, recipients, pwd=None  ):
    
    # Initialize
    srvDict = setup_server(pwd)
    if srvDict is None:
        print "Not emailing because of gmail issues"
        return
    
    # Compose the email
    msg = MIMEMultipart()
    body = MIMEText(message,'plain')
    msg['Subject'] = subject
    msg['From'] = srvDict['sender']
    msg['To'] = ', '.join(recipients)
    msg.attach(body)

    # Attach image
    try:
        msg.attach(MIMEImage(file(fname).read(), _subtype="jpeg"))
    except IOError as e:
        message += "\nNo Image Available at This Time\n"
        body = MIMEText(message,'plain')
        msg.attach(body)

    # Send email
    try:
        srvDict['server'].sendmail( srvDict['sender'], 
                                    recipients,
                                    msg.as_string() )
    except (smtplib.SMTPDataError, smtplib.SMTPServerDisconnected, smtplib.SMTPRecipientsRefused) as e:
        stderr.write("""
        Warning: 
        %s
        
        was caught while trying to notify of:
         %s
        """ % (str(e),message))
    
    # Close it out, and get out
    srvDict['server'].close()

    return

