# Package Overview
This contains functions to help me get data from several sources:
* [OpenAI's ChatGPT](https://platform.openai.com/api-keys) 
* Bureau of Labor Statistics (BLS) 
  * See example here: https://www.bls.gov/developers/api_python.htm#python2
  * Signatures: https://www.bls.gov/developers/api_signature_v2.htm

## API Keys
You'll need to make sure that you obtain API keys. Store them as environment variables so that you do not have to share your API key in your code. An environment variable resides on your computer, so you'll have to save them on each computer that you use.

The way you set it differs between Mac/Linux and Windows.

### Approach using terminal for Mac

This creates a line in the .zshrc file: 
`echo "export OPEN_API_KEY=<apiKey>" >> ~/.zshrc`

Test if it exists: `cat ~./zshrc`

Set it permanently: `source ~/.zshrc`

Get environment variables like this: 
`os.environ['OPENAI_KEY']`
or

`os.environ.get("OPEN_API_KEY")`

## Other useful notes

### Github workflow
git status
git pull
git add file.txt or git add .
git commit -m "message"
git push

### Finding folder where packages are located
import sys; sys.path
help('modules')