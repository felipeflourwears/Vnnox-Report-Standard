# Vnnox Report Automation Standard


## Create the enviroment
```bash
cd ~/Documentos/Github/vnnox-report-standard

# Create venv
python3 -m venv venv

# Activate the environment
source venv/bin/activate

#Dependencies
pip install -r requirements.txt

```

## Download wkhtmltopdf version according to OS
```bash
https://wkhtmltopdf.org/downloads.html
```
### Linux
Install the package
```bash
sudo dpkg -i wkhtmltox_0.12.6.1-2.jammy_amd64.deb
```

Install some requirements to use the library
```bash
sudo apt-get update
sudo apt-get install -y xfonts-75dpi xfonts-base
```

Verify the version
```bash
flourwears@flourwears:~/Descargas$ wkhtmltopdf --version
wkhtmltopdf 0.12.6.1 (with patched qt)
flourwears@flourwears:~/Descargas$ which wkhtmltopdf
/usr/local/bin/wkhtmltopdf
flourwears@flourwears:~/Descargas$ 
```


