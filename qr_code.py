import cv2
from pyzbar.pyzbar import decode
import xml.etree.ElementTree as ET
from twilio.rest import Client
import pyttsx3  # Import pyttsx3 for text-to-speech

# Define the expected values for comparison

# Twilio credentials
account_sid = 'ACfbdad9fa3970ca314bf156193517cec9'
auth_token = '78e1a5f5632e0919c825cbf449654602'
twilio_phone_number = '+15102503972'
user_phone_number = '+918870666787'

expected_data = {
    "uid": "336294599969",
    "name": "Barvin",
    "gender": "M",
    "yob": "2003",
    "co": "S/O: Sasi Kumar",
    "house": "29",
    "street": "yadhavar north street",
    "vtc": "Vadakku Vallioor",
    "po": "Vallioor",
    "dist": "Tirunelveli",
    "subdist": "Radhapuram",
    "state": "Tamil Nadu",
    "pc": "627117",
    "dob": "2003-06-08"
}

def main():
    # Open a video capture device (webcam)
    cap = cv2.VideoCapture(1)

    details_verified = False
    not_verified_printed = False
    call_made = False

    # Initialize pyttsx3 engine for text-to-speech
    engine = pyttsx3.init()

    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()

        # Decode QR codes from the frame
        decoded_objects = decode(frame)
        if decoded_objects:
            for obj in decoded_objects:
                data = obj.data.decode('utf-8')
                print("Scanned Data:", data)
                

                # If details are already verified, skip further comparisons
                if details_verified:
                    continue

                # Compare the scanned data with expected data
                if compare_with_expected_data(data):
                    print("Details verified.")
                    details_verified = True

                    # Generate and play the audio output saying "Details verified"
                    engine.say("Details verified")
                    engine.runAndWait()
                else:
                    if not_verified_printed:
                        continue
                    print("Not verified")
                    not_verified_printed = True


                    engine.say("Details not verified")
                    engine.runAndWait()

        # Display the frame with detected QR codes
        cv2.imshow("QR Code Scanner", frame)

        if not_verified_printed and not call_made:
            # Call the user using Twilio if details are not verified and call not made yet
            call_user_with_twilio()
            call_made = True

        if details_verified or call_made:
            # Automatically close the frame after verification or call
            cv2.waitKey(3000)  # Wait for 3 seconds (adjust as needed)
            break

        # Press 'q' to quit the program
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release the video capture device and close the OpenCV window
    cap.release()
    cv2.destroyAllWindows()

def compare_with_expected_data(xml_data):
    # Parse the XML data
    try:
        root = ET.fromstring(xml_data)

        # Extract attributes from the XML
        attributes = {}
        for key, value in root.attrib.items():
            attributes[key] = value

        # Compare the extracted attributes with expected values
        if attributes == expected_data:
            return True
        else:
            return False
    except ET.ParseError:
        return False

def call_user_with_twilio():
    # Initialize Twilio client
    client = Client(account_sid, auth_token)

    # Create a call
    call = client.calls.create(
        to=user_phone_number,
        from_=twilio_phone_number,
        url='http://demo.twilio.com/docs/voice.xml'  # Replace with your TwiML URL
    )

    print("Calling user...")

if __name__ == "__main__":
    main()
