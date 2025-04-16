import os

from puma.apps.android.whatsapp.whatsapp import WhatsappActions

if __name__ == '__main__':
    os.environ['ANDROID_HOME'] = "C:\\Users\\User\\AppData\\Local\\Android\\Sdk"
    whatsapp = WhatsappActions('34281JEHN03866')
    whatsapp.send_message("test", "Alice")