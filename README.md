# Novelscrape

A educational scraping implementation to pull online paragraph based text content, organize based on user configuration and generated PDF to easy reading.

### Major tools
- Beautiful Soup
- Selenium

### Major commands

```bash
# Download Chapters
python3 main.py --novel lord_of_mysteries --pstart 1 --pend 15

# Create PDF from volumes
python3 main.py --novel lord_of_mysteries --pdfiy all

# Compile Volumes
python3 main.py --novel lord_of_mysteries --volumize all
```
