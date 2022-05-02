## Description
The Python program would satisfy the following
requirements:
- Be an API answering "questions" with a json payload
- Call to an arbitrary external executable
- Handle custom massages for http status codes #400, #404, #500, #501, etc.
- Handle new requests while performing a blocking call
- Graceful shutdown
- Sample unit test(s)

An example of a sample program that would satisfy the above conditions:
- Make a call to an API with a json structure containing a folder name and parameters to list
files from the folder.
- The parameters could define a filter or just be passed over to `ls`.
- To simulate a blocking call, make the code listing files in a directory sleep for 5 seconds.
- Log and respond with a custom message if a folder does not exist, you have no rights to read
it or simply the URL one tries to reach is not reachable.
- If SIGINT is sent to the API serving script, then make sure you handle all outstanding requests
before shutting down.

When you are ready, host your solution on a GitHub or any similar public service, so that we can
clone it and run it locally.

## Instructions
Run the following command to start the gunicorn server:
`gunicorn kambi_django.wsgi:application -w 2 --reload --timeout 600 -b 0.0.0.0:8000 --graceful-timeout=5`


## Requirements
- [x] No parameter: List files in current folder 
- [x] Pass folder: List files in that folder
- [x] Other parameters: Pass to find (or ls)
- [x] Make API async, test blocking call
- [x] Error handling
    * [x] Invalid folder: custom message, log
    * [x] No rights to read: custom message, log
    * [ ] Invalid URL: custom message, log
- Graceful shutdown
    * [x] Handle all outstanding requests first
    
## API
### Endpoints
- `files/files/`
- `files/files/<folder_name>/`

### Query parameters
- `name`: Passed after the test `-name` in the `find` command's expression 
- `params`: Passed as an expression to the `find` command. The tests -name, -maxdepth and -type are ignored
    * Example use: `files/files/my_folder?name=*.txt&params=-atime%2050`
    * translates to `find my_folder -name "*.txt" -maxdepth 1 -type f-- -atime 50`

### Limitations
- Only directories inside the root can be queried
- Only files are displayed
- Subdirectories are neither searched, nor shown
