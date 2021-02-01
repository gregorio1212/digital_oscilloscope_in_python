# digital_oscilloscope_in_python
Python script that reads data from a .txt file and plots it. The data on the .txt file consists of values of a ADC converter.
They have a sinusoidal format. The sampling frequency is 900Hz and the ADC is a 10bit with 5V limit.

## Python virtualenv

To create and activate python virtualenv run:

```sh
python3 -m virtualenv .env
source .env/bin/activate
# install dependencies
pip3 install -r requirements.txt
```
