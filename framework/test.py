from sic_framework.devices import WebserverConf, WebserverService
from sic_framework.services.webserver import GetWebText
from sic_framework.devices import NaoqiTabletService, NaoqiLoadUrl
import logging

class ShowWebImage:

    def __init__(self):
        # Set up the webserver configuration
        web_conf = WebserverConf(host="0.0.0.0", port=8080)

        # Start the webserver service
        self.webserver_connector = WebserverService(device_id='web', conf=web_conf)

        # Start the NaoqiTabletService
        self.pepper_tablet_connector = NaoqiTabletService(device_id='marvin_tab')

        # Path to the HTML file
        html_file = "show_web_image.html"

        # Path to the image
        image_path = "static/images/sample_image.jpg"

        # URL for the webserver
        web_url = "http://localhost:8080/"

        # HTML content with image source
        with open(html_file) as file:
            data = file.read()
            # Replace the placeholder for image source with the actual image path
            data = data.replace("{{ image_source }}", image_path)
            self.webserver_connector.send_message(GetWebText(data))

        # Send URL to NaoqiTabletService to display on Pepper's tablet
        self.pepper_tablet_connector.send_message(NaoqiLoadUrl(web_url))

if __name__ == "__main__":
    show_web_image_instance = ShowWebImage()

