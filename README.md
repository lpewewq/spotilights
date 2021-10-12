# Lightstrip

## MCU
MCU just takes serial data to display on the LED strip.
Compile and flash with ```make flash```.
Don't forget to adjust USB device in Makefile and to ```chmod 666``` it if necessary.

## APP
The python app computes (audio responsive) effects and sends them via USB to the MCU.

### Installation
1. Create virtual environment: ```python3 -m venv venv```
2. Enter virtual environment: ```. venv/bin/activate```
3. Install requirements: ```pip install -r requirements.txt```
4. Create instance folder: ```mkdir -p instance && cp config_template.py instance/config.py```
5. Add spotify authentication credentials in ```instance/config.py``` and configure app as needed
6. Run the Flask server ```flask run```

## References

https://www.embeddedrelated.com/showarticle/528.php
